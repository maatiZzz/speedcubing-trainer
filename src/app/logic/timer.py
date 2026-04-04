import time
import customtkinter as ctk

class Timer(ctk.CTkLabel):
    def __init__(self, timer_frame):
        super().__init__(timer_frame, text = "00:00:000 s", font=('Arial', 26))
        self.grid(row = 0, column = 0, padx = 20, pady = 40, sticky = "new", columnspan = 2)

        self.previous_timestamp = 0
        self.current_timestamp = 0
        self.elapsed_in_ms = 0
        self.string = ""
        self.running = False
        self.paused = False

    def start_timer(self):
        if self.running == False:
            return
        
        self.previous_timestamp = time.time_ns()
        self.update_timer()

    def __get_current_time(self):
        self.current_timestamp = time.time_ns()
        self.elapsed_in_ms += (self.current_timestamp - self.previous_timestamp) / 1000000
        self.previous_timestamp = self.current_timestamp

        self.string = self.__convert()
        return f"{self.string} s"
    
    def __convert(self):
        sec, ms = divmod(self.elapsed_in_ms, 1000)
        min, sec = divmod(sec, 60)
        return '%02d:%02d:%03d' % (min, sec, ms)
    
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
        self.previous_timestamp = 0
        self.current_timestamp = 0
        self.elapsed_in_ms = 0

        self.paused = False
        self.running = False

        self.configure(text =  "00:00:000 s")
    
    def resume(self):
        self.running = True

        self.start_timer()

    def get_paused(self):
        return self.paused

    def set_paused(self, state):
        self.paused = state