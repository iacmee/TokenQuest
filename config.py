import secrets
from pathlib import Path
from werkzeug.security import generate_password_hash

HOST="0.0.0.0"
PORT=5000
THREADS_NUM=8
LOGGING_FORMAT="%(asctime)s [%(levelname)s] %(message)s"

METEO_COORDINATE_URL = "https://geocoding-api.open-meteo.com/v1/search"
METEO_FORECAST_URL = "https://api.open-meteo.com/v1/forecast"
FORECAST_DAYS = 3
WEEK_DAYS = ['Lunedì', 'Martedì', 'Mercoledì', 'Giovedì', 'Venerdì', 'Sabato', 'Domenica']

ROOT_PATH = Path(__file__).resolve().parent
DATABASE_DIR = ROOT_PATH / "data"
DATABASE_PATH = DATABASE_DIR / "app.sqlite"
SECRET_KEY_PATH = DATABASE_DIR / "secret_key"
DATABASE_DIR.mkdir(parents=True, exist_ok=True)

# used to spend time verifing the password. Against time-based attack
DUMMY_USER_HASH = generate_password_hash(secrets.token_hex(32))


USERNAME_MIN_LENGTH = 1
USERNAME_MAX_LENGTH = 80
EMAIL_MIN_LENGTH = 1
EMAIL_MAX_LENGTH = 254
PASSWORD_MIN_LENGTH = 10
PASSWORD_MAX_LENGTH = 128
LOGIN_USERNAME_MIN_LENGTH = 1
LOGIN_USERNAME_MAX_LENGTH = max(80, USERNAME_MAX_LENGTH)
LOGIN_PASSWORD_MIN_LENGTH = 1
LOGIN_PASSWORD_MAX_LENGTH = max(128, PASSWORD_MAX_LENGTH)


def load_secret_key() -> str:

    try:
        key = SECRET_KEY_PATH.read_text(encoding="utf-8").strip()
    except FileNotFoundError:

        key = secrets.token_hex(32)

        SECRET_KEY_PATH.write_text(key, encoding="utf-8")

    if not key:
        raise RuntimeError("data/secret_key file is empty. Delete the file and will be filled with a new key.")

    return key
