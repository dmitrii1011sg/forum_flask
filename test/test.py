# from data import db_session
# from data.question import Question
#
# db_session.global_init("db/database.db")
# db_sess = db_session.create_session()
# for i in range(60):
#     que = Question(title=i,
#                    content=i,
#                    user_id=1,
#                    tags=f'zed {i}')
#     db_sess.add(que)
# db_sess.commit()

arr = [(0, 9), (8, 9), (4, 9)]
arr1 = sorted(arr, reverse=True)
print(arr1)
