from multiprocessing import Process, Manager, Array, RLock
from bot.bot import Bot


def bot(user_id: int, dictionary: dict, rlock: RLock):
    current_bot = Bot(user_id, dictionary, rlock)
    current_bot.auth()
    current_bot.join_room()
    print(user_id)
    current_bot.socket_listen()


def main():
    with Manager() as manager:
        dictionary = manager.dict({
            'room_id': '',
            'game_state': None
        })
        rlock = manager.RLock()
        for user_id in range(1, 5):
            th = Process(target=bot, args=(user_id, dictionary, rlock))
            th.start()
            th.join()


if __name__ == '__main__':
    main()
