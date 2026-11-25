from flask_wtf import FlaskForm
from wtforms import EmailField, PasswordField, StringField
from wtforms.validators import Email, EqualTo, InputRequired, Length


def strip_whitespace(value):
    return value.strip() if value else value


class RegistrationForm(FlaskForm):
    username = StringField(
        "Username",
        filters=[strip_whitespace],
        validators=[Length(min=1, max=80, message="Inserisci uno username da 1 a 80 caratteri.")],
    )
    email = EmailField(
        "Email",
        filters=[strip_whitespace],
        validators=[
            Length(max=254, message="L’indirizzo email può contenere al massimo 254 caratteri."),
            Email(message="Inserisci un indirizzo email valido."),
        ],
    )
    password = PasswordField(
        "Password",
        validators=[Length(min=10, max=128, message="Usa da 10 a 128 caratteri.")],
    )
    confirm_password = PasswordField(
        "Conferma password",
        validators=[
            InputRequired(message="Conferma la password."),
            EqualTo("password", message="Le password non coincidono."),
        ],
    )
