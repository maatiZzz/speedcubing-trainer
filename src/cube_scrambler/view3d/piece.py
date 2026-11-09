import ursina as ur
from ursina import Texture
from cube_scrambler.view3d.face import Face


class Piece(ur.Entity):
    """Single piece composed of 6 batched face objects."""

    def __init__(self, pos_x: int, pos_y: int, pos_z: int, img: object) -> None:
        super().__init__()
        self.scale = (0.95, 0.95, 0.95)
        self.origin = (0, 0, 0)
        self.position = ur.Vec3(pos_x, pos_y, pos_z)
        self.img = img

        self.texture = Texture(self.img)
        self.texture.filtering = None

        self.faces: list[Face] = []
        self._init_faces(pos_x, pos_y, pos_z)

        if self.faces:
            self.combine()

    def _init_faces(self, pos_x: int, pos_y: int, pos_z: int) -> None:
        if pos_x == 0 and pos_y == 0 and pos_z == 0:
            return

        self.faces.append(
            Face(self, self.img, "l", face_color="r" if pos_x == -1 else "black")
        )
        self.faces.append(
            Face(self, self.img, "r", face_color="o" if pos_x == 1 else "black")
        )
        self.faces.append(
            Face(self, self.img, "d", face_color="w" if pos_y == -1 else "black")
        )
        self.faces.append(
            Face(self, self.img, "u", face_color="y" if pos_y == 1 else "black")
        )
        self.faces.append(
            Face(self, self.img, "b", face_color="g" if pos_z == -1 else "black")
        )
        self.faces.append(
            Face(self, self.img, "f", face_color="b" if pos_z == 1 else "black")
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
