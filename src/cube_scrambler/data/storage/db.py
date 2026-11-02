import sqlite3
from collections.abc import Sequence
from pathlib import Path
from cube_scrambler.config import DB_PATH


class DBManager:
    """SQLite database manager with connection lifecycle and parameterized queries."""

    def __init__(self, db_path: Path | str = DB_PATH) -> None:
        self.db_path: Path = Path(db_path)

    @staticmethod
    def _validate_identifier(identifier: str) -> str:
        if not identifier.isidentifier():
            raise ValueError(f"Invalid SQL identifier: {identifier!r}")
        return identifier

    def _connect(self) -> sqlite3.Connection:
        return sqlite3.connect(self.db_path)

    def create_table(self, table_name: str = "algorithms") -> None:
        table = self._validate_identifier(table_name)
        with self._connect() as con:
            con.execute(
                f"""
                CREATE TABLE IF NOT EXISTS {table} (
                    name TEXT NOT NULL,
                    setup TEXT NOT NULL,
                    solution TEXT NOT NULL,
                    category TEXT NOT NULL
                )
                """
            )
            con.execute(
                f"CREATE INDEX IF NOT EXISTS idx_{table}_category ON {table}(category)"
            )

    def insert_data(
        self,
        table_name: str,
        obj_arr: Sequence[tuple[str, str, str, str]],
    ) -> None:
        table = self._validate_identifier(table_name)
        with self._connect() as con:
            con.executemany(
                f"INSERT INTO {table} (name, setup, solution, category) VALUES (?, ?, ?, ?)",
                obj_arr,
            )

    def check_if_empty(self, table_name: str = "algorithms") -> bool:
        table = self._validate_identifier(table_name)
        with self._connect() as con:
            row = con.execute(f"SELECT EXISTS(SELECT 1 FROM {table})").fetchone()
            return not bool(row and row[0])

    def get_all_alg_data(
        self,
        table_name: str = "algorithms",
        category: str | None = None,
    ) -> list[tuple[str, str, str, str]]:
        table = self._validate_identifier(table_name)
        with self._connect() as con:
            if category:
                cur = con.execute(
                    f"SELECT name, setup, solution, category FROM {table} WHERE UPPER(category) = UPPER(?)",
                    (category,),
                )
            else:
                cur = con.execute(
                    f"SELECT name, setup, solution, category FROM {table}"
                )
            return cur.fetchall()
