import flask
import config
import database
from waitress import serve
from paste.translogger import TransLogger
from flask import request, Response
import logging

logging.basicConfig(level=logging.INFO,format=config.LOGGING_FORMAT)

app = flask.Flask(__name__)
database.init(app)

@app.route('/')
def index():
    return flask.render_template("index.html")

@app.route('/login')
def login():
    return flask.render_template("login.html")




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