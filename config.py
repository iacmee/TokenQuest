import secrets
from pathlib import Path

HOST="0.0.0.0"
PORT=5000
THREADS_NUM=8
LOGGING_FORMAT="%(asctime)s [%(levelname)s] %(message)s"

ROOT_PATH = Path(__file__).resolve().parent
DATABASE_DIR = ROOT_PATH / "data"
DATABASE_PATH = DATABASE_DIR / "app.sqlite"
SECRET_KEY_PATH = DATABASE_DIR / "secret_key"


DATABASE_DIR.mkdir(parents=True, exist_ok=True)


def load_secret_key() -> str:

    try:
        key = SECRET_KEY_PATH.read_text(encoding="utf-8").strip()
    except FileNotFoundError:

        key = secrets.token_hex(32)

        SECRET_KEY_PATH.write_text(key, encoding="utf-8")

    if not key:
        raise RuntimeError("data/secret_key file is empty. Delete the file and will be filled with a new key.")

    return key