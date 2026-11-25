from flask_sqlalchemy import SQLAlchemy
from datetime import datetime, timezone
import config

db = SQLAlchemy()


class Question(db.Model):
    __tablename__ = "questions"

    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.Text, nullable=False)
    options = db.Column(db.JSON, nullable=False)
    correct_option = db.Column(db.Integer, nullable=False)


class QuizRound(db.Model):
    __tablename__ = "quiz_rounds"

    user_id = db.Column(db.ForeignKey("users.id"), primary_key=True)
    question_ids = db.Column(db.JSON, nullable=False)
    position = db.Column(db.Integer, nullable=False, default=0)
    correct_answers = db.Column(db.Integer, nullable=False, default=0)


class User(db.Model):

    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)

    username = db.Column(
        db.String(80, collation="NOCASE"),
        nullable=False,
        unique=True
    )

    nickname = db.Column(
        db.String(config.NICKNAME_MAX_LENGTH, collation="NOCASE"),
        nullable=False,
        unique=True,
    )

    email = db.Column(
        db.String(254, collation="NOCASE"),
        nullable=False,
        unique=True
    )

    password_hash = db.Column(
        db.Text,
        nullable=False
    )

    score = db.Column(
        db.Integer,
        nullable=False,
        default=0,
        server_default="0"
    )

    created_at = db.Column(
        db.DateTime,
        nullable=False,
        default=lambda: datetime.now(timezone.utc)
    )

    password_changed_at = db.Column(
        db.DateTime,
        nullable=True
    )
