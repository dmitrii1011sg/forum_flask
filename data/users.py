import datetime
import sqlalchemy
from flask_login import UserMixin
from sqlalchemy import orm
from .db_session import SqlAlchemyBase
from werkzeug.security import generate_password_hash, check_password_hash


class User(SqlAlchemyBase, UserMixin):
    __tablename__ = 'users'

    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)
    name = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    lastname = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    login = sqlalchemy.Column(sqlalchemy.String, index=True, unique=True, nullable=True)
    about = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    hashed_password = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    created_date = sqlalchemy.Column(sqlalchemy.DateTime, default=datetime.datetime.now)
    avatar_id = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey("avatar.id"))

    que = orm.relationship("Question", back_populates='user')
    comm = orm.relationship("Comment", back_populates='user')
    like = orm.relationship("Like", back_populates='user')
    favorite = orm.relationship("Favorite", back_populates='user')
    avatar = orm.relationship("Avatar", back_populates='user')

    def set_password(self, password):
        self.hashed_password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.hashed_password, password)

    def get_data(self):
        return {
            'name': self.name,
            'lastname': self.lastname,
            'about': self.about
        }

