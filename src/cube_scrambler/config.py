from pathlib import Path

PACKAGE_DIR: Path = Path(__file__).resolve().parent
SRC_DIR: Path = PACKAGE_DIR.parent
PROJECT_ROOT: Path = SRC_DIR.parent

ASSETS_DIR: Path = PROJECT_ROOT / "assets"
DATA_DIR: Path = ASSETS_DIR / ("data"
                               "")
ALGORITHMS_SEED_PATH: Path = DATA_DIR / "algorithms.json"
CUBE_TEXTURE_PATH: Path = ASSETS_DIR / "cube-colors" / "cube-colors.png"
ICON_PATH: Path = ASSETS_DIR / "icon" / "icon.ico"
DB_PATH: Path = PROJECT_ROOT / "rubik.db"

ROOT_WINDOW_HEIGHT: int = 800
ROOT_WINDOW_WIDTH: int = 1400
LEARN_WINDOW_HEIGHT: int = 800
LEARN_WINDOW_WIDTH: int = 800

DOUBLE_MOVE_CHANCE: float = 0.3
BACKWARD_MOVE_CHANCE: float = 0.3
CASUAL_MOVE_CHANCE: float = 0.4

SCRAMBLE_SEQUENCE_LENGTH: int = 16
