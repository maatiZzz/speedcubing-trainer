import customtkinter as ctk
from cube_scrambler.core.timer import Stopwatch


class TimerDisplay(ctk.CTkLabel):
    """CustomTkinter label widget wrapping the domain Stopwatch."""

    def __init__(self, timer_frame: ctk.CTkFrame) -> None:
        super().__init__(timer_frame, text="00:00:000 s", font=("Arial", 26))
        self.grid(row=0, column=0, padx=20, pady=40, sticky="new", columnspan=2)
        self.stopwatch = Stopwatch()

    def start_timer(self) -> None:
        if not self.stopwatch.running:
            return
        self.stopwatch.start()
        self.update_timer()

    def change_timer_state(self) -> None:
        self.stopwatch.toggle()

    def update_timer(self) -> None:
        if not self.stopwatch.running:
            return
        self.configure(text=self.stopwatch.tick())
        self.after(15, self.update_timer)

    def get_timer_state(self) -> bool:
        return self.stopwatch.running

    def reset_timer(self) -> None:
        self.stopwatch.reset()
        self.configure(text="00:00:000 s")

    def resume(self) -> None:
        self.stopwatch.resume()
        self.update_timer()

    def get_paused(self) -> bool:
        return self.stopwatch.paused

    def set_paused(self, state: bool) -> None:
        self.stopwatch.paused = state
