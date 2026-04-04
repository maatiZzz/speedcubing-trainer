import ursina as ur
from ursina import Texture

class Face(ur.Entity):
    def __init__(self, parent, img, type, face_color = 'black'):
        super().__init__(parent = parent)

        self.texture = Texture(img)
        self.texture.filtering = 'point'        # avoid blurring collors
        self.type = type
        self.__set_color(face_color)
        self.__init_mesh()

    def __set_color(self, face_color):
        match face_color:
            case 'b':
                self.u_start = 0
                self.u_end = 1/7
            case 'o':
                self.u_start = 1/7
                self.u_end = 2/7
            case 'g':
                self.u_start = 2/7
                self.u_end = 3/7
            case 'r':
                self.u_start = 3/7
                self.u_end = 4/7
            case 'y':
                self.u_start = 4/7
                self.u_end = 5/7
            case 'w':
                self.u_start = 5/7
                self.u_end = 6/7
            case 'black':
                self.u_start = 6/7
                self.u_end = 6.99/7
        

    def __init_mesh(self):
        # each face has 4 unique vertices 
        vertices = self.__pick_vertices()

        # order of connecting triangles
        triangles = [
            (0,1,2),
            (2,3,0)
        ]

        # coordinates of texture - color picking
        uvs = [
            ur.Vec2(self.u_start, 0),
            ur.Vec2(self.u_start, 1),
            ur.Vec2(self.u_end, 1),
            ur.Vec2(self.u_end, 0),
        ]

        self.model = ur.Mesh(vertices = vertices, triangles = triangles, uvs = uvs)

    def __pick_vertices(self):
        match self.type:
            case 'f':                  # front face
                vertices = [
                    ur.Vec3(-0.5, -0.5, 0.5),   # left-down
                    ur.Vec3(-0.5, 0.5, 0.5),    # left-up
                    ur.Vec3(0.5, 0.5, 0.5),     # right-up
                    ur.Vec3(0.5, -0.5, 0.5),    # right-down
                ]
            case 'b':                  # back face
                vertices = [
                    ur.Vec3(0.5, -0.5, -0.5),   # left-down
                    ur.Vec3(0.5, 0.5, -0.5),    # left-up
                    ur.Vec3(-0.5, 0.5, -0.5),     # right-up
                    ur.Vec3(-0.5, -0.5, -0.5),    # right-down
                ]
            case 'l':                  # left face
                vertices = [
                    ur.Vec3(-0.5, -0.5, -0.5),   # left-down
                    ur.Vec3(-0.5, 0.5, -0.5),    # left-up
                    ur.Vec3(-0.5, 0.5, 0.5),     # right-up
                    ur.Vec3(-0.5, -0.5, 0.5),    # right-down
                ]
            case 'r':                  # right face
                vertices = [
                    ur.Vec3(0.5, -0.5, 0.5),   # left-down
                    ur.Vec3(0.5, 0.5, 0.5),    # left-up
                    ur.Vec3(0.5, 0.5, -0.5),     # right-up
                    ur.Vec3(0.5, -0.5, -0.5),    # right-down
                ]
            case 'u':                  # up face
                vertices = [
                    ur.Vec3(-0.5, 0.5, 0.5),   # left-down
                    ur.Vec3(-0.5, 0.5, -0.5),    # left-up
                    ur.Vec3(0.5, 0.5, -0.5),     # right-up
                    ur.Vec3(0.5, 0.5, 0.5),    # right-down
                ]
            case 'd':                  # down face
                vertices = [
                    ur.Vec3(0.5, -0.5, 0.5),   # left-down
                    ur.Vec3(0.5, -0.5, -0.5),    # left-up
                    ur.Vec3(-0.5, -0.5, -0.5),     # right-up
                    ur.Vec3(-0.5, -0.5, 0.5),    # right-down
                ]
        return vertices
        