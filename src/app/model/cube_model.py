import ursina as ur
import numpy as np
from app.model.piece import Piece 
from app.model.input_handler import InputHandler 
from ursina.shaders import camera_grayscale_shader
from ursina import EditorCamera
import os
from PIL import Image

class ModelApp:
    def __init__(self):
        self.app = ur.Ursina(title='Cube model')
        self.mouse_handler = InputHandler()
        self.camera = EditorCamera()
        self.camera.shader = camera_grayscale_shader
        img_path = self.__set_img_path()
        self.__init_img(img_path) 
        

        self.pieces = np.full((3,3,3), Piece(0,0,0, self.img))
        for x in range(-1, 2):
            for y in range(-1, 2):
                for z in range(-1, 2):
                    self.pieces[x + 1][y + 1][z + 1] = Piece(x, y, z, self.img)

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