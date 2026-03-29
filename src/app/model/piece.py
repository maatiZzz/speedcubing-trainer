import ursina as ur
from ursina import Texture
from app.model.face import Face

class Piece(ur.Entity):
    def __init__(self, pos_x, pos_y, pos_z, img):
        super().__init__()
        self.scale = (.95, .95, .95)
        self.origin = (0,0,0)
        self.position = ur.Vec3(pos_x,pos_y,pos_z)
        self.img = img
 
        self.texture = Texture(self.img)
        self.texture.filtering = None           # sharp colors
        
        self.faces = []
        self.__init_faces()
        
        self.combine()                    # batching entitites to optimize rendering 

    def __init_faces(self):
        for _ in range(6):
            if self.position.X_getter() == 0 and self.position.Y_getter() == 0 and self.position.Z_getter() == 0:
                continue    # skip middle cube

            if self.position.X_getter() == -1:                              # left face orange
                self.faces.append(Face(self, self.img, 'l', face_color='r'))
            else:
                self.faces.append(Face(self, self.img, 'l'))

            if self.position.X_getter() == 1:                              # right face red
                self.faces.append(Face(self, self.img, 'r', face_color='o'))
            else:
                self.faces.append(Face(self, self.img, 'r'))

            if self.position.Y_getter() == -1:                              # down face white
                self.faces.append(Face(self, self.img, 'd', face_color='w'))
            else:
                self.faces.append(Face(self, self.img, 'd'))

            if self.position.Y_getter() == 1:                              # up face yellow
                self.faces.append(Face(self, self.img, 'u', face_color='y'))
            else:
                self.faces.append(Face(self, self.img, 'u'))

            if self.position.Z_getter() == -1:                              # back face green
                self.faces.append(Face(self, self.img, 'b', face_color='g'))
            else:
                self.faces.append(Face(self, self.img, 'b'))

            if self.position.Z_getter() == 1:                              # front face blue
                self.faces.append(Face(self, self.img, 'f', face_color='b'))
            else:
                self.faces.append(Face(self, self.img, 'f'))

    def get_position(self):
        return self.position

    def set_parent(self, parent):
        self.parent = parent
    
    def set_world_parent(self, parent):
        self.world_parent = parent