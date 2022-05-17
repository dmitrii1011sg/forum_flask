from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, EmailField
from wtforms.validators import DataRequired


class SearchForm(FlaskForm):
    category_search = StringField('Категория')
    submit = SubmitField('Поиск')