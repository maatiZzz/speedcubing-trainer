import ursina as ur
from ursina import Texture
from cube_scrambler.config import CUBE_TEXTURE_PATH


class Face(ur.Entity):
    """Single face of a rubik's cube piece."""

    shared_texture: Texture | None = None

    def __init__(
        self,
        parent: ur.Entity,
        face_type: str,
        face_color: str = "black",
    ) -> None:
        """Create face entity with texture and mesh."""
        super().__init__(parent=parent)

        self._init_texture()
        self.texture = self.get_texture()
        self.type = face_type
        self._set_color(face_color)
        self._init_mesh()

    @classmethod
    def _init_texture(cls) -> None:
        if cls.shared_texture is None:
            cls.shared_texture = Texture(CUBE_TEXTURE_PATH)
            # point filtering keeps colors sharp without blur
            cls.shared_texture.filtering = "point"

    @classmethod
    def get_texture(cls) -> Texture:
        if cls.shared_texture is None:
            cls._init_texture()
        return cls.shared_texture

    def _set_color(self, face_color: str) -> None:
        """Pick horizontal texture coordinates for the face color (/assets/cube-colors)."""
        match face_color:
            case "b":
                self.u_start, self.u_end = 0.0, 1 / 7
            case "o":
                self.u_start, self.u_end = 1 / 7, 2 / 7
            case "g":
                self.u_start, self.u_end = 2 / 7, 3 / 7
            case "r":
                self.u_start, self.u_end = 3 / 7, 4 / 7
            case "y":
                self.u_start, self.u_end = 4 / 7, 5 / 7
            case "w":
                self.u_start, self.u_end = 5 / 7, 6 / 7
            case _:
                # black for hidden/internal faces
                self.u_start, self.u_end = 6 / 7, 6.99 / 7

    def _init_mesh(self) -> None:
        """Build mesh from 4 vertices and UV map."""
        vertices = self._pick_vertices()

        triangles = [(0, 1, 2), (2, 3, 0)]
        # map 4 vertices to color strip in texture (bottom-left to top-right)
        uvs = [
            ur.Vec2(self.u_start, 0),
            ur.Vec2(self.u_start, 1),
            ur.Vec2(self.u_end, 1),
            ur.Vec2(self.u_end, 0),
        ]
        self.model = ur.Mesh(vertices=vertices, triangles=triangles, uvs=uvs)

    def _pick_vertices(self) -> list[ur.Vec3]:
        """Return 4 corner vertices for the face in local 3D space."""
        # piece dimensions are 1x1x1 (-0.5 to 0.5 on x, y, z)
        # vertices are in counter-clockwise order so normals face outward
        match self.type:
            case "f":
                # front face at z = +0.5
                return [
                    ur.Vec3(-0.5, -0.5, 0.5),  # bottom-left
                    ur.Vec3(-0.5, 0.5, 0.5),   # top-left
                    ur.Vec3(0.5, 0.5, 0.5),    # top-right
                    ur.Vec3(0.5, -0.5, 0.5),   # bottom-right
                ]
            case "b":
                # back face at z = -0.5
                return [
                    ur.Vec3(0.5, -0.5, -0.5),  # bottom-left
                    ur.Vec3(0.5, 0.5, -0.5),   # top-left
                    ur.Vec3(-0.5, 0.5, -0.5),  # top-right
                    ur.Vec3(-0.5, -0.5, -0.5), # bottom-right
                ]
            case "l":
                # left face at x = -0.5
                return [
                    ur.Vec3(-0.5, -0.5, -0.5),  # bottom-left
                    ur.Vec3(-0.5, 0.5, -0.5),   # top-left
                    ur.Vec3(-0.5, 0.5, 0.5),    # top-right
                    ur.Vec3(-0.5, -0.5, 0.5),   # bottom-right
                ]
            case "r":
                # right face at x = +0.5
                return [
                    ur.Vec3(0.5, -0.5, 0.5),   # bottom-left
                    ur.Vec3(0.5, 0.5, 0.5),    # top-left
                    ur.Vec3(0.5, 0.5, -0.5),   # top-right
                    ur.Vec3(0.5, -0.5, -0.5),  # bottom-right
                ]
            case "u":
                # up/top face at y = +0.5
                return [
                    ur.Vec3(-0.5, 0.5, 0.5),   # bottom-left
                    ur.Vec3(-0.5, 0.5, -0.5),  # top-left
                    ur.Vec3(0.5, 0.5, -0.5),   # top-right
                    ur.Vec3(0.5, 0.5, 0.5),    # bottom-right
                ]
            case "d":
                # down/bottom face at y = -0.5
                return [
                    ur.Vec3(0.5, -0.5, 0.5),   # bottom-left
                    ur.Vec3(0.5, -0.5, -0.5),  # top-left
                    ur.Vec3(-0.5, -0.5, -0.5), # top-right
                    ur.Vec3(-0.5, -0.5, 0.5),  # bottom-right
                ]
            case _:
                raise ValueError(f"Unknown face type: {self.type!r}")

