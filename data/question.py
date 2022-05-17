import datetime
import sqlalchemy
from sqlalchemy import orm

from .db_session import SqlAlchemyBase


class Question(SqlAlchemyBase):
    __tablename__ = 'que'

    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)
    title = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    content = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    created_date = sqlalchemy.Column(sqlalchemy.DateTime, default=datetime.datetime.now)
    #tags = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    close = sqlalchemy.Column(sqlalchemy.Boolean, default=False)
    user_id = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey("users.id"))
    category_id = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey("category.id"))
    user = orm.relationship("User", back_populates='que')
    comm = orm.relationship("Comment", back_populates='que', cascade="all, delete, delete-orphan")
    category = orm.relationship('Category', back_populates='questions')

    def get_data(self):
        return self.created_date.strftime("%m/%d/%Y")

