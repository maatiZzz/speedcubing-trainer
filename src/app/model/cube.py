from ursina import Entity, invoke, curve, Func, Sequence, Wait
from app.model.piece import Piece 
import numpy as np

class Cube(Entity):
    def __init__(self, img, sq):
        super().__init__()

        self.origin = (0,0,0)
        self.img = img

        self.__init_pieces()

        self.sequence = sq

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
            self.face_move('x', -1, -1)
        if key == 'r':
            self.face_move('x', 1, 1)
        if key == 'u':
            self.face_move('y', 1, 1)
        if key == 'd':
            self.face_move('y', -1, -1)
        if key == 'f':
            self.face_move('z', -1, 1)
        if key == 'b':
            self.face_move('z', 1, -1)
         
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

    def face_move(self, dimension, coord, direction):
        self.is_rotating = True

        face = self.__face_prepare(dimension, coord)

        if dimension == 'x':
            face.animate_rotation_x(face.rotation_x + (direction * 90), duration=0.3, curve=curve.in_out_sine)
        elif dimension == 'y':
            face.animate_rotation_y(face.rotation_y + (direction * 90), duration=0.3, curve=curve.in_out_sine)
        elif dimension == 'z':
            face.animate_rotation_z(face.rotation_z + (direction * 90), duration=0.3, curve=curve.in_out_sine)

        invoke(self.reset_parenting, delay=0.4)
    
    def animate_sequence(self):
        # self.sequence = 'U D L R F B U\' D\' L\' R\' F\' B\''
        moves_arr = self.sequence.split()
        print(moves_arr)
        s = Sequence()
        for m in moves_arr:
            if m == 'L':
                s.append(Func(self.face_move, 'x', -1, -1))
            if m == 'L\'':
                s.append(Func(self.face_move, 'x', -1, 1))
            if m == 'R':
                s.append(Func(self.face_move, 'x', 1, 1))
            if m == 'R\'':
                s.append(Func(self.face_move, 'x', 1, -1))
            if m == 'U':
                s.append(Func(self.face_move, 'y', 1, 1))
            if m == 'U\'':
                s.append(Func(self.face_move, 'y', 1, -1))
            if m == 'D':
                s.append(Func(self.face_move, 'y', -1, -1))
            if m == 'D\'':
                s.append(Func(self.face_move, 'y', -1, 1))
            if m == 'F':
                s.append(Func(self.face_move, 'z', -1, 1))
            if m == 'F\'':
                s.append(Func(self.face_move, 'z', -1, -1))
            if m == 'B':
                s.append(Func(self.face_move, 'z', 1, -1))
            if m == 'B\'':
                s.append(Func(self.face_move, 'z', 1, 1))

            s.append(Wait(0.5))

        s.start()

    def __get_dimension(self, dimension):
        if dimension == 'x':
            return 0
        elif dimension == 'y':
            return 1
        else:
            return 2
        
    def __get_face(self, dimension, coord):
        if dimension == 'x':
            if coord == 1:
                return self.r_face
            else:
                return self.l_face
        if dimension == 'y':
            if coord == 1:
                return self.u_face
            else:
                return self.d_face
        if dimension == 'z':
            if coord == 1:
                return self.b_face
            else:
                return self.f_face
        
    def __face_prepare(self, dimension, coord):
        int_dim = self.__get_dimension(dimension)
        face = self.__get_face(dimension, coord)        

        for p in self.pieces:
            if p.get_position()[int_dim] == coord:   
                p.set_parent(face)

        return face