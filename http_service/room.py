import requests
from models.tokens import Token


class Room:
    create_url: str = 'https://monopoly-one.com/api/rooms.create'
    join_url: str = 'https://monopoly-one.com/api/rooms.join'

    def __init__(self, token: Token):
        self.token = token

    def __create_request(self):
        auth_object = {
                'game_submode': 0,
                'maxplayers': 4,
                'option_private': 1,
                'option_autostart': 1,
                'access_token': self.token.access_token
        }
        return requests.post(self.create_url, auth_object).json()

    def create(self):
        request_data = self.__create_request()
        if request_data['code'] != 0:
            return 0

        return {
            'room_id': request_data['data']['room_id']
        }

    def __join_request(self, room_id):
        join_object = {
            'room_id': room_id,
            "access_token": self.token.access_token
        }
        return requests.post(self.join_url, join_object).json()

    def join(self, room_id):
        request_data = self.__join_request(room_id)
        if request_data['code'] != 0:
            return 0

        return 1

