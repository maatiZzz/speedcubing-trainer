from ursina import Entity, invoke, curve, Func, Wait
import ursina
from app.model.piece import Piece 

class Cube(Entity):
    def __init__(self, img, sq=''):
        super().__init__()

        self.origin = (0,0,0)
        self.img = img

        self.__init_pieces()

        self.sequence = sq

        self.is_rotating = False
        self.animation_speed = 0.5

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

    def change_speed(self, slider):
        self.animation_speed = slider.value

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
            face.animate_rotation_x(face.rotation_x + (direction * 90), duration= 1-self.animation_speed, curve=curve.in_out_sine)
        elif dimension == 'y':
            face.animate_rotation_y(face.rotation_y + (direction * 90), duration= 1-self.animation_speed, curve=curve.in_out_sine)
        elif dimension == 'z':
            face.animate_rotation_z(face.rotation_z + (direction * 90), duration=1-self.animation_speed, curve=curve.in_out_sine)

        invoke(self.reset_parenting, delay=1-self.animation_speed+0.1)
    
    def animate_sequence(self, sequence, slider, stop_button, animate_button):
        # self.sequence = 'U D L R F B U\' D\' L\' R\' F\' B\''
        moves_arr = self.sequence.split()
        for m in moves_arr:
            if m == 'L':
                sequence.append(Func(self.face_move, 'x', -1, -1))
            if m == 'R':
                sequence.append(Func(self.face_move, 'x', 1, 1))
            if m == 'U':
                sequence.append(Func(self.face_move, 'y', 1, 1))
            if m == 'D':
                sequence.append(Func(self.face_move, 'y', -1, -1))
            if m == 'F':
                sequence.append(Func(self.face_move, 'z', -1, 1))
            if m == 'B':
                sequence.append(Func(self.face_move, 'z', 1, -1))

            if m == '2L':
                sequence.append(Func(self.face_move, 'x', -1, -1))
                sequence.append(Wait(1-self.animation_speed + 0.2))
                sequence.append(Func(self.face_move, 'x', -1, -1))
            if m == '2R':
                sequence.append(Func(self.face_move, 'x', 1, 1))
                sequence.append(Wait(1-self.animation_speed + 0.2))
                sequence.append(Func(self.face_move, 'x', 1, 1))
            if m == '2U':
                sequence.append(Func(self.face_move, 'y', 1, 1))
                sequence.append(Wait(1-self.animation_speed + 0.2))
                sequence.append(Func(self.face_move, 'y', 1, 1))
            if m == '2D':
                sequence.append(Func(self.face_move, 'y', -1, -1))
                sequence.append(Wait(1-self.animation_speed + 0.2))
                sequence.append(Func(self.face_move, 'y', -1, -1))
            if m == '2F':
                sequence.append(Func(self.face_move, 'z', -1, 1))
                sequence.append(Wait(1-self.animation_speed + 0.2))
                sequence.append(Func(self.face_move, 'z', -1, 1))
            if m == '2B':
                sequence.append(Func(self.face_move, 'z', 1, -1))
                sequence.append(Wait(1-self.animation_speed + 0.2))
                sequence.append(Func(self.face_move, 'z', 1, -1))

            if m == 'R':
                sequence.append(Func(self.face_move, 'x', 1, 1))
            if m == 'L\'':
                sequence.append(Func(self.face_move, 'x', -1, 1))
            if m == 'R\'':
                sequence.append(Func(self.face_move, 'x', 1, -1))
            if m == 'U\'':
                sequence.append(Func(self.face_move, 'y', 1, -1))
            if m == 'D\'':
                sequence.append(Func(self.face_move, 'y', -1, 1))
            if m == 'F\'':
                sequence.append(Func(self.face_move, 'z', -1, -1))
            if m == 'B\'':
                sequence.append(Func(self.face_move, 'z', 1, 1))

            sequence.append(Wait(1-self.animation_speed + 0.2))

        slider.enabled = False
        stop_button.enabled = True
        animate_button.enabled = False
        sequence.start()

    def stop_animation(self, sequence):
        sequence.pause()

    def resume_animation(self, sequence, resume_button, stop_button):
        sequence.resume()
        resume_button.enabled = False
        resume_button.enabled = False
        stop_button.enabled = True

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
    
    def destroy_cube(self):
        for p in self.pieces:
            p.set_parent(self)
        ursina.destroy(self)