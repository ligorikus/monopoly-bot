from singleton import *
from peewee import SqliteDatabase


class DbConnection(metaclass=Singleton):
    def __init__(self):
        self.connection = SqliteDatabase('monopoly.db')
