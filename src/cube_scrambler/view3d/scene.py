import ursina
from ursina import Button, EditorCamera, Entity, Func, Sequence, Slider, Text, color
from ursina.shaders import camera_grayscale_shader
from cube_scrambler.view3d.cube import Cube


class MainScene(Entity):
    """Ursina 3D scene managing the camera, cube entity, and playback controls."""

    def __init__(self, queue: object = None, sequence: str = "") -> None:
        super().__init__()

        self._init_camera()
        self.sequence: str = sequence
        self._init_sq_text()

        self.process_queue = queue
        self.cube = Cube(self.sequence)
        self.moves_queue = Sequence()


        self._init_speed_slider()
        self._init_stop_button()
        self._init_animate_button()
        self._init_reset_button()
        self._init_resume_button()

    def update(self) -> None:
        if self.process_queue is not None and not self.process_queue.empty():
            msg = self.process_queue.get()
            if msg == "__SHUTDOWN__":
                ursina.application.quit()
                return

            self.sequence = str(msg)
            self.moves_queue.kill()
            self.moves_queue = Sequence()

            self.cube.destroy_cube()
            self.cube = Cube(self.sequence)

            ursina.destroy(self.sq_text)
            self._init_sq_text()
            self._set_start_animation_buttons()

        if self.moves_queue.finished:
            self._set_start_animation_buttons()

        if self.moves_queue.paused:
            self._set_paused_animation_buttons()

    def run_animation(self) -> None:
        self.moves_queue.kill()
        self.moves_queue = Sequence()

        self.cube.animate_sequence(
            self.moves_queue,
            self.speed_slider,
            self.stop_button,
            self.animate_button,
        )
        self.resume_button.on_click = Func(
            self.cube.resume_animation,
            self.moves_queue,
            self.resume_button,
            self.stop_button,
            self.reset_button,
        )
        self.stop_button.on_click = Func(self.cube.stop_animation, self.moves_queue)

    def reset_animation(self) -> None:
        self.moves_queue.kill()
        self.moves_queue = Sequence()

        self.cube.destroy_cube()
        self.cube = Cube(self.sequence)

        self._set_start_animation_buttons()

    def _set_start_animation_buttons(self) -> None:
        self.speed_slider.enabled = True
        self.animate_button.enabled = True
        self.stop_button.enabled = False
        self.resume_button.enabled = False
        self.reset_button.enabled = True

    def _set_paused_animation_buttons(self) -> None:
        self.resume_button.enabled = True
        self.reset_button.enabled = True
        self.stop_button.enabled = False

    def _init_sq_text(self) -> None:
        self.sq_text = Text(
            text=self.sequence,
            origin=(0, 0),
            position=(0, 0.4),
            scale=1.3,
            size=2,
            color=color.hex("#F5F5F5"),
        )

    def _init_camera(self) -> None:
        self.camera = EditorCamera()
        self.camera.rotation = (30, 135, 0)
        self.camera.shader = camera_grayscale_shader

    def _init_speed_slider(self) -> None:
        self.speed_slider = Slider(
            0.1,
            0.9,
            default=0.5,
            position=(0, -0.3),
            step=0.01,
            text="Speed",
            bar_color=color.hex("#F5F5F5"),
            dynamic=True,
        )
        self.speed_slider.on_value_changed = Func(
            self.cube.change_speed, self.speed_slider
        )

    def _init_stop_button(self) -> None:
        self.stop_button = Button(
            "Stop",
            position=(0, -0.4),
            radius=0.01,
            scale=(0.1, 0.05),
            enabled=False,
            on_click=Func(self.cube.stop_animation, self.moves_queue),
        )

    def _init_resume_button(self) -> None:
        self.resume_button = Button(
            "Resume",
            position=(0, -0.4),
            radius=0.01,
            scale=(0.1, 0.05),
            enabled=False,
        )
        self.resume_button.on_click = Func(
            self.cube.resume_animation,
            self.moves_queue,
            self.resume_button,
            self.stop_button,
            self.reset_button,
        )

    def _init_animate_button(self) -> None:
        self.animate_button = Button(
            "Scramble",
            position=(0.0, -0.4),
            radius=0.01,
            scale=(0.1, 0.05),
            on_click=Func(self.run_animation),
        )

    def _init_reset_button(self) -> None:
        self.reset_button = Button(
            "Reset",
            position=(0.2, -0.4),
            radius=0.01,
            scale=(0.1, 0.05),
            on_click=Func(self.reset_animation),
        )
