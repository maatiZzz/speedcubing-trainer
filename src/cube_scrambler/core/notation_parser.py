"""WCA notation parsing and move tokenization.

Provides parsing utilities for Rubik's cube notation, mapping human-readable
move tokens (e.g. 'R', "U'", 'F2') to spatial rotation specifications.
"""

from cube_scrambler.core.move_spec import MoveSpec


class NotationParser:
    """Parser for Rubik's WCA sequences to 3D rotation steps (represented by MoveSpec objects)."""

    BASE_MOVES: dict[str, tuple[str, tuple[int, ...], int]] = {
        "L": ("x", (-1,), -1),
        "R": ("x", (1,), 1),
        "U": ("y", (1,), 1),
        "D": ("y", (-1,), -1),
        "F": ("z", (-1,), 1),
        "B": ("z", (1,), -1),
        "l": ("x", (-1, 0), -1),        # double-layer moves
        "r": ("x", (0, 1), 1),
        "u": ("y", (0, 1), 1),
        "d": ("y", (-1, 0), -1),
        "f": ("z", (-1, 0), 1),
        "b": ("z", (0, 1), -1),
    }

    @classmethod
    def parse_move(cls, token: str) -> MoveSpec:
        """Parse a single WCA move token into a 3D rotation specification.

        Handles standard face turns, prime turns (counter-clockwise), double turns
        (both modern 'R2' and legacy '2R' prefix notation), and wide layer moves.

        Args:
            token: Raw move string token (e.g. "R", "U'", "F2", "r'").

        Returns:
            MoveSpec: Immutable dataclass containing move details.

        Raises:
            ValueError: If `token` is empty or contains an unrecognized move character.
        """
        cleaned = token.strip()
        if not cleaned:
            raise ValueError("Empty move token")

        quarter_turns = 1
        is_prime = "'" in cleaned

        if cleaned[0] == "2" and len(cleaned) > 1:
            quarter_turns = 2
            face_char = cleaned[1]
        else:
            face_char = cleaned[0]
            if "2" in cleaned[1:]:  # e.g. R2, L2
                quarter_turns = 2

        if face_char not in cls.BASE_MOVES:
            raise ValueError(f"Unsupported move token: {token!r}")

        axis, layers, base_dir = cls.BASE_MOVES[face_char]
        direction = -base_dir if is_prime else base_dir

        return MoveSpec(
            token=cleaned,
            face=face_char,
            axis=axis,
            layers=layers,
            direction=direction,
            quarter_turns=quarter_turns,
        )

    @classmethod
    def parse_sequence(cls, sequence_str: str) -> list[MoveSpec]:
        """Parse a sequence of moves into a list of MoveSpec objects.

        Args:
            sequence_str: Full sequence string, e.g. "R U R' U' R' F R2 U' R' U' R U R' F'".

        Returns:
            list[MoveSpec]: Ordered list of parsed MoveSpec objects. Returns an empty list
                if the input is empty or contains only whitespace.
        """
        if not sequence_str or not sequence_str.strip():
            return []

        return [cls.parse_move(tok) for tok in sequence_str.split() if tok.strip()]
