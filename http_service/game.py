import requests
from models.tokens import Token


class Game:
    execute_url: str = 'https://monopoly-one.com/api/execute.games'
    resolve_url: str = 'https://monopoly-one.com/api/games.resolve'

    def __init__(self, token: Token):
        self.token = token

    def __execute_request(self):
        auth_object = {
            'access_token': self.token.access_token
        }
        return requests.post(self.execute_url, auth_object).json()

    def __execute(self):
        request_data = self.__execute_request()

        rooms = request_data['result']['rooms']
        if rooms.get('current_game') is None:
            return 0

        return {
            'gs_id': rooms['current_game']['gs_id'],
            'gs_game_id': rooms['current_game']['gs_game_id']
        }

    def __resolve_request(self):
        join_object = self.__execute()
        if join_object == 0:
            return {
                'code': -1
            }
        join_object['access_token'] = self.token.access_token
        resolve_result = requests.post(self.resolve_url, join_object).json()
        resolve_result['data']['gs_id'] = join_object['gs_id']
        return resolve_result

    def resolve(self):
        request_data = self.__resolve_request()
        if request_data['code'] != 0:
            return 0

        return {
            'gs_id': request_data['data']['gs_id'],
            'gs_token': request_data['data']['gs_token']
        }

