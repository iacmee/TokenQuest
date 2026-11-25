import flask
import config
import sqlite3
from flask_wtf.csrf import CSRFError, CSRFProtect
from forms import LoginForm, RegistrationForm
from models import db, Question, QuizRound, User
from questions import INITIAL_QUESTIONS
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
from datetime import datetime
from statistics import mean

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
            conn.exec_driver_sql("BEGIN IMMEDIATE")
            db.metadata.create_all(conn)
            question_count = conn.scalar(db.select(db.func.count()).select_from(Question))
            if question_count < len(INITIAL_QUESTIONS):
                existing_texts = set(conn.scalars(db.select(Question.text)))
                missing_questions = [
                    {"text": text, "options": options, "correct_option": correct_option}
                    for text, options, correct_option in INITIAL_QUESTIONS
                    if text not in existing_texts
                ]
                if missing_questions:
                    conn.execute(Question.__table__.insert(), missing_questions)
            conn.commit()

except SQLAlchemyError as e:
    print(f"Database error: {e}")
    raise


def fetch_json_from_url(url: str, parameters: dict[str, Any]) -> Any:
    full_url = f"{url}?{urlencode(parameters)}"
    with urlopen(full_url, timeout=6) as response:
        return json.load(response)

def weather_from_city(city: str, days: int = config.DEFAULT_FORECAST_DAYS) -> dict | None:
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
            "hourly": "temperature_2m,is_day",
            "temperature_unit": "celsius",
            "forecast_days": days,
        }

        hourly = fetch_json_from_url(config.METEO_FORECAST_URL, params)["hourly"]
        temperatures_by_date = {}
        for timestamp, temperature, is_day in zip(
            hourly["time"], hourly["temperature_2m"], hourly["is_day"], strict=True):
            day = datetime.fromisoformat(timestamp).date()
            if day not in temperatures_by_date:
                temperatures_by_date[day] = {0: [], 1: []}
            # note that is_day is either 0 or 1
            temperatures = temperatures_by_date[day]
            if temperature is not None and is_day in temperatures:
                temperatures[is_day].append(temperature)

        daily_forecasts = []

        # it could be sorted because is a date obj
        for day, temperatures in sorted(temperatures_by_date.items()):
            daytime = temperatures[1]
            nighttime = temperatures[0]
            daily_forecasts.append({
                "label": config.WEEK_DAYS[day.weekday()],
                "date": day.strftime("%d/%m/%Y"),
                "day_temp": round(mean(daytime), 1) if daytime else None,
                "night_temp": round(mean(nighttime), 1) if nighttime else None,
            })
        return {'name': location['name'], 'country': location.get('country', ''), 'days': daily_forecasts}

    except Exception as e:
        logging.error("Unable to retrieve weather data for %s: %s", city, e)
        return None



@app.route('/')
def index() -> ResponseReturnValue:
    query = request.args.get("city")
    city = query.strip() if query is not None else ""
    days = request.args.get("days", type=int)
    weather = None
    error = None

    if "days" not in request.args:
        days = config.DEFAULT_FORECAST_DAYS
    elif days is None or not 1 <= days <= config.MAX_FORECAST_DAYS:
        error = f"Scegli da 1 a {config.MAX_FORECAST_DAYS} giorni."
        days = config.DEFAULT_FORECAST_DAYS

    if query is not None and error is None:
        if not 2 <= len(city) <= 100:
            error = "Inserisci un nome di città da 2 a 100 caratteri."
        else:
            weather = weather_from_city(city, days)
            if not weather or not weather["days"]:
                error = "Previsioni non disponibili. Controlla il nome della città o riprova più tardi."

    return flask.render_template(
        "index.html", city=city, days=days, max_days=config.MAX_FORECAST_DAYS,
        weather=weather, error=error,
    )

@app.route('/login', methods=['GET', 'POST'])
def login() -> ResponseReturnValue:

    form = LoginForm()
    if form.validate_on_submit(): # this function already verify that method is POST
        user = db.session.scalar(db.select(User).where(User.username == form.username.data))
        password_hash = user.password_hash if user is not None else config.DUMMY_USER_HASH
        if check_password_hash(password_hash, form.password.data) and user is not None:
            flask.session.clear()
            flask.session["user_id"] = user.id
            return flask.redirect(flask.url_for("index"), code=303)

        flask.flash("Username o password non validi.", "error")
        return flask.render_template("login.html", form=form), 401

    if form.is_submitted():
        status = 400
    else:
        200
    return flask.render_template("login.html", form=form), status



@app.post('/logout')
def logout() -> ResponseReturnValue:
    # no need to verify the request there, CSRFProtect was called
    flask.session.clear()
    return flask.redirect(flask.url_for("login"), code=303)

@app.route('/leaderboard')
def leaderboard() -> ResponseReturnValue:
    players = db.session.execute(
        db.select(User.nickname, User.score)
        .where(User.score > 0)
        .order_by(User.score.desc(), User.nickname)
    ).all()
    return flask.render_template("leaderboard.html", players=players)



@app.route("/quiz", methods=["GET", "POST"])
def quiz() -> ResponseReturnValue:

    user_id = flask.session.get("user_id")
    if user_id is None:
        return flask.redirect(flask.url_for("login"), code=303)

    try:
        if request.method == "POST":
            db.session.execute(db.text("BEGIN IMMEDIATE"))


        user = db.session.get(User, user_id)
        if user is None:
            flask.session.clear()
            return flask.redirect(flask.url_for("login"), code=303)

        quiz_round = db.session.get(QuizRound, user_id)
        finished = False
        question = None

        if quiz_round is not None:
            finished = quiz_round.position >= len(quiz_round.question_ids)
            if not finished:
                question_id = quiz_round.question_ids[quiz_round.position]
                question = db.get_or_404(Question, question_id)

        #  it's a GET so we render the page. with the resumed question or not
        if request.method == "GET":
            return flask.render_template(
                "quiz.html",
                user=user,
                quiz_round=quiz_round,
                finished=finished,
                question=question,
                pass_score=config.QUIZ_PASS_SCORE,
                round_size=config.QUIZ_ROUND_SIZE,
                points_per_pass=config.QUIZ_POINTS_PER_PASS,
            )

        # if it reach this point is a POST
        action = request.form.get("action")
        if action == "start":

            # can't start the quiz, need to end the pending one first
            if quiz_round is not None and not finished:
                return flask.redirect(flask.url_for("quiz"), code=303)

            question_ids = db.session.scalars(
                db.select(Question.id)
                .order_by(db.func.random())
                .limit(config.QUIZ_ROUND_SIZE)
            ).all()

            # if there is not enough questions in the db
            if len(question_ids) < config.QUIZ_ROUND_SIZE:
                flask.abort(503, description="Il quiz è temporaneamente non disponibile.")

            if quiz_round is None:
                quiz_round = QuizRound(user_id=user.id)
                db.session.add(quiz_round)

            quiz_round.question_ids = question_ids
            quiz_round.position = 0
            quiz_round.correct_answers = 0

        elif action == "answer":

            # if there is an answer but there is no quiz_round in the database redirect
            if quiz_round is None or question is None:
                return flask.redirect(flask.url_for("quiz"), code=303)

            # verify that the question_id from the request is the expected question_id from the quiz_round
            question_id = request.form.get("question_id", type=int)
            if question_id != question.id:
                return flask.redirect(flask.url_for("quiz"), code=303)

            # verify that the answer is coherent
            answer = request.form.get("answer", type=int)
            if answer is None or answer not in range(len(question.options)):
                flask.abort(400, description="Scegli una risposta valida.")

    
            if answer == question.correct_option:
                quiz_round.correct_answers += 1
                flask.flash("Risposta corretta.", "success")
            else:
                correct_answer = question.options[question.correct_option]
                flask.flash(f"Risposta errata. La risposta corretta era «{correct_answer}».", "error")


            quiz_round.position += 1
            if quiz_round.position == len(quiz_round.question_ids):
                if quiz_round.correct_answers >= config.QUIZ_PASS_SCORE:
                    user.score += config.QUIZ_POINTS_PER_PASS
        else: # if is a get with unknown action
            flask.abort(400, description="Azione non valida.")
        db.session.commit()
        return flask.redirect(flask.url_for("quiz"), code=303)

    finally:
        db.session.rollback()

@app.route('/register', methods=['GET', 'POST'])
def register() -> ResponseReturnValue:

    form = RegistrationForm()
    if form.validate_on_submit(): # this function already verify that method is POST
        user = User(
            username=form.username.data,
            nickname=form.nickname.data,
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
            conflicts = {
                "UNIQUE constraint failed: users.username": (form.username, "Username già in uso."),
                "UNIQUE constraint failed: users.email": (form.email, "Indirizzo email già in uso."),
                "UNIQUE constraint failed: users.nickname": (form.nickname, "Nickname già in uso."),
            }
            conflict = conflicts.get(str(error.orig))
            if conflict is None:
                raise
            field, message = conflict
            field.errors.append(message)
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
