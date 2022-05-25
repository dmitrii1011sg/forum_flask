import datetime
import sqlalchemy
from sqlalchemy import orm

from .db_session import SqlAlchemyBase


class Like(SqlAlchemyBase):
    __tablename__ = 'like'

    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)
    user_id = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey("users.id"))
    comm_id = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey("comment.id"))
    user = orm.relationship("User", back_populates='like')
    comm = orm.relationship("Comment", back_populates='like')


# class Favorite(SqlAlchemyBase):
#     __tablename__ = 'favorite'
#
#     id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)
#     user_id = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey("users.id"))
#     que_id = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey("que.id"))
#     user = orm.relationship("User", back_populates='favorite')
#     que = orm.relationship("Comment", back_populates='favorite')


