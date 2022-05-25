import os

from sqlalchemy import and_

from data.avatar_user import Avatar
from data.category import Category
from data.comments import Comment
from data.question import Question
from data.users import User

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}


def created_diaposon(num_page, col_el, col_el_page):
    """
    Create diapason
    :param num_page: number page
    :param col_el: numbers elements
    :param col_el_page: numbers elements on page
    :return:
    """
    return col_el - (col_el_page * num_page), col_el - (col_el_page * (num_page - 1))


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS


class DataBaseTool:
    """
    Tools for work with database
    """
    def __init__(self, db_sess):
        self.db_sess = db_sess

    # user tools
    def create_user(self, name, lastname, login, about, password, file=False) -> bool:
        """
        Create new user
        :param name: name user
        :param lastname: lastname user
        :param login: login user
        :param about: about info user
        :param password: password user
        :return:
        """
        user_login = self.db_sess.query(User).filter(User.login == login)
        if not user_login.first():
            id_image = 1
            if file and allowed_file(file.filename):
                id_image = self.db_sess.query(Avatar).order_by(Avatar.id.desc()).first().id + 1
                file.save(os.path.join('static/image_avatars/', f'{id_image}.png'))
                self.db_sess.add(Avatar())
            user = User(name=name, lastname=lastname, login=login, about=about, avatar_id=id_image)
            user.set_password(password)
            self.db_sess.add(user)
            self.db_sess.commit()
            print(f'Susseful add user: {name, lastname, login}')
            return True
        return False

    def update_user(self, id_user, context):
        user = self.db_sess.query(User).filter(User.id == id_user).first()
        dict_for_update = {}
        for param in context:
            if context[param]:
                dict_for_update[param] = context[param]
            else:
                dict_for_update[param] = user.get_data()[param]
        self.db_sess.query(User).filter(User.id == id_user).update(dict_for_update)
        self.db_sess.commit()

    def check_user(self, login, password):
        """
        User existence check
        :param login: login user
        :param password: password user
        :return:
        """
        user = self.db_sess.query(User).filter(User.login == login).first()
        if user and user.check_password(password):
            return user
        return False

    def get_questions_user_id(self, user_id):
        questions = self.db_sess.query(Question).filter(Question.user_id == user_id)
        return questions

    def get_user_id(self, id):
        """
        Get user by id
        :param id: id user
        :return:
        """
        return self.db_sess.query(User).filter(User.id == id).first()

    # category tools
    def creating_missing_category(self, category: str) -> None:
        """
        Create a category if it doesn't exist
        :param category: name category
        :return:
        """
        if category:
            if not self.db_sess.query(Category).filter(Category.name == category).first():
                new_tag = Category(name=category)
                self.db_sess.add(new_tag)
            self.db_sess.commit()

    def get_category_id(self, id):
        """
        Get category by id
        :param id: id category
        :return:
        """
        category = self.db_sess.query(Category).filter(Category.id == id).first()
        return category

    def get_list_category_popularity(self) -> list:
        """
        Categories by their popularity
        :return:
        """
        list_info_category = list()
        for category in self.db_sess.query(Category):
            num = self.db_sess.query(Question).join(Category).filter(Category.name == category.name).count()
            list_info_category.append((num, category.id))
        sorted_list = sorted(list_info_category, reverse=True)[:3]
        return sorted_list

    # questions tools
    def create_questions(self, title='Отсутствует', content='...', category=False, user_id=1):
        """
        Create questions
        :param title: title question
        :param content: text question
        :param category: category question
        :param user_id: id user who created the question
        :return:
        """
        self.creating_missing_category(category)
        que = Question(title=title,
                       content=content,
                       user_id=user_id,
                       category_id=self.db_sess.query(Category).filter(Category.name == category).first().id)
        self.db_sess.add(que)
        self.db_sess.commit()

    def get_questions_category(self, category, filter_id: bool = True):
        """
        Get questions by category
        :param category:
        :param filter_id:
        :return:
        """
        items_query = self.db_sess.query(Question).join(Category).filter(Category.name == category)
        if filter_id:
            items_query = items_query.order_by(Question.id.desc())
        return items_query

    def get_questions_id(self, id):
        """
        Get questions by category
        :param id: id questions
        :return:
        """
        question = self.db_sess.query(Question).filter(Question.id == id).first()
        return question

    # comments tools
    def create_comment(self, user_id, question_id, content):
        """
        Create comment user
        :param user_id: id user who created the comment
        :param question_id: id question
        :param content: text comment
        :return:
        """
        comment = Comment(content=content,
                          user_id=user_id,
                          que_id=question_id)
        self.db_sess.add(comment)
        self.db_sess.commit()

    # other
    def get_diapason_query(self, query, num_page, col_el_page):
        """
        Get diapason by query
        :param query:
        :param num_page:
        :param col_el_page:
        :return:
        """
        diapason = (num_page - 1) * col_el_page, (num_page - 1) * col_el_page + col_el_page
        question_list = list()
        for ind, el in enumerate(query):
            if diapason[0] <= ind < diapason[1]:
                question_list.append(el)
        return question_list







