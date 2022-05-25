import sqlalchemy
from flask_login import UserMixin
from sqlalchemy import orm
from .db_session import SqlAlchemyBase


class Avatar(SqlAlchemyBase):
    __tablename__ = 'avatar'

    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)
    user = orm.relationship("User", back_populates='avatar')

    def get_name_file(self):
        return f'/image_avatars/{self.id}.png'

