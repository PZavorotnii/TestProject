import datetime
import sqlalchemy
from .db_session import SqlAlchemyBase
from sqlalchemy import orm


class Answers(SqlAlchemyBase):
    __tablename__ = 'answers'
    id = sqlalchemy.Column(sqlalchemy.INTEGER, primary_key=True, autoincrement=True)
    '''word_1 = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey("variants.c.id"))
    word_1_id = orm.relationship('Variants', foreign_keys="variants.c.id")
    word_2 = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey("variants.c.id"))
    word_2_id = orm.relationship('Variants', foreign_keys="variants.c.id")
    word_3 = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey("variants.c.id"))
    word_3_id = orm.relationship('Variants', foreign_keys="variants.c.id")
    word_4 = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey("variants.c.id"))
    word_4_id = orm.relationship('Variants', foreign_keys="variants.c.id")
    word_5 = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey("variants.c.id"))
    word_5_id = orm.relationship('Variants', foreign_keys="variants.c.id")
    test = orm.relationship('Tests', back_populates='answ')'''
