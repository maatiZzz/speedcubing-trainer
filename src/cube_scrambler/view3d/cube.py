import ursina
from ursina import Entity, Func, Wait, curve, invoke
from cube_scrambler.core.notation_parser import NotationParser
from cube_scrambler.view3d.piece import Piece


class Cube(Entity):
    """3D Rubik's cube entity handling manual and sequenced rotations."""

    def __init__(self, sq: str = "") -> None:
        super().__init__()

        self.origin = (0, 0, 0)
        self.sequence: str = sq
        self.is_rotating: bool = False
        self.animation_speed: float = 0.5

        self.pivot = Entity(parent=self)
        self.pieces: list[Piece] = []
        self._init_pieces()

    def _init_pieces(self) -> None:
        for x in range(-1, 2):
            for y in range(-1, 2):
                for z in range(-1, 2):
                    if x == 0 and y == 0 and z == 0:
                        continue
                    self.pieces.append(Piece(x, y, z))


    def change_speed(self, slider: object) -> None:
        self.animation_speed = slider.value

    def input(self, key: str) -> None:
        if self.is_rotating:
            return

        manual_moves: dict[str, tuple[str, tuple[int, ...], int]] = {
            "l": ("x", (-1,), -1),
            "r": ("x", (1,), 1),
            "u": ("y", (1,), 1),
            "d": ("y", (-1,), -1),
            "f": ("z", (-1,), 1),
            "b": ("z", (1,), -1),
        }
        if key in manual_moves:
            dim, layers, direction = manual_moves[key]
            self.face_move(dim, layers, direction, use_invoke=True)

    def reset_parenting(self) -> None:
        """Detach pieces from pivot and snap positions to integer grid."""
        for piece in self.pieces:
            # re-parent back to cube, keeping current world transform
            piece.set_world_parent(self)
            # snap position to grid (-1, 0, 1) to prevent float drift
            piece.x = round(piece.x)
            piece.y = round(piece.y)
            piece.z = round(piece.z)
            # snap angles to clean 90-degree multiples
            piece.rotation_x = round(piece.rotation_x / 90) * 90
            piece.rotation_y = round(piece.rotation_y / 90) * 90
            piece.rotation_z = round(piece.rotation_z / 90) * 90

        # reset pivot angle back to origin for next turn
        self.pivot.rotation = (0, 0, 0)
        self.is_rotating = False

    def face_move(
        self,
        dimension: str,
        layers: tuple[int, ...] | int,
        direction: int,
        use_invoke: bool = False,
    ) -> None:
        self.is_rotating = True
        layer_tuple = (layers,) if isinstance(layers, int) else layers
        self._prepare_pivot(dimension, layer_tuple)

        duration = max(0.05, 1.0 - self.animation_speed)
        if dimension == "x":
            self.pivot.animate_rotation_x(
                self.pivot.rotation_x + (direction * 90),
                duration=duration,
                curve=curve.in_out_sine,
            )
        elif dimension == "y":
            self.pivot.animate_rotation_y(
                self.pivot.rotation_y + (direction * 90),
                duration=duration,
                curve=curve.in_out_sine,
            )
        elif dimension == "z":
            self.pivot.animate_rotation_z(
                self.pivot.rotation_z + (direction * 90),
                duration=duration,
                curve=curve.in_out_sine,
            )

        if use_invoke:
            invoke(self.reset_parenting, delay=duration + 0.05)

    def animate_sequence(
        self,
        sequence: ursina.Sequence,
        slider: object,
        stop_button: object,
        animate_button: object,
    ) -> None:
        self.change_speed(slider)
        move_specs = NotationParser.parse_sequence(self.sequence)
        if not move_specs:
            return

        duration = max(0.05, 1.0 - self.animation_speed)
        for spec in move_specs:
            for _ in range(spec.quarter_turns):
                sequence.append(
                    Func(
                        self.face_move,
                        spec.axis,
                        spec.layers,
                        spec.direction,
                        False,
                    )
                )
                sequence.append(Wait(duration + 0.05))
                sequence.append(Func(self.reset_parenting))
                sequence.append(Wait(0.05))

        slider.enabled = False
        stop_button.enabled = True
        animate_button.enabled = False
        sequence.start()

    def stop_animation(self, sequence: ursina.Sequence) -> None:
        sequence.pause()

    def resume_animation(
        self,
        sequence: ursina.Sequence,
        resume_button: object,
        stop_button: object,
        reset_button: object | None = None,
    ) -> None:
        sequence.resume()
        resume_button.enabled = False
        if reset_button is not None:
            reset_button.enabled = False
        stop_button.enabled = True

    @staticmethod
    def _axis_index(dimension: str) -> int:
        if dimension == "x":
            return 0
        if dimension == "y":
            return 1
        return 2

    def _prepare_pivot(self, dimension: str, layers: tuple[int, ...]) -> None:
        """Attach pieces in target layers to pivot entity for rotation."""
        # ensure previous rotation is fully baked before new move
        self.reset_parenting()
        axis_idx = self._axis_index(dimension)

        for piece in self.pieces:
            coord = round(piece.get_position()[axis_idx])
            if coord in layers:
                piece.set_parent(self.pivot)


    def destroy_cube(self) -> None:
        for piece in self.pieces:
            piece.destroy_piece()
        ursina.destroy(self.pivot)
        ursina.destroy(self)
