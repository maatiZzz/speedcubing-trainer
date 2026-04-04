from ursina import Button, Slider, Text, color, Func, Sequence, Entity
from app.model.cube.cube import Cube 
from ursina.shaders import camera_grayscale_shader
from ursina import EditorCamera
import ursina

class MainScene(Entity):
    def __init__(self, img, queue, sequence=''):
        super().__init__()

        self.__init_camera()

        self.sequence = sequence
        self.__init_sq_text()

        self.process_queue = queue

        self.img = img

        self.cube = Cube(self.img, self.sequence)

        self.moves_queue = Sequence()
        
        self.__init_speed_slider()
        
        self.__init_stop_button()
        self.__init_resume_button()
        self.__init_animate_button()
        self.__init_reset_button()
    
    def update(self):
        if not self.process_queue.empty():              # new generated sequence in processes queue
            self.sequence = self.process_queue.get()

            self.cube.destroy_cube()
            self.cube = Cube(self.img, self.sequence)

            ursina.destroy(self.sq_text)
            self.__init_sq_text()

        if self.moves_queue.finished:
            self.__set_start_animation_buttons()

        if self.moves_queue.paused:
            self.__set_paused_animation_buttons()

    def run_animation(self):
        self.moves_queue.kill()
        self.moves_queue = Sequence()
        
        self.cube.animate_sequence(self.moves_queue, self.speed_slider, self.stop_button, self.animate_button)
        self.resume_button.on_click = Func(self.cube.resume_animation, self.moves_queue, self.resume_button, self.stop_button)
        self.stop_button.on_click=Func(self.cube.stop_animation, self.moves_queue)

    def reset_animation(self):
        self.cube.destroy_cube()
        self.cube = Cube(self.img, self.sequence)

        self.moves_queue.kill()
        self.moves_queue = Sequence()
        
        self.__set_start_animation_buttons()

    def __set_start_animation_buttons(self):
        self.speed_slider.enabled = True
        self.animate_button.enabled = True
        self.stop_button.enabled = False
        self.resume_button.enabled = False
        self.reset_button.enabled = False
    
    def __set_paused_animation_buttons(self):
        self.resume_button.enabled = True
        self.reset_button.enabled = True
        self.stop_button.enabled = False

    def __init_sq_text(self):
        self.sq_text = Text(text=self.sequence, origin=(0, 0), position=(0, .4), scale=1.3, size = 2, color=color.hex('#F5F5F5'))
    
    def __init_camera(self):
        self.camera = EditorCamera()
        self.camera.rotation = (30, -45, 0)         # rotate camera 30 degrees up, 45 to the left
        self.camera.shader = camera_grayscale_shader

    def __init_speed_slider(self):
        self.speed_slider = Slider(0.1, 0.9, default = 0.5, position=(0, -0.3), step=0.01,
                                    text='Speed', bar_color=color.hex('#F5F5F5'), dynamic=True)
        self.speed_slider.on_value_changed = Func(self.cube.change_speed, self.speed_slider)

    def __init_stop_button(self):
        self.stop_button = Button('Stop', position=(0,-0.4), radius=.01, scale=(0.1, 0.05), enabled = False,
                                         on_click=Func(self.cube.stop_animation, self.moves_queue))
        
    def __init_resume_button(self):
        self.resume_button = Button('Resume', position=(0,-0.4), radius=.01, scale=(0.1, 0.05), enabled = False)
        self.resume_button.on_click = Func(self.cube.resume_animation, self.moves_queue, self.resume_button, self.stop_button)

    def __init_animate_button(self):
        self.animate_button = Button('Scramble', position=(0.0,-0.4), radius=.01, scale=(0.1, 0.05))
        self.animate_button.on_click = Func(self.run_animation)
    
    def __init_reset_button(self):
        self.reset_button = Button('Reset', position=(0.2,-0.4), radius=.01, scale=(0.1, 0.05))
        self.reset_button.on_click = Func(self.reset_animation)