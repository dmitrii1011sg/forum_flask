import random

from data.comments import Comment


def create_context(title_page='None', href='/'):
    return {
        'title_page': title_page,
        'form': False,
        'form_search': False,
        'items_que': False,
        'question': False,
        'Comment': Comment,
        'randint': random.randint,
        'href': href
    }


def created_diaposon(num_page, col_el, col_el_page):
    return col_el - (col_el_page * num_page), col_el - (col_el_page * (num_page - 1))



