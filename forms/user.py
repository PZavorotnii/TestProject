from flask_wtf import FlaskForm
from wtforms import PasswordField, StringField, TextAreaField, SubmitField, EmailField, BooleanField, FieldList, HiddenField
from wtforms import SelectMultipleField
from wtforms.validators import DataRequired


class RegisterForm(FlaskForm):
    name = StringField('Логин', validators=[DataRequired()])
    password = PasswordField('Пароль', validators=[DataRequired()])
    password_again = PasswordField('Повторите пароль', validators=[DataRequired()])
    powers = BooleanField('Хочу быть администратором')
    submit = SubmitField('Войти')


class LoginForm(FlaskForm):
    login = StringField('Логин', validators=[DataRequired()])
    password = PasswordField('Пароль', validators=[DataRequired()])
    remember_me = BooleanField('Запомнить меня')
    submit = SubmitField('Войти')


class TrainForm(FlaskForm):
    answers = SelectMultipleField() # validators=[DataRequired()])
    fwords = HiddenField("words")
    submit = SubmitField('Проверить')

    def __init__(self):
        super().__init__()
        self.answers.choices = [(str(i + 1), str(i + 1)) for i in range(5)]


class CheckForm(FlaskForm):
    user_answers = StringField('Ваши ответы')
    right_answers = StringField('Правильные ответы')
    submit = SubmitField('Вернуться')
    label = StringField()

    def __init__(self, words):
        super().__init__()
        self.words = words

    def words(self):
        return self.words


class AddForm(FlaskForm):
    word = StringField('Введите слово, обозначив ударную гласную прописной буквой', validators=[DataRequired()])
    variant = StringField('Укажите возможный неверны вариант ударения')
    submit = SubmitField('Добавить')
