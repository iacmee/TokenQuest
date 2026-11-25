import flask
import config
import database
from models import db, User
from sqlalchemy.exc import SQLAlchemyError
from waitress import serve
from flask import request, Response
import logging

logging.basicConfig(level=logging.INFO,format=config.LOGGING_FORMAT)

app = flask.Flask(__name__)
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

@app.route('/register')
def register():
    return flask.render_template("register.html")




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
