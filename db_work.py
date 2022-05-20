from sqlalchemy import and_

from data.category import Category
from data.comments import Comment
from data.question import Question
from data.users import User


def created_diaposon(num_page, col_el, col_el_page):
    return col_el - (col_el_page * num_page), col_el - (col_el_page * (num_page - 1))


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

    def create_comment(self, user_id, question_id, content):
        comment = Comment(content=content,
                          user_id=user_id,
                          que_id=question_id)
        self.db_sess.add(comment)
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

    def get_questions_id(self, id):
        question = self.db_sess.query(Question).filter(Question.id == id).first()
        return question

    def get_category_id(self, id):
        category = self.db_sess.query(Category).filter(Category.id == id).first()
        return category

    def get_diapason_query(self, query, num_page, col_el_page):
        diapason = (num_page - 1) * col_el_page, (num_page - 1) * col_el_page + col_el_page
        question_list = list()
        for ind, el in enumerate(query):
            if diapason[0] <= ind < diapason[1]:
                question_list.append(el)
        return question_list

    def get_user_id(self, id):
        return self.db_sess.query(User).filter(User.id == id).first()

    def get_list_category_popularity(self) -> list:
        list_info_category = list()
        for category in self.db_sess.query(Category):
            num = self.db_sess.query(Question).join(Category).filter(Category.name == category.name).count()
            list_info_category.append((num, category.id))
        sorted_list = sorted(list_info_category, reverse=True)[:3]
        return sorted_list



