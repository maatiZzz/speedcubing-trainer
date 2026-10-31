"""Random WCA-compliant scramble sequence generator for 3x3x3 Rubik's cube."""

import random

from cube_scrambler.config import (
    BACKWARD_MOVE_CHANCE,
    CASUAL_MOVE_CHANCE,
    DOUBLE_MOVE_CHANCE,
    SCRAMBLE_SEQUENCE_LENGTH,
)

class Generator:
    """Generates random WCA-style scramble move sequences.

    Enforces standard speedcubing constraints:
    1. No consecutive moves on the same face (e.g. 'R R').
    2. No redundant 3-move sequences on opposite faces along the same axis (e.g. 'R L R').
    3. Proper WCA suffix notation ('R2', "R'", 'R') instead of legacy prefix notation ('2R').

    Attributes:
        moves: List of valid 3x3 face characters ('U', 'D', 'R', 'L', 'F', 'B').
        length: Desired number of moves in the generated scramble sequence.
        sequence: The most recently generated sequence of move tokens.
    """

    OPPOSITES: dict[str, str] = {
        "L": "R",
        "R": "L",
        "U": "D",
        "D": "U",
        "F": "B",
        "B": "F",
    }

    def __init__(self, length: int = SCRAMBLE_SEQUENCE_LENGTH) -> None:
        """Initialize the scramble generator.

        Args:
            length: Sequence length in number of moves. Defaults to SCRAMBLE_SEQUENCE_LENGTH.
        """
        self.moves: list[str] = ["U", "D", "R", "L", "F", "B"]
        self.length: int = length
        self.sequence: list[str] = []

    @staticmethod
    def _base_face(move: str) -> str:
        """Strip modifier characters (' and 2) to extract the primary face identifier.

        Returns:
            str: Single character face identifier (e.g. "R", "U", "F").
        """
        return move.replace("'", "").replace("2", "")

    def generate_sequence(self) -> list[str]:
        """Generate a new random scramble sequence satisfying WCA validity constraints.

        Returns:
            list[str]: Newly generated list of move token strings.
        """
        sequence: list[str] = []
        last_move: str | None = None
        last_last_move: str | None = None

        while len(sequence) < self.length:
            random_move = random.choice(self.moves)

            if sequence:
                last_move = self._base_face(sequence[-1])
                if len(sequence) > 1:
                    last_last_move = self._base_face(sequence[-2])

            if (
                last_move
                and random_move == last_move
                and random_move == self.OPPOSITES[last_move]
            ):
                continue

            if (
                last_last_move
                and last_move
                and random_move == last_last_move
            ):
                continue

            modifier = random.choices(
                ["'", "2", ""],
                weights=[BACKWARD_MOVE_CHANCE, DOUBLE_MOVE_CHANCE, CASUAL_MOVE_CHANCE],
                k=1,
            )[0]
            sequence.append(f"{random_move}{modifier}")

        self.sequence = sequence
        return self.sequence

    def get_sequence(self) -> list[str]:
        """Return a copy of the current sequence list.

        Returns:
            list[str]: List of move tokens in the current sequence.
        """
        return list(self.sequence)

    def get_sequence_str(self) -> str:
        """Return the current sequence formatted as a space-separated string for display.

        Returns:
            str: Move tokens separated by 3 spaces (e.g. "R   U'   F2   D").
        """
        return "   ".join(self.sequence)
