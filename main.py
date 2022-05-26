import os
import flask_login
from dotenv import load_dotenv
from flask import Flask, render_template, redirect, request
from flask_login import LoginManager, login_required, logout_user, current_user
from sqlalchemy import and_

from data import db_session
from data.avatar_user import Avatar
from data.question import Question
from data.users import User
from db_work import DataBaseTool, created_diaposon
from flask_forms.comment_form import CommentForm
from flask_forms.create_question_form import QuestionForm
from flask_forms.edit_profile import EditProfileForm
from flask_forms.edit_question import EditQuestionForm
from flask_forms.login_form import LoginUserForm
from flask_forms.register_form import RegisterForm
from flask_forms.search_form import SearchForm
from tools import create_context

load_dotenv()

app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv('TOKEN')
login_manager = LoginManager()
login_manager.init_app(app)


@login_manager.user_loader
def load_user(user_id):
    """
    Load user
    :param user_id: id user
    :return:
    """
    db_sess = db_session.create_session()
    return db_sess.query(User).get(user_id)


@app.route('/', methods=['GET', 'POST'])
def index():
    """
    Main page
    :return: template or redirect
    """
    context = create_context(title_page='Главная', href='/')

    form_search = SearchForm()
    if form_search.validate_on_submit() and form_search.category_search.data:
        return redirect(
            f'/search?category={form_search.category_search.data}&page=1')

    page_number = request.args.get('page')
    if page_number:
        page_number = int(page_number)
    else:
        return redirect('/?page=1')

    db_sess = db_session.create_session()
    col_que = db_sess.query(Question).count()
    diapason = created_diaposon(page_number, col_que, 20)
    # data_tool.get_diapason_query(items_que, int(page_number), 20)

    items_que = db_sess.query(Question).filter(
        and_(Question.id > diapason[0],
             Question.id <= diapason[1]
             )).order_by(Question.id.desc())

    context['form_search'] = form_search
    context['page_number'] = page_number
    context['db_sess'] = db_sess
    context['title_list_question'] = 'Последние вопросы:'
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
    data_tool = DataBaseTool(db_session.create_session())  # tools for db
    context = create_context(title_page='Вход', href='/login')

    form_search = SearchForm()
    if form_search.validate_on_submit() and form_search.category_search.data:
        return redirect(
            f'/search?category={form_search.category_search.data}&page=1')

    form = LoginUserForm()
    context['form'], context['form_search'] = form, form_search
    if form.validate_on_submit():
        user = data_tool.check_user(login=form.login.data,
                                    password=form.password.data)
        if user:
            flask_login.login_user(user, remember=form.remember_me.data)
            return redirect("/?page=1")
        context['message'] = 'Вы неправильно ввели  логин или пароль'
        return render_template('login_page.html', context=context)
    return render_template('login_page.html', context=context)


@app.route('/register', methods=['GET', 'POST'])
def regist_user():
    """
    Page for signup users
    :return: template or redirect
    """
    data_tool = DataBaseTool(db_session.create_session())  # tools for db
    context = create_context(title_page='Регистрация', href='/register')

    form_search = SearchForm()  # search
    if form_search.validate_on_submit() and form_search.category_search.data:
        return redirect(
            f'/search?category={form_search.category_search.data}&page=1')

    form = RegisterForm()  # create signup form
    context['form'], context['form_search'] = form, form_search

    if form.validate_on_submit():  # form validate on submit
        if form.password.data != form.password_again.data:  # validate password
            context['message'] = 'Пароли не совпадают'
            return render_template('regist_page.html', context=context)
        file = True if form.avatar.data else False
        user_info = data_tool.create_user(name=form.name.data,
                                          lastname=form.lastname.data,
                                          login=form.login.data,
                                          about=form.about.data,
                                          password=form.password.data,
                                          file=True)
        if user_info:
            if file:
                db_sess = db_session.create_session()
                last_image = db_sess.query(Avatar).order_by(Avatar.id.desc())
                id_image = last_image.first().id
                form.avatar.data.save('static/image_avatars/' + f'{id_image}.png')
            return redirect("/login")
        else:
            context['message'] = f'Пользователь с логином {form.login.data}, уже существует'
            return render_template('regist_page.html', context=context)
    return render_template('regist_page.html', context=context)


@app.route('/edit-profile', methods=['GET', 'POST'])
def edit_user():
    """
    Page for signup users
    :return: template or redirect
    """
    data_tool = DataBaseTool(db_session.create_session())  # tools for db
    context = create_context(title_page='Регистрация', href='/register')

    form_search = SearchForm()  # search
    if form_search.validate_on_submit() and form_search.category_search.data:
        return redirect(
            f'/search?category={form_search.category_search.data}&page=1')

    form = EditProfileForm()  # create signup form
    context['form'], context['form_search'] = form, form_search

    if form.validate_on_submit():  # form validate on submit
        data_tool.update_user(flask_login.current_user.id, {
                              'name': form.name.data,
                              'lastname': form.lastname.data,
                              'about': form.about.data})
        return redirect(f'/profile/{flask_login.current_user.id}')
    return render_template('edit_profile.html', context=context)


@app.route('/edit-question/<int:que_id>', methods=['GET', 'POST'])
def edit_question(que_id):
    """
    Page for signup users
    :return: template or redirect
    """
    data_tool = DataBaseTool(db_session.create_session())  # tools for db
    context = create_context(title_page='Редактирование вопроса',
                             href=f'/edit-question/{que_id}')

    form_search = SearchForm()  # search
    if form_search.validate_on_submit() and form_search.category_search.data:
        return redirect(
            f'/search?category={form_search.category_search.data}&page=1')

    form = EditQuestionForm()  # create signup form
    context['form'], context['form_search'] = form, form_search

    if form.validate_on_submit():  # form validate on submit
        if flask_login.current_user.id == data_tool.get_questions_id(que_id).user_id:
            data_tool.update_question(que_id,
                                      {'title': form.title_question.data,
                                       'content': form.text_question.data})
        return redirect(f'/question?id={que_id}')
    context['question'] = data_tool.get_questions_id(que_id)
    return render_template('edit_question_temp.html', context=context)


@app.route('/like/<int:que_id>/<int:comm_id>', methods=['GET', 'POST'])
def like(que_id, comm_id):
    data_tool = DataBaseTool(db_session.create_session())  # tools for db
    data_tool.like_comment(user_id=flask_login.current_user.id, comm_id=comm_id)
    return redirect(f'/question?id={que_id}')


@app.route('/favorite/<int:que_id>', methods=['GET', 'POST'])
def favorite(que_id):
    data_tool = DataBaseTool(db_session.create_session())  # tools for db
    data_tool.add_favorite_questions(user_id=flask_login.current_user.id,
                                     que_id=que_id)
    return redirect(f'/question?id={que_id}')


@app.route('/close-question/<int:que_id>', methods=['GET', 'POST'])
def close_question(que_id):
    data_tool = DataBaseTool(db_session.create_session())  # tools for db
    if data_tool.get_questions_id(que_id).user_id == current_user.id:
        data_tool.close_question(que_id=que_id)
    return redirect(f'/question?id={que_id}')


@app.route('/open-question/<int:que_id>', methods=['GET', 'POST'])
def open_question(que_id):
    data_tool = DataBaseTool(db_session.create_session())  # tools for db
    if data_tool.get_questions_id(que_id).user_id == current_user.id:
        data_tool.open_question(que_id=que_id)
    return redirect(f'/question?id={que_id}')


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
    data_tool = DataBaseTool(db_session.create_session())  # tools for db
    context = create_context(title_page='Создание вопроса',
                             href='/create-question')  # param for templates

    form_search = SearchForm()  # search
    if form_search.validate_on_submit() and form_search.category_search.data:
        return redirect(
            f'/search?category={form_search.category_search.data}&page=1')

    form = QuestionForm()  # create questions form
    context['form'], context['form_search'] = form, form_search

    if form.validate_on_submit():  # form validate on submit
        data_tool.create_questions(title=form.title_question.data,
                                   content=form.text_question.data,
                                   user_id=flask_login.current_user.id,
                                   category=form.category_question.data)
        return redirect('/?page=1')
    return render_template('create_question_temp.html', context=context)


@app.route('/search', methods=['GET', 'POST'])
def search_page():
    """
    Page search by category
    :return:
    """
    data_tool = DataBaseTool(db_session.create_session())  # tools for db
    context = create_context(title_page='Результаты Поиска', href='/search')

    form_search = SearchForm()
    if form_search.validate_on_submit() and form_search.category_search.data:
        return redirect(
            f'/search?category={form_search.category_search.data}&page=1')

    page_number = request.args.get('page')
    category = request.args.get('category')
    items_que = data_tool.get_questions_category(category)
    items_que = data_tool.get_diapason_query(items_que, int(page_number), 20)

    context['form_search'] = form_search
    context['page_number'] = int(page_number)
    context['db_sess'] = db_session.create_session()
    context['additional_arg'] = f'category={category}'
    context['title_list_question'] = f'Результаты поиска по запросу {category}:'
    if items_que:
        context['items_que'] = items_que
        return render_template('questions_list_temp.html', context=context)

    return render_template('questions_list_temp.html', context=context)


@app.route('/questions/user/<int:id>', methods=['GET', 'POST'])
def users_questions(id):
    """
    Page for questions users
    :return:
    """
    data_tool = DataBaseTool(db_session.create_session())  # tools for db
    context = create_context(title_page='Результаты Поиска',
                             href=f'/questions/user/{id}')

    form_search = SearchForm()
    if form_search.validate_on_submit() and form_search.category_search.data:
        return redirect(
            f'/search?category={form_search.category_search.data}&page=1')

    page_number = request.args.get('page')
    items_que = data_tool.get_questions_user_id(id)
    items_que = data_tool.get_diapason_query(items_que, int(page_number), 20)

    context['form_search'] = form_search
    context['page_number'] = int(page_number)
    context['db_sess'] = db_session.create_session()
    context['title_list_question'] = f'Список вопросов пользователя:'
    if items_que:
        context['items_que'] = items_que
        return render_template('questions_list_temp.html', context=context)

    return render_template('questions_list_temp.html', context=context)


@app.route('/questions_fav/user/<int:id>', methods=['GET', 'POST'])
def users_fav_questions(id):
    """
    Page for questions users
    :return:
    """
    data_tool = DataBaseTool(db_session.create_session())  # tools for db
    context = create_context(title_page='Избранные вопросы',
                             href=f'/questions_fav/user/{id}')

    form_search = SearchForm()
    if form_search.validate_on_submit() and form_search.category_search.data:
        return redirect(
            f'/search?category={form_search.category_search.data}&page=1')

    page_number = request.args.get('page')
    items_que = data_tool.get_questions_favorite_user(id)
    items_que = data_tool.get_diapason_query(items_que, int(page_number), 20)

    context['form_search'] = form_search
    context['page_number'] = int(page_number)
    context['db_sess'] = db_session.create_session()
    context['title_list_question'] = f'Список избранных вопросов пользователя:'
    if items_que:
        context['items_que'] = items_que
        return render_template('questions_list_temp.html', context=context)

    return render_template('questions_list_temp.html', context=context)


@app.route('/question', methods=['GET', 'POST'])
def question_page():
    """
    Page for question
    :return:
    """
    id = request.args.get('id')
    data_tool = DataBaseTool(db_session.create_session())  # tools for db
    context = create_context(title_page=f'Вопрос №{id}', href='/question')

    form_search = SearchForm()
    if form_search.validate_on_submit() and form_search.category_search.data:
        return redirect(
            f'/search?category={form_search.category_search.data}&page=1')

    form = CommentForm()  # create questions form

    if form.validate_on_submit():  # form validate on submit
        data_tool.create_comment(content=form.comment_text.data,
                                 user_id=flask_login.current_user.id,
                                 question_id=id)
        return redirect(f'/question?id={id}')

    context['form_search'] = form_search
    context['form'] = form
    context['question'] = data_tool.get_questions_id(id)
    context['db_sess'] = db_session.create_session()
    return render_template('questions_page_temp.html', context=context)


@app.route('/profile/<int:id>', methods=['GET', 'POST'])
def profile(id):
    """
    Page for user's profile
    :param id:
    :return:
    """
    data_tool = DataBaseTool(db_session.create_session())  # tools for db
    context = create_context(title_page=f'Профиль', href='/profile')

    form_search = SearchForm()
    if form_search.validate_on_submit() and form_search.category_search.data:
        return redirect(f'/search?category={form_search.category_search.data}&page=1')

    context['form_search'] = form_search
    context['db_sess'] = db_session.create_session()
    context['user'] = data_tool.get_user_id(id)
    return render_template('profile.html', context=context)


@app.route('/rules', methods=['GET', 'POST'])
def rules():
    """
    Page for rule
    :return:
    """
    data_tool = DataBaseTool(db_session.create_session())  # tools for db
    context = create_context(title_page=f'Профиль', href='/profile')

    form_search = SearchForm()
    if form_search.validate_on_submit() and form_search.category_search.data:
        return redirect(
            f'/search?category={form_search.category_search.data}&page=1')

    context['form_search'] = form_search
    context['db_sess'] = db_session.create_session()
    return render_template('rule_temp.html', context=context)


def main():
    """
    Run main application and initialization database
    :return: None
    """
    db_session.global_init("db/database.db")
    app.run(debug=True)


if __name__ == '__main__':
    main()
