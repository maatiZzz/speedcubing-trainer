from ursina import Ursina
from app.model.main_scene import MainScene
from PIL import Image
import os


class RootApp:
    def __init__(self, generated_sq=''):
        self.app = Ursina(title = 'Cube model')
        
        img_path = self.__set_img_path()
        self.__init_img(img_path) 
        
        self.main_scene = MainScene(self.img, generated_sq)

    def run_root_app(self):
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