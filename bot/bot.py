import websocket
import time

from models.user import User
from models.tokens import Token
from http_service.auth import Auth
from http_service.room import Room
from http_service.game import Game
from multiprocessing import RLock
from threading import Thread


class Bot:
    gs_id = ''
    gs_token = ''

    def __init__(self, user_id: int, dictionary: dict, rlock: RLock):
        self.token = None
        self.user = User.get_by_id(user_id)
        self.dictionary = dictionary
        self.rlock = rlock

    def auth(self):
        token = Auth(self.user).signin()
        if token != 0:
            Token.delete().where(Token.user_id == self.user.id).execute()
            self.token = Token.create(user=self.user,
                                      user_id=self.user.id,
                                      access_token=token['access_token'],
                                      refresh_token=token['refresh_token'],
                                      service_user_id=token['service_user_id'])

    def join_room(self):
        self.resolve()
        if self.gs_token != '':
            return

        room_object = Room(self.token)
        with self.rlock:
            if self.dictionary['room_id'] == '':
                room = room_object.create()
                if room == 0:
                    self.rlock.release()
                    self.join_room()
                self.dictionary['room_id'] = room['room_id']
            else:
                room_object.join(self.dictionary['room_id'])

    def resolve(self):
        if self.gs_token != '':
            return

        game_object = Game(self.token)
        gs_object = game_object.resolve()
        if gs_object != 0:
            self.gs_token = gs_object['gs_token']
            self.gs_id = gs_object['gs_id']

    def __game_url(self):
        game_url = 'wss://gs{}.monopoly-one.com/ws?gs_token={}'
        return game_url.format(self.gs_id, self.gs_token)

    def on_message(self, ws, message):
        def run(*args):
            print(message)
            print("Message received...")
            time.sleep(1)

        Thread(target=run).start()

    def __socket(self, dictionary):
        while self.gs_id == '' and self.gs_token == '':
            self.resolve()
        ws = websocket.WebSocketApp(self.__game_url(), on_data=self.on_message, on_message=self.on_message)
        ws.run_forever()

    def socket_listen(self):
        print(self.user.email)
        socket_process = Thread(target=self.__socket, args=(self.dictionary,))
        socket_process.start()
        socket_process.join()
