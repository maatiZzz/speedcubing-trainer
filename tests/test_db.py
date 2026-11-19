from pathlib import Path
import pytest
from cube_scrambler.data.storage.db import DBManager
from cube_scrambler.data.persistence.repository import AlgorithmRepository


@pytest.fixture
def db_manager(tmp_path: Path) -> DBManager:
    """Fixture providing an isolated DBManager connected to a temporary SQLite file."""
    db_file = tmp_path / "test_rubik.db"
    manager = DBManager(db_file)
    manager.create_table("algorithms")
    return manager


def test_db_manager_initial_state_is_empty(db_manager: DBManager) -> None:
    assert db_manager.check_if_empty("algorithms") is True


def test_db_manager_insert_and_fetch_with_single_quotes(
    db_manager: DBManager,
) -> None:
    sample_data = [
        ("F2L 1", "F R' F' R", "U R U' R'", "F2L"),
        ("F2L 2", "R' F R F'", "F R' F' R", "F2L"),
    ]
    db_manager.insert_data("algorithms", sample_data)

    assert db_manager.check_if_empty("algorithms") is False

    rows = db_manager.get_all_alg_data("algorithms", category="f2l")
    assert len(rows) == 2
    assert rows[0] == ("F2L 1", "F R' F' R", "U R U' R'", "F2L")
    assert rows[1] == ("F2L 2", "R' F R F'", "F R' F' R", "F2L")


@pytest.mark.parametrize("invalid_identifier", ["bad-table", "table;DROP TABLE test--", "123tbl", "tbl name"])
def test_db_manager_rejects_invalid_table_identifiers(
    db_manager: DBManager, invalid_identifier: str
) -> None:
    with pytest.raises(ValueError, match="Invalid SQL identifier"):
        db_manager.create_table(invalid_identifier)


def test_algorithm_repository_initializes_from_offline_seed(
    tmp_path: Path,
) -> None:
    db_path = tmp_path / "seeded_repo.db"
    repository = AlgorithmRepository(db_manager=DBManager(db_path))

    repository.initialize()

    algorithms = repository.get_all(category="F2L")
    assert len(algorithms) == 41
    assert algorithms[0].name == "F2L 1"
    assert algorithms[0].setup == "F R' F' R"
    assert algorithms[0].solution == "U R U' R'"
