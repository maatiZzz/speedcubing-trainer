import ursina as ur
import numpy as np
from app.model.piece import Piece 
from app.model.input_handler import InputHandler 
from ursina.shaders import camera_grayscale_shader
from ursina import EditorCamera

class ModelApp:
    def __init__(self):
        self.app = ur.Ursina(title='Cube model')
        self.mouse_handler = InputHandler()
        self.camera = EditorCamera()
        self.camera.shader = camera_grayscale_shader

        self.pieces = np.full((3,3,3), Piece(0,0,0))
        for x in range(-1, 2):
            for y in range(-1, 2):
                for z in range(-1, 2):
                    self.pieces[x + 1][y + 1][z + 1] = Piece(x, y, z)

    def run_model_app(self):
        self.app.run()