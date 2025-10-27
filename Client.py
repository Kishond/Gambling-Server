import socket
from Roulette import Roulette
from Protocol import Protocol

class Client:

    def __init__(self, target_ip, target_port):
        self.target_ip = target_ip
        self.target_port = target_port
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def start(self):
        self.client_socket.connect((self.target_ip, self.target_port))

        message = input("Enter message to send to server (type 'exit' to quit): ")
        loop_number = 0
        while True:
            message_length = str(len(message)).zfill(4)
            self.client_socket.send((message_length + message).encode())
            length = self.client_socket.recv(4)
            reply = self.client_socket.recv(int(length)).decode()
            if loop_number <= 1:
                print(reply)
            else:
                Protocol.handle_server_reply(reply)
            if message == "exit":
                return self.end()
            message = input("Enter message to send to server (type 'exit' to quit): ")
            loop_number += 1


    def end(self):
        self.client_socket.close()
        print("client has successfully exited")

def main():
    client = Client("127.0.0.1", 8810)
    client.start()

if __name__ == "__main__":
    main()