from ursina import Ursina
from cube_scrambler.view3d.scene import MainScene


class RootApp:
    """Entrypoint wrapper for Ursina 3D subprocess."""

    def __init__(self, queue: object = None, generated_sq: str = "") -> None:
        self.app = Ursina(title="Cube model")
        self.queue = queue
        self.main_scene = MainScene(self.queue, generated_sq)

    def run_root_app(self) -> None:
        self.app.run()
