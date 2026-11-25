import flask
import config
import sqlite3
from flask_wtf.csrf import CSRFError, CSRFProtect
from forms import LoginForm, RegistrationForm
from models import db, User
from sqlalchemy.exc import IntegrityError, SQLAlchemyError
from werkzeug.security import check_password_hash, generate_password_hash
from waitress import serve
from flask import request, Response
import logging
from flask.typing import ResponseReturnValue
import json
from urllib.parse import urlencode
from urllib.request import urlopen
from typing import Any
from datetime import date

logging.basicConfig(level=logging.INFO,format=config.LOGGING_FORMAT)

app = flask.Flask(__name__)
app.config["SECRET_KEY"] = config.load_secret_key()
app.config["SQLALCHEMY_DATABASE_URI"] = f"sqlite:///{config.DATABASE_PATH}"
db.init_app(app)
CSRFProtect(app)

@app.errorhandler(CSRFError)
def handle_csrf_error(error: CSRFError) -> ResponseReturnValue:
    return "Sessione del modulo scaduta o non valida. Ricarica la pagina e riprova.", 400

try:
    with app.app_context():
        with db.engine.connect() as conn:
            conn.exec_driver_sql("PRAGMA journal_mode=WAL")

        db.create_all()

except SQLAlchemyError as e:
    print(f"Database error: {e}")
    raise


def fetch_json_from_url(url: str, parameters: dict[str, Any]) -> Any:
    full_url = f"{url}?{urlencode(parameters)}"
    with urlopen(full_url, timeout=6) as response:
        return json.load(response)

def weather_from_city(city : str) -> dict | None:
    params = {
        "name": city,
        "count": 1,
        "language": "it",
    }
    try:
        locations = fetch_json_from_url(config.METEO_COORDINATE_URL, params).get('results', [])
        if not locations:
            return None

        location = locations[0]

        params = {
            "latitude": location["latitude"],
            "longitude": location["longitude"],
            "timezone": location["timezone"],
            "daily": "temperature_2m_max,temperature_2m_min",
            "forecast_days": config.FORECAST_DAYS,
        }

        forecast = fetch_json_from_url(config.METEO_FORECAST_URL, params)
        forecast = forecast["daily"]
    
        dates = forecast["time"]
        max_temps = forecast["temperature_2m_max"]
        min_temps = forecast["temperature_2m_min"]

        days = []

        for day, max_temp, min_temp in zip(dates, max_temps, min_temps, strict=True):
            parsed = date.fromisoformat(day)
            days.append({
                "label": config.WEEK_DAYS[parsed.weekday()],
                "date": parsed.strftime("%d/%m/%Y"),
                "max_temp": max_temp,
                "min_temp": min_temp,
            })
        return {'name': location['name'], 'country': location.get('country', ''), 'days': days}

    except Exception as e:
        logging.error("Unable to retrieve weather data for %s: %s", city, e)
        return None



@app.route('/')
def index():
    return flask.render_template("index.html")

@app.route('/login', methods=['GET', 'POST'])
def login() -> ResponseReturnValue:

    form = LoginForm()
    if form.validate_on_submit(): # this function already verify that methos is POST
        user = db.session.scalar(db.select(User).where(User.username == form.username.data))
        password_hash = user.password_hash if user is not None else config.DUMMY_USER_HASH
        if check_password_hash(password_hash, form.password.data) and user is not None:
            flask.session.clear()
            flask.session["user_id"] = user.id
            return flask.redirect(flask.url_for("index"), code=303)

        flask.flash("Username o password non validi.", "error")
        return flask.render_template("login.html", form=form), 401

    status = 400 if form.is_submitted() else 200
    return flask.render_template("login.html", form=form), status



@app.post('/logout')
def logout() -> ResponseReturnValue:
    # no need to verify the request there, CSRFProtect was called
    flask.session.clear()
    return flask.redirect(flask.url_for("login"), code=303)

@app.route('/leaderboard')
def leaderboard() -> ResponseReturnValue:
    return flask.render_template("leaderboard.html")

@app.route('/quiz')
def quiz() -> ResponseReturnValue:
    return flask.render_template("quiz.html")

@app.route('/register', methods=['GET', 'POST'])
def register() -> ResponseReturnValue:

    form = RegistrationForm()
    if form.validate_on_submit(): # this function already verify that methos is POST
        user = User(
            username=form.username.data,
            email=form.email.data,
            password_hash=generate_password_hash(form.password.data),
        )
        db.session.add(user)

        try:
            db.session.commit()
        except IntegrityError as error:
            db.session.rollback()
            if getattr(error.orig, "sqlite_errorcode", None) != sqlite3.SQLITE_CONSTRAINT_UNIQUE:
                raise
            flask.flash("Username o indirizzo email già in uso.", "error")
            return flask.render_template("register.html", form=form), 409

        flask.flash("Account creato. Ora puoi accedere.", "success")
        return flask.redirect(flask.url_for("login"), code=303)

    status = 400 if form.is_submitted() else 200
    return flask.render_template("register.html", form=form), status




# log the request
@app.after_request
def log_request(response: Response) -> Response:

    app.logger.info(
        "%s - %s %s - %d",
        request.remote_addr,
        request.method,
        request.path,
        response.status_code
    )

    return response

if __name__ == "__main__":
    serve(app, host=config.HOST, port=config.PORT, threads=config.THREADS_NUM)
