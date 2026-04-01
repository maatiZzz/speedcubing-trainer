import os
import customtkinter as ctk
from multiprocessing import Queue, Process
import multiprocessing as mp
from app.logic.generator import Generator
from app.logic.timer import Timer
from app.model.root_app import RootApp
from app.constants.constants import ROOT_WINDOW_HEIGHT, ROOT_WINDOW_WIDTH

class App(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.__init_window("Cube scrambler")

        # MULTIPROCESSING
        self.__init_mp_queue()

        # need to load absolute path
        self.icon_path = self.set_icon_path()
        try:
            self.iconbitmap(self.icon_path)
        except Exception as e:
            print(f"Couldn't load icon {e}")

        self.bind('<space>', lambda event : self.__start_stop_clicked())
        self.bind('<r>', lambda event : self.__reset_clicked())
        self.bind('<g>', lambda event : self.__generate())
        self.bind('<Escape>', lambda event : self.close_app())

        self.moves = ''

        self.generator = Generator()

        self.grid_columnconfigure((0), weight = 1)
        self.grid_rowconfigure((0, 1, 2), weight = 1)

        # SCRAMBLE FRAME
        self.__init_scramble_frame()

        # MODEL FRAME
        self.__init_model_frame()
        
        # TIMER FRAME
        self.__init_timer_frame()

    def __load_3d_model(self):
        # destroy current process if exists
        if hasattr(self, "model_app_process"):
            if self.model_app_process.is_alive():
                self.model_app_process.kill()
        # create new process
        self.model_app_process = mp.Process(target=self.__start_ursina)
        self.model_app_process.start()

    def __start_ursina(self):
        self.model_app = RootApp(self.moves)
        self.model_app.run_root_app()

    def __generate(self):
        self.generator.generate_sequence()
        self.moves = self.generator.get_sequence_str()
        # update sequence frame
        self.sequence_string.configure(text=self.moves)


    def __start_stop_clicked(self):

        self.timer.change_timer_state()
        self.timer.start_timer()

        if (self.timer.get_timer_state()):
            # running
            self.start_stop_button.configure(text = "Stop (space)", fg_color = "red", hover_color="#7B0000")
            self.__show_start_stop_button()
        else:
            # paused
            self.__show_resume_button()
            self.timer.set_paused(True)

    def __resume_button_clicked(self):
        if self.timer.get_paused():
            # allow to resume if paused previosly
            self.__show_start_stop_button()
            self.timer.resume()
        
    def __reset_clicked(self):
        self.timer.reset_timer()
        self.start_stop_button.configure(text = "Start (space)", fg_color = "green", hover_color="#006810")
        self.__show_start_stop_button()

    def __show_start_stop_button(self):
        self.resume_button.grid_forget()
        self.start_stop_button.grid(row = 1, column = 0, padx = 20, pady = 40, sticky = "sew")

    def get_icon_path(self):
        return self.icon_path
    
    def set_icon_path(self):
        curr_dir = os.path.dirname(os.path.abspath(__file__))
        root_dir = os.path.dirname(os.path.dirname(os.path.dirname(curr_dir)))
        icon_path = os.path.join(root_dir, "assets", "icon", "icon.ico")
        self.icon_path = icon_path

    def __show_resume_button(self):
        self.start_stop_button.grid_forget()
        self.resume_button.grid(row = 1, column = 0, padx = 20, pady = 40, sticky = "sew")

    def __init_scramble_frame(self):
        self.sequence_frame = ctk.CTkFrame(self)
        self.sequence_frame.grid(row=0, column=0, padx=10, pady=10, sticky="new")
        self.sequence_frame.grid_columnconfigure((0), weight=1)

        self.sequence_string = ctk.CTkLabel(self.sequence_frame, text="Generate your scramble", font=('Arial', 22))
        self.generate_button = ctk.CTkButton(self.sequence_frame, text="Generate scramble (g)", command=self.__generate,
                                               bg_color="black", font=('Arial', 18))
        self.sequence_string.grid(row = 0, column = 0, padx = 20, pady = 40, sticky = "new")
        self.generate_button.grid(row = 1, column = 0, padx = 20, pady = 40, sticky = "sew")

    def __init_model_frame(self):
        self.model_frame = ctk.CTkFrame(self)
        self.model_frame.grid(row=1, column=0, padx=10, pady=10, sticky="ew")
        self.model_frame.grid_columnconfigure(0, weight=1)

        self.model_button = ctk.CTkButton(self.model_frame, text="View 3D cube model", command=self.__load_3d_model,
                                               bg_color="black", font=('Arial', 18))
        self.model_button.grid(row = 0, column = 0, padx = 20, pady = 40, columnspan = 2, sticky="ew")

    def __init_timer_frame(self):
        self.timer_frame = ctk.CTkFrame(self)
        self.timer_frame.grid(row=2, column=0, padx=1, pady=10, sticky="sew")
        self.timer_frame.grid_columnconfigure((0, 1), weight=1)
        
        self.timer = Timer(self.timer_frame)
        self.start_stop_button = ctk.CTkButton(self.timer_frame, text="Start (space)", command=self.__start_stop_clicked,
                                                bg_color="black", fg_color="green", hover_color="#006810", font=('Arial', 18))
        self.resume_button = ctk.CTkButton(self.timer_frame, text="Resume (space)", command=self.__resume_button_clicked,
                                                bg_color="black", fg_color="green", hover_color="#006810", font=('Arial', 18))
        self.reset_button = ctk.CTkButton(self.timer_frame, text="Reset (r)", command=self.__reset_clicked,
                                        bg_color="black", fg_color="#ff4d01", hover_color="#a63400", font=('Arial', 18))
        self.start_stop_button.grid(row = 1, column = 0, padx = 20, pady = 40, sticky = "sew")
        self.reset_button.grid(row = 1, column = 1, padx = 20, pady = 40, sticky = "sew")
    
    def close_app(self):
        self.destroy()

    def __init_window(self, title):
        string = ''
        string += str(ROOT_WINDOW_WIDTH) + "x" + str(ROOT_WINDOW_HEIGHT) 
        self.geometry(string)
        self.title(title)

    def __init_mp_queue(self):
        self.mp_queue = mp.Queue()