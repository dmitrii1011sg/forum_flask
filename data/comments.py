import datetime
import sqlalchemy
from sqlalchemy import orm

from .db_session import SqlAlchemyBase


class Comment(SqlAlchemyBase):
    __tablename__ = 'comment'

    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)
    content = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    created_date = sqlalchemy.Column(sqlalchemy.DateTime, default=datetime.datetime.now)

    user_id = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey("users.id"))
    que_id = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey("que.id"))

    user = orm.relationship('User', back_populates="comm")
    que = orm.relationship('Question', back_populates="comm")

