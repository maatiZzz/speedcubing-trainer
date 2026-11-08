import json
from dataclasses import dataclass
from pathlib import Path
from cube_scrambler.config import ALGORITHMS_SEED_PATH, DB_PATH
from cube_scrambler.data.storage.db import DBManager
from cube_scrambler.data.scraper import AlgorithmScraper
from cube_scrambler.data.persistence.algorithm import Algorithm

class AlgorithmRepository:
    """Repository providing offline-first access to algorithms."""

    TABLE_NAME: str = "algorithms"

    def __init__(
        self,
        db_manager: DBManager | None = None,
        seed_path: Path = ALGORITHMS_SEED_PATH,
    ) -> None:
        self.db: DBManager = db_manager or DBManager(DB_PATH)
        self.seed_path: Path = seed_path

    def initialize(self) -> None:
        """Create schema and populate from local JSON seed (or scraper fallback) if empty."""
        self.db.create_table(self.TABLE_NAME)
        if self.db.check_if_empty(self.TABLE_NAME):
            if self.seed_path.is_file():
                self._seed_from_json()
            else:
                self.sync_from_scraper("F2L")

    def _seed_from_json(self) -> None:
        raw_items = json.loads(self.seed_path.read_text(encoding="utf-8"))
        records = [
            (
                item["name"],
                item["setup"],
                item["solution"],
                item.get("category", "F2L").upper(),
            )
            for item in raw_items
        ]
        if records:
            self.db.insert_data(self.TABLE_NAME, records)

    def sync_from_scraper(self, category: str = "F2L") -> int:
        scraper = AlgorithmScraper()
        scraper.get_response()
        scraper.parse_html()
        scraper.scrape_algorithms(category.upper())
        scraped = scraper.get_scraped_obj()
        if scraped:
            self.db.insert_data(self.TABLE_NAME, scraped)
        return len(scraped)

    def get_all(self, category: str | None = None) -> list[Algorithm]:
        rows = self.db.get_all_alg_data(self.TABLE_NAME, category=category)
        return [
            Algorithm(name=r[0], setup=r[1], solution=r[2], category=r[3])
            for r in rows
        ]
