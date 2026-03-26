import customtkinter as ctk
from app.logic.cube import Cube
from app.logic.timer import Timer

class App(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.geometry("900x500")
        self.title("Cube scrambler")

        self.cube = Cube()
        
        self.grid_columnconfigure((0), weight = 1)
        self.grid_rowconfigure((0, 1), weight = 1)

        # SCRAMBLE FRAME

        self.sequence_frame = ctk.CTkFrame(self)
        self.sequence_frame.grid(row=0, column=0, padx=20, pady=20, sticky="new")
        self.sequence_frame.grid_columnconfigure((0), weight=1)

        self.sequence_string = ctk.CTkLabel(self.sequence_frame, text="Generate your scramble", font=('Arial', 20))
        self.generate_button = ctk.CTkButton(self.sequence_frame, text="Generate scramble", command=self.generate,  bg_color="black")
        self.sequence_string.grid(row = 0, column = 0, padx = 20, pady = 40, sticky = "new")
        self.generate_button.grid(row = 1, column = 0, padx = 20, pady = 40, sticky = "sew")

        # TIMER FRAME

        self.timer_frame = ctk.CTkFrame(self)
        self.timer_frame.grid(row=1, column=0, padx=20, pady=20, sticky="sew")
        self.timer_frame.grid_columnconfigure((0, 1), weight=1)
        
        self.timer = Timer(self.timer_frame)
        self.start_stop_button = ctk.CTkButton(self.timer_frame, text="Start", command=self.timer_clicked, bg_color="black", fg_color="green")
        self.reset_button = ctk.CTkButton(self.timer_frame, text="Reset", command=self.reset_clicked, bg_color="black", fg_color="#ff4d01")
        self.start_stop_button.grid(row = 1, column = 0, padx = 20, pady = 40, sticky = "sew")
        self.reset_button.grid(row = 1, column = 1, padx = 20, pady = 40, sticky = "sew")

    def generate(self):
        self.cube.generate_sequence()
        sq = self.cube.get_sequence_str()
        self.sequence_string.configure(text=sq)

    def timer_clicked(self):
        self.timer.change_timer_state()
        self.timer.start_timer()

        if (self.timer.get_timer_state()):
            self.start_stop_button.configure(text = "Stop", fg_color = "red")
        else:
            self.start_stop_button.configure(text = "Start", fg_color = "green")

    def reset_clicked(self):
        self.timer.reset_timer()