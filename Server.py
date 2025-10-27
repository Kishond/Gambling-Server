import socket
from contextlib import nullcontext
import random
import asyncio
from User import User
from Protocol import Game, Protocol


class Server:

    def __init__(self, listen_address, port):
        self.listen_address = listen_address
        self.port = port
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.bind((listen_address, port))
        self.commands = ["ROULETTE", "COINFLIP", ]

    async def start(self):
        self.socket.listen()
        self.socket.setblocking(False)
        print(f"the server is up and running and listening on {self.listen_address}")
        loop = asyncio.get_running_loop()
        while True:
            (client_socket, client_address) = await loop.sock_accept(self.socket)
            asyncio.create_task(self.handle_request(client_socket, client_address))

    async def handle_request(self, client_socket, client_address):
        user = nullcontext
        loop_number = 0
        print("Client connected")
        while True:
            loop = asyncio.get_running_loop()
            length = (await loop.sock_recv(client_socket, 4)).decode()
            data = (await loop.sock_recv(client_socket, int(length))).decode()
            if loop_number == 1:
                user = User(data)
            if data == "EXIT":
                return self.end(client_socket)
            response = str(self.get_response(data, loop_number, user))
            response_length = len(str(response))
            print("Client sent: " + data)
            reply = str(response_length).zfill(4) + response
            client_socket.send(str(reply).encode())
            loop_number += 1

    def end(self, client_socket):
        self.socket.close()
        client_socket.close()

    def get_response(self, data, loop_number, user):
        if loop_number == 0:
            return ("Welcome user to Kishonzino please enter your username in order to proceed with your mega betting"
                    + "on mama")
        if loop_number == 1:
            return (f"Dear {user.get_name()} You have been registered you have been granted 500 tokens "
                    "if you like you may send !h to view full commands of the Kishonzino")
        data = data.upper().strip().split(" ")

        if self.is_data_valid(data):
            command = data[0]
            bet = int(data[1])
            parameter = data[2]
            if bet > user.get_balance():
                return "1"
            if command == "ROULETTE":
                return Server.roulette_handler(bet, parameter, user)

            if command == "COINFLIP":
                return Server.coin_flip_handler(bet, parameter, user)

        if data[0].startswith("!") and len(data[0]) > 1:
            command = data[1:]
            if command == "BALANCE":
                return user.get_balance()

            if command == "TOTALPROFIT":
                return user.get_total_profit()

        return Protocol.create_server_error_reply()

    def is_data_valid(self, data):
        return (len(data) == 3
                and data[0] in self.commands
                and data[1].isdigit())


    @staticmethod
    def roulette_handler(bet, parameter, user):
        if not Server.is_roulette_parameter_valid(parameter):
            return Protocol.create_server_error_reply()
        user.remove_balance(bet)

        total_tokens, winning_sign, has_won = Server.roulette(bet, parameter)
        user.add_balance(total_tokens)
        return Protocol.create_server_reply(Game.ROULETTE, user.get_balance()
                                            , has_won, winning_sign)

    @staticmethod
    def is_roulette_parameter_valid(parameter):
        return (parameter in ["BLACK", "RED", "GREEN"]
                or (parameter.isdigit() and 36 >= int(parameter) > 0))

    @staticmethod
    def roulette(bet, parameter):
        winning_color = random.choice(["BLACK", "RED"])
        if parameter in ["BLACK","RED"]:
            return (bet * 2, winning_color, True) if winning_color == parameter else (0, winning_color, False)
        winning_number = random.randint(0, 36)
        if parameter == "GREEN":
            return (bet * 36, "GREEN", True) if winning_number == 0 else (0, winning_color, False)
        if 36 >= int(parameter) > 0:
            return (bet * 36, winning_number, True) if winning_number == parameter\
                else (0, winning_number, False)
        return 0, False

    @staticmethod
    def coin_flip_handler(bet, parameter, user):
        if not Server.is_coin_flip_parameter_valid(parameter):
            return Protocol.create_server_error_reply()
        user.remove_balance(bet)

        total_tokens, winning_coin, has_won = Server.coin_flip(parameter, bet)
        user.add_balance(total_tokens)
        return Protocol.create_server_reply(Game.COIN_FLIP, user.get_balance(), has_won, winning_coin)

    @staticmethod
    def is_coin_flip_parameter_valid(parameter):
        return parameter in ["HEADS", "TAILS"]

    @staticmethod
    def coin_flip(coin, bet):
        winning_coin = random.choice(['HEADS', 'TAILS'])
        if winning_coin == coin:
            return bet * 2, winning_coin, True
        return 0, winning_coin, False

def main():
    server = Server("0.0.0.0", 8810)
    asyncio.run(server.start())

if __name__ == "__main__":
    main()
