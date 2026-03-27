import ursina as ur

class Piece(ur.Entity):
    def __init__(self, position_x, position_y, position_z):
        super().__init__()
        self.model='cube'
        self.color = ur.color.black
        self.scale = (.8, .8, .8)
        self.origin = (0,0,0)
        self.position = ur.Vec3(position_x,position_y,position_z)