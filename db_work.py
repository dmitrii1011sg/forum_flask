from sqlalchemy import and_

from data.category import Category
from data.question import Question
from data.users import User
from tools import created_diaposon


class DataBaseTool:
    def __init__(self, db_sess):
        self.db_sess = db_sess

    def creating_missing_category(self, category: str):
        if category:
            if not self.db_sess.query(Category).filter(Category.name == category).first():
                new_tag = Category(name=category)
                self.db_sess.add(new_tag)
            self.db_sess.commit()

    def create_questions(self, title='Отсутствует', content='...', category=False, user_id=1) -> bool:
        self.creating_missing_category(category)
        que = Question(title=title,
                       content=content,
                       user_id=user_id,
                       category_id=self.db_sess.query(Category).filter(Category.name == category).first().id)
        self.db_sess.add(que)
        self.db_sess.commit()

    def create_user(self, name, lastname, login, about, password) -> bool:
        user_login = self.db_sess.query(User).filter(User.login == login)
        if not user_login.first():
            user = User(name=name, lastname=lastname, login=login, about=about)
            user.set_password(password)
            self.db_sess.add(user)
            self.db_sess.commit()
            print(f'Susseful add user: {name, lastname, login}')
            return True
        return False

    def check_user(self, login, password):
        user = self.db_sess.query(User).filter(User.login == login).first()
        if user and user.check_password(password):
            return user
        return False

    def get_questions_user_id(self, user_id):
        pass

    def get_questions_category(self, category, filter_id: bool = True):
        items_query = self.db_sess.query(Question).join(Category).filter(Category.name == category)
        if filter_id:
            items_query = items_query.order_by(Question.id.desc())
        return items_query

    def get_diapason_query(self, query, num_page, col_el_page):
        diapason = (num_page-1)*col_el_page, (num_page-1)*col_el_page+col_el_page
        question_list = list()
        for ind, el in enumerate(query):
            if diapason[0] <= ind < diapason[1]:
                question_list.append(el)
        return question_list
