from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, EmailField
from wtforms.validators import DataRequired


class SearchForm(FlaskForm):
    tag_search = StringField('Тег')
    submit = SubmitField('Найти по Тегу')