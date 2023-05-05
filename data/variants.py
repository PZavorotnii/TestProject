import datetime
import sqlalchemy
from .db_session import SqlAlchemyBase
from sqlalchemy import orm


class Variants(SqlAlchemyBase):
    __tablename__ = 'variants'
    id = sqlalchemy.Column(sqlalchemy.INTEGER, primary_key=True, autoincrement=True)
    word = sqlalchemy.Column(sqlalchemy.String, unique=True)
    parent_id = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey("words.id"))
    parent = orm.relationship('Words')
    is_right = sqlalchemy.Column(sqlalchemy.Boolean)
