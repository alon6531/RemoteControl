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
            if parts[0] == "MOUSE":
                x, y = int(parts[1]), int(parts[2])
                left_click = parts[3] == 'True'
                right_click = parts[4] == 'True'

                pyautogui.moveTo(x, y)

                if left_click:
                    pyautogui.mouseDown(button='left')
                else:
                    pyautogui.mouseUp(button='left')

                if right_click:
                    pyautogui.mouseDown(button='right')
                else:
                    pyautogui.mouseUp(button='right')

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
