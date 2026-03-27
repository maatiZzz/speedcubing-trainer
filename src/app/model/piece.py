import ursina as ur
from ursina import Texture
from PIL import Image
import os

class Piece(ur.Entity):
    def __init__(self, position_x, position_y, position_z):
        super().__init__()
        self.model='cube'
        self.scale = (.8, .8, .8)
        self.origin = (0,0,0)
        self.position = ur.Vec3(position_x,position_y,position_z)
 
        self.img_path = self.__set_img_path()
        try:
            self.img = Image.open(self.img_path).convert('RGB')
            print(self.img.getpixel((0,0)))
            self.texture = Texture(self.img)
            self.texture.filtering = None           # sharp colors
        except Exception as e:
            raise(f"Couldn't load texture {e}")

    def __set_img_path(self):
        curr_dir = os.path.dirname(os.path.abspath(__file__))   # model dir path
        root_dir = os.path.dirname(os.path.dirname(os.path.dirname(curr_dir)))
        return os.path.join(root_dir, "assets", "cube-colors", "cube-colors.png")
