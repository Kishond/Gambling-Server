import enum
from enum import Enum, auto
from Roulette import Roulette
from coin_flip import CoinFlip

class Game(Enum):
    ROULETTE = auto()
    COIN_FLIP = auto()

class Protocol:
    @staticmethod
    def create_server_reply(game, balance, has_won, message):
        reply =  f" {balance} {has_won} {message}"
        match game:
            case Game.ROULETTE:
                return Game.ROULETTE.name + reply
            case Game.COIN_FLIP:
                return Game.COIN_FLIP.name + reply
            case _:
                return "Error unknown game"

    @staticmethod
    def create_server_error_reply():
        return -1

    @staticmethod
    def handle_server_command_reply(server_reply):
        print(server_reply)

    @staticmethod
    def handle_server_reply(reply):
        if reply.startswith("!"):
            Protocol.handle_server_command_reply(reply)
        elif reply != str(-1):
            if reply == "1":
                print("Sorry, your bet can't be greater than your balance.")
            else:
                Protocol.handle_game_reply(reply)
        else:
            print("Invalid Request")

    @staticmethod
    def handle_game_reply(reply):
        game, balance, has_won, message = reply.split(" ")
        match game:
            case Game.ROULETTE.name:
                if Roulette.is_a_number(message):
                    Roulette.start_roulette(message, balance, has_won)
                else:
                    Roulette.start_roulette(Roulette.get_random_number_by_color(message), balance, has_won)
            case Game.COIN_FLIP.name:
                CoinFlip.coin_flip_animation(message, balance, has_won)

