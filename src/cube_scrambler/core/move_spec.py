from dataclasses import dataclass

@dataclass(frozen=True)
class MoveSpec:
    """Immutable specification of a single 3D cube rotation step.

    Attributes:
        token: Original sanitized move string representation ("R'", "U2", ...).
        face: Primary face identifier ('U', 'D', 'R' ...).
        axis: Coordinate axis of rotation (X, Y, Z).
        layers: Tuple of layer coordinates along the axis to be rotated ((1,), (-1, 0)).
        direction: Direction of rotation multiplier (1 for clockwise, -1 for counter-clockwise).
        quarter_turns: Number of 90-degree rotations (1 for standard rotation, 2 for half-turns).
    """

    token: str
    face: str
    axis: str
    layers: tuple[int, ...]
    direction: int
    quarter_turns: int