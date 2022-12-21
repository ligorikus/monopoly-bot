import json
from models.user import User
from models.tokens import Token
from db_connection import DbConnection
from http_service.auth import Auth


def init_users():
    users = json.load(open('users.json'))
    User.insert_many(users).execute()


def create_tables():
    (DbConnection()).connection.create_tables([User, Token])


def main():
    user = User.get_by_id(1)
    token = Auth(user).signin()
    if token != 0:
        Token.delete().where(Token.user_id == user.id).execute()
        Token.create(user=user,
                     user_id=user.id,
                     access_token=token['access_token'],
                     refresh_token=token['refresh_token'],
                     service_user_id=token['service_user_id'])