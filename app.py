import flask
import config
from forms import RegistrationForm
from models import db, User
from sqlalchemy.exc import IntegrityError, SQLAlchemyError
from werkzeug.security import generate_password_hash
from waitress import serve
from flask import request, Response
import logging

logging.basicConfig(level=logging.INFO,format=config.LOGGING_FORMAT)

app = flask.Flask(__name__)
app.config["SECRET_KEY"] = config.load_secret_key()
app.config["SQLALCHEMY_DATABASE_URI"] = f"sqlite:///{config.DATABASE_PATH}"
db.init_app(app)

try:
    with app.app_context():
        with db.engine.connect() as conn:
            conn.exec_driver_sql("PRAGMA journal_mode=WAL")

        db.create_all()

except SQLAlchemyError as e:
    print(f"Database error: {e}")
    raise

@app.route('/')
def index():
    return flask.render_template("index.html")

@app.route('/login')
def login():
    return flask.render_template("login.html")

@app.route('/leaderboard')
def leaderboard():
    return flask.render_template("leaderboard.html")

@app.route('/quiz')
def quiz():
    return flask.render_template("quiz.html")

@app.route('/register', methods=['GET', 'POST'])
def register():

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
