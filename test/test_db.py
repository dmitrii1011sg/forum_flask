from data import db_session
from db_work import DataBaseTool

users = {
    'zed': {
        'id': 1,
        'name': 'Pavel',
        'lastname': 'Vinogradov',
        'password': 'zxc',
        'about': '...'
    },
    'qvantm': {
        'id': 2,
        'name': 'Vlad',
        'lastname': 'Viktorov',
        'password': 'zxc',
        'about': '...'
    },
    'aktuatop': {
        'id': 3,
        'name': 'Arseniy',
        'lastname': 'Nikitin',
        'password': 'zxc',
        'about': '...'
    },
    'zinix': {
        'id': 4,
        'name': 'Daniel',
        'lastname': 'Rizhik',
        'password': 'zxc',
        'about': '...'
    },
    'l1lhakagad': {
        'id': 5,
        'name': 'Michal',
        'lastname': 'Kurevin',
        'password': 'zxc',
        'about': '...'
    },
    'sniperpro2015': {
        'id': 6,
        'name': 'Egor',
        'lastname': 'Kakulechkin',
        'password': 'zxc',
        'about': 'миня завут егор,мне 7 лет, я люблю маму и папу'
    },
    'Chur2004': {
        'id': 7,
        'name': 'Sasha',
        'lastname': 'Churka',
        'password': 'zxc',
        'about': 'Меня зовут Александр, мне 17 лет, в школе все меня гнобили за мою фамилию, но я не отчаиваюсь и иду вперёд!'
    },
    'VIP3000': {
        'id': 8,
        'name': 'Sirgay',
        'lastname': 'Ananiev',
        'password': 'zxc',
        'about': 'Сделаю интро. Пока бесплатно'
    },
}
questions = {
    'Как пройти Гёбу Онива?': {
        'id': 1,
        'content': 'Я уже несколько дней не могу его пройти. Не подскажите, как его пройти. (игра Sekiro)',
        'category': 'sekiro',
        'user_id': 1
    },
    'Как настроить парсек?': {
        'id': 2,
        'content': 'Хочу с другом поиграть вместе в старую игру. Нашел приложение parsec и не могу понять как его настраивать.',
        'category': 'parsec',
        'user_id': 2
    },
    'Как подготовиться к ОГэ за 5 дней?': {
        'id': 3,
        'content': 'Прозедил весь год и теперь не знаю, как сдавать ОГЭ. Не подскажите как можно фастом подоготовиться',
        'category': 'огэ',
        'user_id': 5
    },
    'Как работать с MongoDB?': {
        'id': 4,
        'content': 'Надо для проекта. Помогите пожалйста',
        'category': 'mongodb',
        'user_id': 4
    },
    'Как пройти Горящего быка?': {
        'id': 5,
        'content': 'Спасибо всем за помощь а моем прошлом вопросе. Но как теперь проходить огненого быка (игра Sekiro)',
        'category': 'sekiro',
        'user_id': 1
    },
    'Как вы относитесь к игре csgo?': {
        'id': 6,
        'content': 'Просто интересно.',
        'category': 'опрос',
        'user_id': 3
    },
    'Не знаю что сказать.': {
        'id': 7,
        'content': 'Вопрос ради вопроса',
        'category': 'вопрос',
        'user_id': 8
    },
    'Как легко заработать деньги школьнику?.': {
        'id': 8,
        'content': 'Я не могу позволить себе купить новую игру, помргите, как заработать денег?',
        'category': 'вопрос',
        'user_id': 4
    },
    'Как вы относитесь к результатам "Евровидения 2022"?': {
        'id': 9,
        'content': 'В этом году победила Украина, как вы считаете, результаты политизированы?',
        'category': 'вопрос',
        'user_id': 6
    },
    'Как вы относитесь к OUTWORLD DESTROYER?': {
        'id': 10,
        'content': 'Интересно просто',
        'category': 'Опрос',
        'user_id': 1
    },
    'НАШИ ПОБЕДИЛИ!!!!!': {
        'id': 11,
        'content': 'TEAM SPIRIT ЗАБРАЛИ ПРИЗ В БОЛЕЕ ЧЕМ 18 МЛН. ДОЛЛАРОВ!!!Как считаете, стоит развивать киберспорт среди школьников?',
        'category': 'киберспорт',
        'user_id': 6
    },
    'Смотрите ли вы фирамира?': {
        'id': 12,
        'content': 'Я вот да',
        'category': 'Опрос',
        'user_id': 2
    },
    'Играли ли вы в World of Tanks?': {
        'id': 12,
        'content': 'Если да то го сходим',
        'category': 'Опрос',
        'user_id': 3
    },
    'Игрок под ником "qvantm" оскорбил меня в игре ': {
        'id': 13,
        'content': 'Он сказал, что я плохо играю и смеялся над моей фамилией, как его можно наказать?',
        'category': 'игры',
        'user_id': 7
    },
    'Сколько кКал в лаваше?': {
        'id': 14,
        'content': 'Варианты:1-398\n2-277\n3-576\n4-356\nМини-викторина',
        'category': 'игры',
        'user_id': 4
    },
    'Саша Чурка вызвал меня на стрелу.': {
        'id': 15,
        'content': 'Он вызвал меня драться за школой, что сказать чтобы не идти?',
        'category': 'вопрос',
        'user_id': 2
    },
}

db_session.global_init("db/database.db")
data_tool = DataBaseTool(db_session.create_session())
for user in users:
    us = users[user]
    data_tool.create_user(name=us['name'], lastname=us['lastname'],
                          login=user, about=us['about'], password=us['password'])

for ii in questions:
    que = questions[ii]
    data_tool.create_questions(title=ii, content=que['content'],
                               user_id=que['user_id'], category=que['category'])
