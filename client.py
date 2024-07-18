import socket
import threading


class Client:
    def __init__(self, host='localhost', port=65432):
        self.host = host
        self.port = port
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def connect(self):
        self.client_socket.connect((self.host, self.port))
        print(f'Connected to server at {self.host}:{self.port}')
        threading.Thread(target=self.receive_keys).start()
        threading.Thread(target=self.send_command).start()

    def send_command(self):
        commands = ["move 100 200", "click", "move 300 400", "scroll -10"]
        for command in commands:
            self.client_socket.sendall(command.encode())

    def receive_keys(self):
        try:
            while True:
                data = self.client_socket.recv(1024)
                if data:
                    print(f'Received key: {data.decode()}')
                else:
                    break
        except ConnectionError:
            print("Connection to server lost.")
        finally:
            self.client_socket.close()


if __name__ == "__main__":
    client = Client()
    client.connect()
