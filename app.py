import flask
import os

DATABASE_PATH = os.getcwd() + "/data" + "app.sqlite"

app = flask.Flask(__name__)
app.config.update(DATABASE = DATABASE_PATH)

