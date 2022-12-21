from peewee import Model
from db_connection import DbConnection


class BaseModel(Model):
    class Meta:
        database = DbConnection().connection
