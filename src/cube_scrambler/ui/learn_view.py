from collections.abc import Callable
import customtkinter as ctk
from cube_scrambler.config import LEARN_WINDOW_HEIGHT, LEARN_WINDOW_WIDTH
from cube_scrambler.data.persistence.repository import AlgorithmRepository


class LearnView(ctk.CTkToplevel):
    """Scrollable window listing algorithms to practice in the 3D viewer."""

    def __init__(self, on_select_algorithm: Callable[[str], None]) -> None:
        super().__init__()
        self.geometry(f"{LEARN_WINDOW_WIDTH}x{LEARN_WINDOW_HEIGHT}")
        self.title("Learn Algorithms")

        self.on_select_algorithm = on_select_algorithm

        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)

        self.repository = AlgorithmRepository()
        self.repository.initialize()

        self._init_header_frame()
        self._init_list_frame()

    def _init_header_frame(self) -> None:
        self.label_frame = ctk.CTkFrame(self)
        self.label_frame.grid(row=0, column=0, padx=10, pady=10, sticky="new")
        self.label_frame.grid_columnconfigure(0, weight=1)

        self.header_label = ctk.CTkLabel(
            self.label_frame,
            text="Pick an algorithm to practice:",
            font=("Arial", 22),
        )
        self.header_label.grid(row=0, column=0, padx=20, pady=20, sticky="ew")

    def _init_list_frame(self) -> None:
        self.list_frame = ctk.CTkScrollableFrame(self)
        self.list_frame.grid(row=1, column=0, padx=10, pady=10, sticky="nsew")
        self.list_frame.grid_columnconfigure(0, weight=1)

        algorithms = self.repository.get_all()
        for index, alg in enumerate(algorithms):
            row_frame = ctk.CTkFrame(self.list_frame)
            row_frame.grid(row=index, column=0, padx=10, pady=8, sticky="ew")
            row_frame.grid_columnconfigure(0, weight=1)

            info_label = ctk.CTkLabel(
                row_frame,
                text=f"{alg.name}  |  Setup: {alg.setup}  |  Alg: {alg.solution}",
                font=("Arial", 15),
                anchor="w",
            )
            info_label.grid(row=0, column=0, padx=15, pady=10, sticky="ew")

            learn_button = ctk.CTkButton(
                row_frame,
                text=f"Learn {alg.name}",
                command=lambda s=alg.setup: self.on_select_algorithm(s),
                bg_color="black",
                font=("Arial", 16),
                width=140,
            )
            learn_button.grid(row=0, column=1, padx=15, pady=10, sticky="e")
