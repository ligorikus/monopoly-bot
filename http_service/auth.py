import requests
from models.user import User


class Auth:
    signin_url: str = 'https://monopoly-one.com/api/auth.signin'

    def __init__(self, user: User):
        self.user = user

    def __signin_request(self):
        auth_object = {
            'email': self.user.email,
            'password': self.user.password
        }
        return requests.post(self.signin_url, auth_object).json()

    def signin(self):
        request_data = self.__signin_request()
        if request_data['code'] != 0:
            return 0

        return {
            'access_token': request_data['data']['access_token'],
            'refresh_token': request_data['data']['refresh_token'],
            'service_user_id': request_data['data']['user_id']
        }
