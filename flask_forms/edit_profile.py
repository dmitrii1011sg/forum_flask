from flask_wtf import FlaskForm
from wtforms import PasswordField, StringField, TextAreaField, SubmitField, EmailField
from wtforms.validators import DataRequired


class EditProfileForm(FlaskForm):
    name = StringField('Имя пользователя')
    lastname = StringField('Фамилия пользователя')
    about = TextAreaField('О вас')
    submit = SubmitField('Изменить')

