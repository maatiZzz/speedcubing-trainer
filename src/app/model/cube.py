from ursina import Entity, invoke, curve
from app.model.piece import Piece 
import numpy as np

class Cube(Entity):
    def __init__(self, img):
        super().__init__()

        self.origin = (0,0,0)
        self.img = img

        self.__init_pieces()

        self.is_rotating = False

    def __init_pieces(self):
        self.pieces = []
        self.l_face = Entity()
        self.r_face = Entity()
        self.b_face = Entity()
        self.f_face = Entity()
        self.u_face = Entity()
        self.d_face = Entity()

        for x in range(-1, 2):
            for y in range(-1, 2):
                for z in range(-1, 2):
                    self.pieces.append(Piece(x, y, z, self.img))

    def input(self, key):
        if self.is_rotating:
            return

        if key == 'l':
            for p in self.pieces:
                if p.get_position()[0] == -1:
                    p.set_parent(self.l_face)
            self.face_move(self.l_face, 'x', -1)
        if key == 'r':
            for p in self.pieces:
                if p.get_position()[0] == 1:   
                    p.set_parent(self.r_face)
            self.face_move(self.r_face, 'x', 1)
        if key == 'u':
            for p in self.pieces:
                if p.get_position()[1] == 1:   
                    p.set_parent(self.u_face)
            self.face_move(self.u_face, 'y', 1)
        if key == 'd':
            for p in self.pieces:
                if p.get_position()[1] == -1:   
                    p.set_parent(self.d_face)
            self.face_move(self.d_face, 'y', -1)
        if key == 'f':
            for p in self.pieces:
                if p.get_position()[2] == -1:   
                    p.set_parent(self.f_face)
            self.face_move(self.f_face, 'z', 1)
        if key == 'b':
            for p in self.pieces:
                if p.get_position()[2] == 1:   
                    p.set_parent(self.b_face)
            self.face_move(self.b_face, 'z', -1)
         


    def reset_parenting(self):
        for p in self.pieces:
            p.set_world_parent(self)
            p.x = round(p.x)
            p.y = round(p.y)
            p.z = round(p.z)
            p.rotation_x = round(p.rotation_x / 90) * 90
            p.rotation_y = round(p.rotation_y / 90) * 90
            p.rotation_z = round(p.rotation_z / 90) * 90
        
        self.l_face.rotation_x = 0
        self.r_face.rotation_x = 0
        self.d_face.rotation_y = 0
        self.u_face.rotation_y = 0
        self.b_face.rotation_z = 0
        self.f_face.rotation_z = 0

        self.is_rotating = False

    def face_move(self, face, dimension, direction):
        self.is_rotating = True

        if dimension == 'x':
            face.animate_rotation_x(face.rotation_x + (direction * 90), duration=0.3)
        elif dimension == 'y':
            face.animate_rotation_y(face.rotation_y + (direction * 90), duration=0.3)
        elif dimension == 'z':
            face.animate_rotation_z(face.rotation_z + (direction * 90), duration=0.3)

        invoke(self.reset_parenting, delay=0.4)
      