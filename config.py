from pathlib import Path

HOST="0.0.0.0"
PORT=5000
THREADS_NUM=8
LOGGING_FORMAT="%(asctime)s [%(levelname)s] %(message)s"

ROOT_PATH = Path(__file__).resolve().parent
DATABASE_DIR = ROOT_PATH / "data"
DATABASE_PATH = DATABASE_DIR / "app.sqlite"


DATABASE_DIR.mkdir(parents=True, exist_ok=True)