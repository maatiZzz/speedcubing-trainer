import multiprocessing as mp
import customtkinter as ctk
from cube_scrambler.config import ICON_PATH, ROOT_WINDOW_HEIGHT, ROOT_WINDOW_WIDTH
from cube_scrambler.core.generator import Generator
from cube_scrambler.ui.components.timer_display import TimerDisplay
from cube_scrambler.ui.learn_view import LearnView
from cube_scrambler.view3d.app import RootApp


class App(ctk.CTk):
    """Main CustomTkinter application window."""

    def __init__(self) -> None:
        super().__init__()
        self._init_window("Cube scrambler")

        self.mp_queue: mp.Queue = mp.Queue()
        self.model_app_process: mp.Process | None = None
        self.learn_window: LearnView | None = None

        self._set_icon()
        self._init_key_binds()

        self.moves: str = ""
        self.generator = Generator()

        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure((0, 1, 2), weight=1)

        self._init_scramble_frame()
        self._init_model_frame()
        self._init_timer_frame()

        self.protocol("WM_DELETE_WINDOW", self.close_app)

    def _open_learn_window(self) -> None:
        if self.learn_window is not None and self.learn_window.winfo_exists():
            self.learn_window.focus()
            return
        self.learn_window = LearnView(on_select_algorithm=self._load_3d_model)

    def _load_3d_model(self, sequence: str | None = None) -> None:
        target_sequence = sequence if sequence is not None else self.moves
        if self.model_app_process is not None and self.model_app_process.is_alive():
            self.mp_queue.put(target_sequence)
            return

        self.model_app_process = mp.Process(
            target=self.start_ursina,
            args=(self.mp_queue, target_sequence),
            daemon=True,
        )
        self.model_app_process.start()

    def _stop_3d_process(self) -> None:
        if self.model_app_process is not None and self.model_app_process.is_alive():
            try:
                self.mp_queue.put("__SHUTDOWN__")
                self.model_app_process.join(timeout=1.0)
            except Exception:
                pass
            if self.model_app_process.is_alive():
                self.model_app_process.terminate()
                self.model_app_process.join(timeout=0.5)

    @staticmethod
    def start_ursina(queue: mp.Queue, moves: str) -> None:
        model_app = RootApp(queue, moves)
        model_app.run_root_app()

    def _generate(self) -> None:
        self.generator.generate_sequence()
        self.moves = self.generator.get_sequence_str()
        self.sequence_string.configure(text=self.moves)
        if self.model_app_process is not None and self.model_app_process.is_alive():
            self.mp_queue.put(self.moves)

    def close_app(self) -> None:
        self._stop_3d_process()
        self.destroy()

    def _set_icon(self) -> None:
        if not ICON_PATH.is_file():
            return
        try:
            self.iconbitmap(str(ICON_PATH))
        except Exception:
            pass

    def _show_resume_button(self) -> None:
        self.start_stop_button.grid_forget()
        self.resume_button.grid(row=1, column=0, padx=20, pady=40, sticky="sew")

    def _init_scramble_frame(self) -> None:
        self.sequence_frame = ctk.CTkFrame(self)
        self.sequence_frame.grid(row=0, column=0, padx=10, pady=10, sticky="new")
        self.sequence_frame.grid_columnconfigure(0, weight=1)

        self.sequence_string = ctk.CTkLabel(
            self.sequence_frame,
            text="Generate your scramble",
            font=("Arial", 22),
        )
        self.generate_button = ctk.CTkButton(
            self.sequence_frame,
            text="Generate scramble (g)",
            command=self._generate,
            bg_color="black",
            font=("Arial", 18),
        )
        self.sequence_string.grid(row=0, column=0, padx=20, pady=40, sticky="new")
        self.generate_button.grid(row=1, column=0, padx=20, pady=40, sticky="sew")

    def _init_model_frame(self) -> None:
        self.model_frame = ctk.CTkFrame(self)
        self.model_frame.grid(row=1, column=0, padx=10, pady=10, sticky="ew")
        self.model_frame.grid_columnconfigure((0, 1), weight=1)

        self.model_button = ctk.CTkButton(
            self.model_frame,
            text="View 3D scramble animation",
            command=lambda: self._load_3d_model(self.moves),
            bg_color="black",
            font=("Arial", 18),
        )
        self.model_button.grid(row=0, column=0, padx=20, pady=40, sticky="ew")

        self.learn_button = ctk.CTkButton(
            self.model_frame,
            text="Learn algorithms",
            command=self._open_learn_window,
            bg_color="black",
            font=("Arial", 18),
        )
        self.learn_button.grid(row=0, column=1, padx=20, pady=40, sticky="ew")

    def _init_timer_frame(self) -> None:
        self.timer_frame = ctk.CTkFrame(self)
        self.timer_frame.grid(row=2, column=0, padx=1, pady=10, sticky="sew")
        self.timer_frame.grid_columnconfigure((0, 1), weight=1)

        self.timer = TimerDisplay(self.timer_frame)
        self.start_stop_button = ctk.CTkButton(
            self.timer_frame,
            text="Start (space)",
            command=self._start_stop_clicked,
            bg_color="black",
            fg_color="green",
            hover_color="#006810",
            font=("Arial", 18),
        )
        self.resume_button = ctk.CTkButton(
            self.timer_frame,
            text="Resume (space)",
            command=self._resume_button_clicked,
            bg_color="black",
            fg_color="green",
            hover_color="#006810",
            font=("Arial", 18),
        )
        self.reset_button = ctk.CTkButton(
            self.timer_frame,
            text="Reset (r)",
            command=self._reset_clicked,
            bg_color="black",
            fg_color="#ff4d01",
            hover_color="#a63400",
            font=("Arial", 18),
        )
        self.start_stop_button.grid(row=1, column=0, padx=20, pady=40, sticky="sew")
        self.reset_button.grid(row=1, column=1, padx=20, pady=40, sticky="sew")

    def _init_window(self, title: str) -> None:
        self.geometry(f"{ROOT_WINDOW_WIDTH}x{ROOT_WINDOW_HEIGHT}")
        self.title(title)

    def _init_key_binds(self) -> None:
        self.bind("<space>", lambda event: self._start_stop_clicked())
        self.bind("<r>", lambda event: self._reset_clicked())
        self.bind("<g>", lambda event: self._generate())
        self.bind("<Escape>", lambda event: self.close_app())

    def _start_stop_clicked(self) -> None:
        self.timer.change_timer_state()
        self.timer.start_timer()

        if self.timer.get_timer_state():
            self.start_stop_button.configure(
                text="Stop (space)", fg_color="red", hover_color="#7B0000"
            )
            self._show_start_stop_button()
        else:
            self._show_resume_button()
            self.timer.set_paused(True)

    def _resume_button_clicked(self) -> None:
        if self.timer.get_paused():
            self._show_start_stop_button()
            self.timer.resume()

    def _reset_clicked(self) -> None:
        self.timer.reset_timer()
        self.start_stop_button.configure(
            text="Start (space)", fg_color="green", hover_color="#006810"
        )
        self._show_start_stop_button()

    def _show_start_stop_button(self) -> None:
        self.resume_button.grid_forget()
        self.start_stop_button.grid(row=1, column=0, padx=20, pady=40, sticky="sew")
