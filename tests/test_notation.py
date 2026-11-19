import pytest
from cube_scrambler.core.notation_parser import NotationParser


@pytest.mark.parametrize(
    ("token", "expected_axis", "expected_layers", "expected_dir", "expected_turns"),
    [
        ("R", "x", (1,), 1, 1),
        ("R'", "x", (1,), -1, 1),
        ("L", "x", (-1,), -1, 1),
        ("L'", "x", (-1,), 1, 1),
        ("U", "y", (1,), 1, 1),
        ("U'", "y", (1,), -1, 1),
        ("D", "y", (-1,), -1, 1),
        ("D'", "y", (-1,), 1, 1),
        ("F", "z", (-1,), 1, 1),
        ("F'", "z", (-1,), -1, 1),
        ("B", "z", (1,), -1, 1),
        ("B'", "z", (1,), 1, 1),
    ],
)
def test_parse_standard_moves(
    token: str,
    expected_axis: str,
    expected_layers: tuple[int, ...],
    expected_dir: int,
    expected_turns: int,
) -> None:
    move = NotationParser.parse_move(token)
    assert move.axis == expected_axis
    assert move.layers == expected_layers
    assert move.direction == expected_dir
    assert move.quarter_turns == expected_turns


@pytest.mark.parametrize(
    ("token", "expected_axis", "expected_layers", "expected_dir", "expected_turns"),
    [
        ("U2", "y", (1,), 1, 2),
        ("U2'", "y", (1,), -1, 2),
        ("R2", "x", (1,), 1, 2),
        ("R2'", "x", (1,), -1, 2),
        ("2F", "z", (-1,), 1, 2),
    ],
)
def test_parse_double_moves_and_legacy_prefix(
    token: str,
    expected_axis: str,
    expected_layers: tuple[int, ...],
    expected_dir: int,
    expected_turns: int,
) -> None:
    move = NotationParser.parse_move(token)
    assert move.axis == expected_axis
    assert move.layers == expected_layers
    assert move.direction == expected_dir
    assert move.quarter_turns == expected_turns


def test_parse_sequence_preserves_order() -> None:
    sequence_str = "R U R' U2' F R' F' R"
    specs = NotationParser.parse_sequence(sequence_str)

    assert len(specs) == 8
    assert [s.face for s in specs] == ["R", "U", "R", "U", "F", "R", "F", "R"]


@pytest.mark.parametrize("invalid_token", ["", "  ", "X", "Z9", "Q'"])
def test_parse_move_raises_value_error_on_invalid_input(invalid_token: str) -> None:
    with pytest.raises(ValueError):
        NotationParser.parse_move(invalid_token)
