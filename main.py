import os

import flask_login
from dotenv import load_dotenv
from flask import Flask, render_template, redirect
from flask_login import LoginManager, login_required, logout_user

from data import db_session
from data.users import User
from flask_forms.login_form import LoginUserForm
from flask_forms.register_form import RegisterForm
from flask_forms.search_form import SearchForm

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
    context = {
        'title_page': 'Главная Страница'
    }
    return render_template('base_temp.html', context=context)


@app.route('/login', methods=['GET', 'POST'])
def login_user():
    context = {
        'title_page': 'Вход'
    }
    form_search = SearchForm()
    if form_search.validate_on_submit() and form_search.tag_search.data:
        return redirect(f'/search?tag={form_search.tag_search.data}&page=1')

    form = LoginUserForm()
    context['form'], context['form_search'] = form, form_search
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        user = db_sess.query(User).filter(User.login == form.login.data).first()
        if user and user.check_password(form.password.data):
            flask_login.login_user(user, remember=form.remember_me.data)
            return redirect("/?page=1")
        return render_template('login_page.html', context=context)
    return render_template('login_page.html', context=context)


@app.route('/register', methods=['GET', 'POST'])
def regist_user():
    context = {
        'title_page': 'Регистрация'
    }
    form_search = SearchForm()
    if form_search.validate_on_submit() and form_search.tag_search.data:
        return redirect(f'/search?tag={form_search.tag_search.data}&page=1')
    form = RegisterForm()
    context['form'], context['form_search'] = form, form_search
    print(2)
    if form.validate_on_submit():
        print(1)
        db_sess = db_session.create_session()
        if form.password.data != form.password_again.data:
            return render_template('regist_page.html', context=context)
        user_email = db_sess.query(User).filter(User.login == form.login.data)
        if not user_email.first():
            user = User(name=form.name.data,
                        lastname=form.lastname.data,
                        login=form.login.data,
                        about=form.about.data)
            user.set_password(form.password.data)
            db_sess.add(user)
            db_sess.commit()
            print(f'Susseful add user: {form.name.data, form.lastname.data, form.login.data}')
            return redirect("/login")
        else:
            return render_template('regist_page.html', context=context)
    return render_template('regist_page.html', context=context)


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect("/?page=1")

def main():
    db_session.global_init("db/database.db")
    app.run(debug=True)


if __name__ == '__main__':
    main()