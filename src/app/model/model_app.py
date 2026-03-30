import ursina as ur
import numpy as np
from app.model.cube import Cube 
from ursina.shaders import camera_grayscale_shader
from ursina import EditorCamera
import os
from PIL import Image

class ModelApp:
    def __init__(self, sequence):
        self.app = ur.Ursina(title = 'Cube model')

        self.camera = EditorCamera()
        self.camera.rotation = (30, -45, 0)         # rotate camera 30 degrees up, 45 to the left
        self.camera.shader = camera_grayscale_shader

        img_path = self.__set_img_path()
        self.__init_img(img_path) 
        
        self.sequence = sequence
        self.__init_sq_text()

        self.cube = Cube(self.img, self.sequence)

        self.animate_button = ur.Button('Scramble', position=(0.0,0.4), radius=.01, scale=(0.2, 0.07),
                                         on_click=self.cube.animate_sequence)

    def run_model_app(self):
        self.app.run()

    def __set_img_path(self):
        curr_dir = os.path.dirname(os.path.abspath(__file__))   # model dir path
        root_dir = os.path.dirname(os.path.dirname(os.path.dirname(curr_dir)))
        return os.path.join(root_dir, "assets", "cube-colors", "cube-colors.png")

    def __init_img(self, img_path):
        try:
            self.img = Image.open(img_path).convert('RGB')

        except Exception as e:
            raise(f"Couldn't load texture {e}")
        
    def __init_sq_text(self):
        self.sq_text = ur.Text(text=self.sequence, position=(-.5, .5), scale=1.3, color=ur.color.red)