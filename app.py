import flask
import config
import database
from waitress import serve

app = flask.Flask(__name__)
database.init(app)

@app.route('/')
def index():
    return "HELLO WORLD"


if __name__ == "__main__":
    serve(app, host=config.HOST, port=config.PORT, threads=config.THREADS_NUM)