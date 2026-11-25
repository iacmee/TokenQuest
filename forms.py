from flask_wtf import FlaskForm
from wtforms import EmailField, PasswordField, StringField
from wtforms.validators import Email, EqualTo, InputRequired, Length
import config


def strip_whitespace(value: str | None) -> str | None:
    if value is None:
        return None
    return value.strip()


class LoginForm(FlaskForm):
    username = StringField(
        "Username",
        filters=[strip_whitespace],
        validators=[Length(
            min=config.LOGIN_USERNAME_MIN_LENGTH,
            max=config.LOGIN_USERNAME_MAX_LENGTH,
            message="Inserisci uno username da %(min)d a %(max)d caratteri.",
        )],
    )
    password = PasswordField(
        "Password",
        validators=[Length(
            min=config.LOGIN_PASSWORD_MIN_LENGTH,
            max=config.LOGIN_PASSWORD_MAX_LENGTH,
            message="Inserisci una password da %(min)d a %(max)d caratteri.",
        )],
    )


class RegistrationForm(FlaskForm):
    username = StringField(
        "Username",
        filters=[strip_whitespace],
        validators=[Length(
            min=config.USERNAME_MIN_LENGTH,
            max=config.USERNAME_MAX_LENGTH,
            message="Inserisci uno username da %(min)d a %(max)d caratteri.",
        )],
    )
    nickname = StringField(
        "Nickname",
        filters=[strip_whitespace],
        validators=[Length(
            min=config.NICKNAME_MIN_LENGTH,
            max=config.NICKNAME_MAX_LENGTH,
            message="Inserisci un nickname da %(min)d a %(max)d caratteri.",
        )],
    )
    email = EmailField(
        "Email",
        filters=[strip_whitespace],
        validators=[
            Length(
                min=config.EMAIL_MIN_LENGTH,
                max=config.EMAIL_MAX_LENGTH,
                message="L’indirizzo email deve contenere da %(min)d a %(max)d caratteri.",
            ),
            Email(message="Inserisci un indirizzo email valido."),
        ],
    )
    password = PasswordField(
        "Password",
        validators=[Length(
            min=config.PASSWORD_MIN_LENGTH,
            max=config.PASSWORD_MAX_LENGTH,
            message="Inserisci una password da %(min)d a %(max)d caratteri.",
        )],
    )
    confirm_password = PasswordField(
        "Conferma password",
        validators=[
            InputRequired(message="Conferma la password."),
            EqualTo("password", message="Le password non coincidono."),
        ],
    )
