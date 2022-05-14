from flask_wtf import FlaskForm
from wtforms import PasswordField, StringField, TextAreaField, SubmitField, EmailField
from wtforms.validators import DataRequired


class RegisterForm(FlaskForm):
    login = StringField('Логин')
    password = PasswordField('Пароль', validators=[DataRequired()])
    password_again = PasswordField('Повторите пароль', validators=[DataRequired()])
    name = StringField('Имя пользователя', validators=[DataRequired()])
    lastname = StringField('Имя пользователя', validators=[DataRequired()])
    about = TextAreaField('О вас')
    submit = SubmitField('Зарегистроваться')

