import pytest
from cube_scrambler.core.generator import Generator
from cube_scrambler.core.notation_parser import NotationParser


@pytest.mark.parametrize("length", [10, 16, 20, 25])
def test_generator_sequence_length_and_valid_wca_tokens(length: int) -> None:
    generator = Generator(length=length)
    sequence = generator.generate_sequence()

    assert len(sequence) == length

    for move in sequence:
        assert not move.startswith("2"), f"Legacy prefix found in {move!r}"

    parsed = NotationParser.parse_sequence(generator.get_sequence_str())
    assert len(parsed) == length


@pytest.mark.parametrize("iteration", range(5))
def test_generator_avoids_consecutive_same_face_and_opposite_axis_triplets(
    iteration: int,
) -> None:
    generator = Generator(length=40)
    sequence = generator.generate_sequence()
    faces = [m.replace("'", "").replace("2", "") for m in sequence]

    for i in range(1, len(faces)):
        assert faces[i] != faces[i - 1], f"Duplicate consecutive move: {faces[i]}"

    for i in range(2, len(faces)):
        if faces[i] == Generator.OPPOSITES[faces[i - 1]]:
            assert (
                faces[i] != faces[i - 2]
            ), f"Redundant axis triplet: {faces[i-2]} {faces[i-1]} {faces[i]}"
