import os
import customtkinter as ctk
from app.logic.cube import Cube
from app.logic.timer import Timer

class App(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.geometry("900x500")
        self.title("Cube scrambler")

        # need to load absolute path
        curr_dir = os.path.dirname(os.path.abspath(__file__))
        root_dir = os.path.dirname(os.path.dirname(os.path.dirname(curr_dir)))
        icon_path = os.path.join(root_dir, "assets", "icon", "icon.ico")

        try:
            self.iconbitmap(icon_path)
        except Exception as e:
            print(f"Couldn't load icon {e}")


        self.cube = Cube()

        self.grid_columnconfigure((0), weight = 1)
        self.grid_rowconfigure((0, 1), weight = 1)

        # SCRAMBLE FRAME
        self.__init_scramble_frame()

        # TIMER FRAME
        self.__init_timer_frame()


    def generate(self):
        self.cube.generate_sequence()
        sq = self.cube.get_sequence_str()
        self.sequence_string.configure(text=sq)

    def start_stop_clicked(self):
        self.timer.change_timer_state()
        self.timer.start_timer()

        if (self.timer.get_timer_state()):
            # running
            self.start_stop_button.configure(text = "Stop", fg_color = "red", hover_color="#7B0000")
        else:
            # paused
            self.start_stop_button.grid_forget()
            self.resume_button.grid(row = 1, column = 0, padx = 20, pady = 40, sticky = "sew")
            self.timer.set_paused(True)

    def resume_button_clicked(self):
        if self.timer.get_paused():
            # allow to resume if paused previosly
            self.resume_button.grid_forget()
            self.start_stop_button.grid(row = 1, column = 0, padx = 20, pady = 40, sticky = "sew")
            
            self.timer.resume()
        
    def reset_clicked(self):
        self.timer.reset_timer()
        self.resume_button.grid_forget()
        self.start_stop_button.grid(row = 1, column = 0, padx = 20, pady = 40, sticky = "sew")
        self.start_stop_button.configure(text = "Start", fg_color = "green", hover_color="#006810")

    def __init_timer_frame(self):
        self.timer_frame = ctk.CTkFrame(self)
        self.timer_frame.grid(row=1, column=0, padx=20, pady=20, sticky="sew")
        self.timer_frame.grid_columnconfigure((0, 1), weight=1)
        
        self.timer = Timer(self.timer_frame)
        self.start_stop_button = ctk.CTkButton(self.timer_frame, text="Start", command=self.start_stop_clicked,
                                                bg_color="black", fg_color="green", hover_color="#006810", font=('Arial', 18))
        self.resume_button = ctk.CTkButton(self.timer_frame, text="Resume", command=self.resume_button_clicked,
                                                bg_color="black", fg_color="green", hover_color="#006810", font=('Arial', 18))
        self.reset_button = ctk.CTkButton(self.timer_frame, text="Reset", command=self.reset_clicked,
                                        bg_color="black", fg_color="#ff4d01", hover_color="#a63400", font=('Arial', 18))
        self.start_stop_button.grid(row = 1, column = 0, padx = 20, pady = 40, sticky = "sew")
        self.reset_button.grid(row = 1, column = 1, padx = 20, pady = 40, sticky = "sew")

    def __init_scramble_frame(self):
        self.sequence_frame = ctk.CTkFrame(self)
        self.sequence_frame.grid(row=0, column=0, padx=20, pady=20, sticky="new")
        self.sequence_frame.grid_columnconfigure((0), weight=1)

        self.sequence_string = ctk.CTkLabel(self.sequence_frame, text="Generate your scramble", font=('Arial', 22))
        self.generate_button = ctk.CTkButton(self.sequence_frame, text="Generate scramble", command=self.generate,
                                               bg_color="black", font=('Arial', 18))
        self.sequence_string.grid(row = 0, column = 0, padx = 20, pady = 40, sticky = "new")
        self.generate_button.grid(row = 1, column = 0, padx = 20, pady = 40, sticky = "sew")