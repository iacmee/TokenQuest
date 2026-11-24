import flask
import config
import database
from waitress import serve
from paste.translogger import TransLogger
from flask import request, Response
import logging

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s"
)

app = flask.Flask(__name__)
database.init(app)

@app.route('/')
def index():
    return "HELLO WORLD"

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