import datetime
import sqlalchemy
from .db_session import SqlAlchemyBase
from sqlalchemy import orm


class Tests(SqlAlchemyBase):
    __tablename__ = 'tests'
    id = sqlalchemy.Column(sqlalchemy.INTEGER, primary_key=True, autoincrement=True)
    #user_id = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey("users.c.id"))
    #user = orm.relationship('User')
    #answers = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey("answers.c.id"))
    #answ = orm.relationship('Answers')
    words = sqlalchemy.Column(sqlalchemy.Integer)
    date = sqlalchemy.Column(sqlalchemy.DateTime, default=datetime.datetime.now)
    is_successful = sqlalchemy.Column(sqlalchemy.Boolean)
