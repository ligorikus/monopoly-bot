from peewee import *
from models.base import BaseModel
from models.user import User


class Token(BaseModel):
    id = AutoField(column_name='id')
    user_id = ForeignKeyField(User, column_name='user_id', backref='users')
    access_token = TextField(column_name='access_token')
    refresh_token = TextField(column_name='refresh_token')
    service_user_id = IntegerField(column_name='service_user_id')

    class Meta:
        table_name = 'tokens'
