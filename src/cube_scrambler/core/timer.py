import time


class Stopwatch:
    """Stopwatch class implemented using standard time module."""

    def __init__(self) -> None:
        self.previous_timestamp: int = 0
        self.elapsed_in_ms: float = 0.0
        self.running: bool = False
        self.paused: bool = False

    def start(self) -> None:
        if not self.running:
            return
        self.previous_timestamp = time.monotonic_ns()

    def toggle(self) -> bool:
        self.running = not self.running
        if self.running:
            self.previous_timestamp = time.monotonic_ns()
        return self.running

    def tick(self) -> str:
        if self.running:
            now = time.monotonic_ns()
            self.elapsed_in_ms += (now - self.previous_timestamp) / 1_000_000.0
            self.previous_timestamp = now
        return f"{self.format_elapsed()} s"

    def format_elapsed(self) -> str:
        total_ms = int(self.elapsed_in_ms)
        sec, ms = divmod(total_ms, 1000)
        minutes, sec = divmod(sec, 60)
        return f"{minutes:02d}:{sec:02d}:{ms:03d}"

    def reset(self) -> None:
        self.previous_timestamp = 0
        self.elapsed_in_ms = 0.0
        self.paused = False
        self.running = False

    def resume(self) -> None:
        self.running = True
        self.paused = False
        self.previous_timestamp = time.monotonic_ns()
