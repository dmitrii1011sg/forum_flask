import random

from data import db_session
from data.comments import Comment
from data.like_favorite_user import Like
from data.question import Question
from db_work import DataBaseTool
from sqlalchemy import and_


def create_context(title_page='None', href='/') -> dict:
    """
    :param title_page: title page
    :param href: link page
    :return: dict for context
    """
    data_tool = DataBaseTool(db_session.create_session())
    arr = data_tool.get_list_category_popularity()
    category_popular = [data_tool.get_category_id(el[1]) for el in arr]
    return {
        'title_page': title_page,
        'form': False,
        'form_search': False,
        'items_que': False,
        'question': False,
        'Comment': Comment,
        'Question': Question,
        'Like': Like,
        'and_': and_,
        'randint': random.randint,
        'href': href,
        'category_popular': category_popular
    }






