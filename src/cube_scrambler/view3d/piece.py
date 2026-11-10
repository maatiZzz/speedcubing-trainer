import ursina as ur
from cube_scrambler.view3d.face import Face


class Piece(ur.Entity):
    """Single piece composed of 6 batched face objects."""

    def __init__(self, pos_x: int, pos_y: int, pos_z: int) -> None:
        super().__init__()
        self.scale = (0.95, 0.95, 0.95)
        self.origin = (0, 0, 0)
        self.position = ur.Vec3(pos_x, pos_y, pos_z)
        # reuse shared texture for piece mesh
        self.texture = Face.get_texture()

        self.faces: list[Face] = []
        self._init_faces(pos_x, pos_y, pos_z)

        if self.faces:
            self.combine()

    def _init_faces(self, pos_x: int, pos_y: int, pos_z: int) -> None:
        # skip center cubie
        if pos_x == 0 and pos_y == 0 and pos_z == 0:
            return

        self.faces.append(
            Face(self, "l", face_color="r" if pos_x == -1 else "black")
        )
        self.faces.append(
            Face(self, "r", face_color="o" if pos_x == 1 else "black")
        )
        self.faces.append(
            Face(self, "d", face_color="w" if pos_y == -1 else "black")
        )
        self.faces.append(
            Face(self, "u", face_color="y" if pos_y == 1 else "black")
        )
        self.faces.append(
            Face(self, "b", face_color="g" if pos_z == -1 else "black")
        )
        self.faces.append(
            Face(self, "f", face_color="b" if pos_z == 1 else "black")
        )

    def get_position(self) -> ur.Vec3:
        return self.position

    def set_parent(self, parent: ur.Entity) -> None:
        self.parent = parent

    def set_world_parent(self, parent: ur.Entity) -> None:
        self.world_parent = parent

    def destroy_piece(self) -> None:
        for face in self.faces:
            ur.destroy(face)
        ur.destroy(self)
