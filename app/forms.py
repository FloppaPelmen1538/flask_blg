from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, TextAreaField, BooleanField, SubmitField
from wtforms.validators import (
    DataRequired,
    Email,
    EqualTo,
    Length,
    ValidationError,
    Regexp,
)

from app.models import User


class RegistrationForm(FlaskForm):
    username = StringField(
        "Имя пользователя",
        validators=[
            DataRequired(message="Поле обязательно для заполнения"),
            Length(min=3, max=64, message="Имя должно быть от 3 до 64 символов"),
            Regexp(
                r"^[A-Za-z0-9_.-]+$",
                message="Только латинские буквы, цифры и . _ -",
            ),
        ],
    )
    email = StringField(
        "Email",
        validators=[
            DataRequired(message="Поле обязательно для заполнения"),
            Email(message="Введите корректный email"),
            Length(max=120),
        ],
    )
    password = PasswordField(
        "Пароль",
        validators=[
            DataRequired(),
            Length(min=6, message="Пароль должен быть не короче 6 символов"),
        ],
    )
    password_confirm = PasswordField(
        "Повторите пароль",
        validators=[
            DataRequired(),
            EqualTo("password", message="Пароли должны совпадать"),
        ],
    )
    submit = SubmitField("Зарегистрироваться")

    def validate_username(self, field):
        if User.query.filter_by(username=field.data).first():
            raise ValidationError("Это имя пользователя уже занято.")

    def validate_email(self, field):
        if User.query.filter_by(email=field.data.lower()).first():
            raise ValidationError("Аккаунт с таким email уже существует.")


class LoginForm(FlaskForm):

    username = StringField(
        "Имя пользователя или email",
        validators=[DataRequired(), Length(max=120)],
    )
    password = PasswordField("Пароль", validators=[DataRequired()])
    remember_me = BooleanField("Запомнить меня")
    submit = SubmitField("Войти")


class PostForm(FlaskForm):

    title = StringField(
        "Заголовок",
        validators=[
            DataRequired(),
            Length(min=3, max=200, message="От 3 до 200 символов"),
        ],
    )
    body = TextAreaField(
        "Текст записи",
        validators=[
            DataRequired(),
            Length(min=10, message="Текст должен быть не короче 10 символов"),
        ],
    )
    submit = SubmitField("Сохранить")
