import time
import customtkinter as ctk

class Timer(ctk.CTkLabel):
    def __init__(self, timer_frame):
        super().__init__(timer_frame, text = "0.000", font=('Arial', 24))
        self.grid(row = 0, column = 0, padx = 20, pady = 40, sticky = "new", columnspan = 2)

        self.start_timestamp = 0
        self.current_timestamp = 0
        self.elapsed_in_ms = 0
        self.string = ""
        self.running = False

    def start_timer(self):
        if self.running == False:
            return
        
        self.start_timestamp = time.time_ns()
        self.update_timer()

    def __get_current_time(self):
        self.current_timestamp = time.time_ns()
        self.elapsed_in_ms =  (self.current_timestamp - self.start_timestamp) / 1000000
        self.string = str(format(self.elapsed_in_ms, '.3f'))
        return self.string
    
    def change_timer_state(self):
        self.running = not self.running

    def update_timer(self):
        if self.running == False:
            return
        
        self.configure(text = self.__get_current_time())
        self.after(15, self.update_timer)

    def get_timer_state(self):
        return self.running
    
    def reset_timer(self):
        self.start_timestamp = 0
        self.current_timestamp = 0
        self.elapsed_in_ms = 0

        self.configure(text =  "0.000")