from peewee import *
from models.base import BaseModel


class User(BaseModel):
    id = AutoField(column_name='id')
    email = TextField(column_name='email', unique=True)
    password = TextField(column_name='password')

    class Meta:
        table_name = 'users'
