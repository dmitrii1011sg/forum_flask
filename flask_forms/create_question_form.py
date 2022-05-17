from flask_wtf import FlaskForm
from wtforms import PasswordField, StringField, TextAreaField, SubmitField, EmailField
from wtforms.validators import DataRequired


class QuestionForm(FlaskForm):
    title_question = StringField('Заголовок вопроса')
    text_question = TextAreaField('О вас')
    category_question = StringField('Теги (через пробел)')
    submit = SubmitField('Создать')

