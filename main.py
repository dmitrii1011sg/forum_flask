import os

import flask_login
from dotenv import load_dotenv
from flask import Flask, render_template, redirect, request
from flask_login import LoginManager, login_required, logout_user
from sqlalchemy import and_

from data import db_session
from data.question import Question
from data.category import Category
from data.users import User
from db_work import DataBaseTool
from flask_forms.create_question_form import QuestionForm
from flask_forms.login_form import LoginUserForm
from flask_forms.register_form import RegisterForm
from flask_forms.search_form import SearchForm
from tools import create_context, created_diaposon

load_dotenv()

app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv('TOKEN')
login_manager = LoginManager()
login_manager.init_app(app)


@login_manager.user_loader
def load_user(user_id):
    db_sess = db_session.create_session()
    return db_sess.query(User).get(user_id)


@app.route('/', methods=['GET', 'POST'])
def index():
    context = create_context(title_page='Главная', href='/')

    form_search = SearchForm()
    if form_search.validate_on_submit() and form_search.category_search.data:
        return redirect(f'/search?category={form_search.category_search.data}&page=1')

    page_number = request.args.get('page')
    if page_number:
        page_number = int(page_number)
    else:
        return redirect('/?page=1')

    db_sess = db_session.create_session()
    col_que = db_sess.query(Question).count()
    diapason = created_diaposon(page_number, col_que, 20)

    items_que = db_sess.query(Question).filter(
        and_(Question.id > diapason[0],
             Question.id <= diapason[1]
             )).order_by(Question.id.desc())

    context['form_search'] = form_search
    context['page_number'] = page_number
    context['db_sess'] = db_sess
    if items_que:
        context['items_que'] = items_que
        return render_template('questions_list_temp.html', context=context)

    return render_template('questions_list_temp.html', context=context)


@app.route('/login', methods=['GET', 'POST'])
def login_user():
    """
    Page for login user
    :return: template or redirect
    """
    data_tool = DataBaseTool(db_session.create_session())   # tools for db
    context = create_context(title_page='Вход', href='/login')

    form_search = SearchForm()
    if form_search.validate_on_submit() and form_search.category_search.data:
        return redirect(f'/search?category={form_search.category_search.data}&page=1')

    form = LoginUserForm()
    context['form'], context['form_search'] = form, form_search
    if form.validate_on_submit():
        user = data_tool.check_user(login=form.login.data, password=form.password.data)
        if user:
            flask_login.login_user(user, remember=form.remember_me.data)
            return redirect("/?page=1")
        return render_template('login_page.html', context=context)
    return render_template('login_page.html', context=context)


@app.route('/register', methods=['GET', 'POST'])
def regist_user():
    """
    Page for signup users
    :return: template or redirect
    """
    data_tool = DataBaseTool(db_session.create_session())   # tools for db
    context = create_context(title_page='Регистрация', href='/register')    # param for templates

    form_search = SearchForm()  # search
    if form_search.validate_on_submit() and form_search.category_search.data:
        return redirect(f'/search?category={form_search.category_search.data}&page=1')

    form = RegisterForm()   # create signup form
    context['form'], context['form_search'] = form, form_search

    if form.validate_on_submit():   # form validate on submit
        if form.password.data != form.password_again.data:  # validate password
            return render_template('regist_page.html', context=context)
        user_info = data_tool.create_user(name=form.name.data, lastname=form.lastname.data,
                                          login=form.login.data, about=form.about.data, password=form.password.data)
        if user_info:
            return redirect("/login")
        else:
            return render_template('regist_page.html', context=context)
    return render_template('regist_page.html', context=context)


@app.route('/logout')
@login_required
def logout():
    """
    Loguot user
    :return: redirect
    """
    logout_user()
    return redirect("/?page=1")


@app.route('/create-question', methods=['GET', 'POST'])
def create_question():
    """
    Page for creating questions
    :return: template or redirect
    """
    data_tool = DataBaseTool(db_session.create_session())   # tools for db
    context = create_context(title_page='Создание вопроса', href='/create-question')    # param for templates

    form_search = SearchForm()  # search
    if form_search.validate_on_submit() and form_search.category_search.data:
        return redirect(f'/search?category={form_search.category_search.data}&page=1')

    form = QuestionForm()   # create questions form
    context['form'], context['form_search'] = form, form_search

    if form.validate_on_submit():   # form validate on submit
        data_tool.create_questions(title=form.title_question.data, content=form.text_question.data,
                                   user_id=flask_login.current_user.id, category=form.category_question.data)
        return redirect('/?page=1')
    return render_template('create_question_temp.html', context=context)


@app.route('/search', methods=['GET', 'POST'])
def search_page():
    data_tool = DataBaseTool(db_session.create_session())  # tools for db
    context = create_context(title_page='Результаты Поиска', href='/search')

    form_search = SearchForm()
    if form_search.validate_on_submit() and form_search.category_search.data:
        return redirect(f'/search?category={form_search.category_search.data}&page=1')

    page_number = request.args.get('page')
    category = request.args.get('category')
    items_que = data_tool.get_questions_category(category)
    items_que = data_tool.get_diapason_query(items_que, int(page_number), 2)
    # db_sess = db_session.create_session()
    # col_que = db_sess.query(Question).join(Category).filter(Category.name == category).count()
    # diapason = created_diaposon(int(page_number), col_que, 20)
    #
    # items_que = db_sess.query(Question).join(Category).filter(
    #     and_(Question.id > diapason[0],
    #          Question.id <= diapason[1],
    #          Category.name == category
    #          )).order_by(Question.id.desc())

    context['form_search'] = form_search
    context['page_number'] = int(page_number)
    context['db_sess'] = db_session.create_session()
    context['additional_arg'] = f'category={category}'
    if items_que:
        context['items_que'] = items_que
        return render_template('questions_list_temp.html', context=context)

    return render_template('questions_list_temp.html', context=context)


def main():
    """
    Run main application and initialization database
    :return: None
    """
    db_session.global_init("db/database.db")
    app.run(debug=True)


if __name__ == '__main__':
    main()
