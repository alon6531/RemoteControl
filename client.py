import socket
import threading
import pyautogui


class Client:
    host = 0

    def __init__(self, host='192.168.1.212', port=6531):
        self.host = host
        self.port = port
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def connect(self):
        self.client_socket.connect((self.host, self.port))
        print(f'Connected to server at {self.host}:{self.port}')
        threading.Thread(target=self.receive_keys).start()
        threading.Thread(target=self.handle_mouse).start()

    def handle_mouse(self):
        while True:
            command = self.client_socket.recv(1024).decode()
            parts = command.split()
            if parts[0] == "MOVE":
                x, y = int(parts[1]), int(parts[2])
                pyautogui.moveTo(x, y)
            elif parts[0] == "CLICK":
                button = parts[1].lower()
                state = parts[2].lower()
                if state == 'down':
                    pyautogui.mouseDown(button=button)
                elif state == 'up':
                    pyautogui.mouseUp(button=button)

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
