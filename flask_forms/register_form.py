from flask_wtf import FlaskForm
from wtforms import PasswordField, StringField, TextAreaField, SubmitField
from wtforms.validators import DataRequired
from flask_wtf.file import FileField


class RegisterForm(FlaskForm):
    login = StringField('Логин')
    password = PasswordField('Пароль', validators=[DataRequired()])
    password_again = PasswordField('Повторите пароль', validators=[DataRequired()])
    name = StringField('Имя пользователя', validators=[DataRequired()])
    lastname = StringField('Имя пользователя', validators=[DataRequired()])
    avatar = FileField()
    about = TextAreaField('О вас')
    submit = SubmitField('Зарегистроваться')

