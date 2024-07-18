import socket
import keyboard
import threading
import pyautogui

class Server:
    client_socket = 0
    host = 0

    def __init__(self, host='192.168.1.212', port=6531):
        self.host = host
        self.port = port
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.connections = []
        self.running = False

    def start(self):
        self.server_socket.bind((self.host, self.port))
        self.server_socket.listen(5)
        print(f'Server listening on {self.host}:{self.port}')
        self.running = True
        self.accept_connections()

    def accept_connections(self):
        while self.running:
            self.client_socket, client_address = self.server_socket.accept()
            self.connections.append(self.client_socket)
            print(f'Connection from {client_address}')
            threading.Thread(target=self.keyboard).start()
            threading.Thread(target=self.mouse).start()

    def keyboard(self):
        def on_key_event(event):
            key = event.name
            self.client_socket.sendall(key.encode())
            print(f'Sent key: {key}')

        print("Press ESC to stop capturing keys.")
        keyboard.on_press(on_key_event)
        keyboard.wait('esc')

    def mouse(self):
        while True:
            left_click = pyautogui.mouseDown(button='left')
            right_click = pyautogui.mouseDown(button='right')
            message = f"MOUSE {x} {y} {left_click} {right_click}"
            self.client_socket.sendall(message.encode())

        pyautogui.sleep(1)  # Send commands at intervals

    def handle(self):
        print("hellow")

    def stop(self):
        self.running = False
        for conn in self.connections:
            conn.close()
        self.server_socket.close()

if __name__ == "__main__":
    server = Server()
    try:
        server.start()
    except KeyboardInterrupt:
        print("Server stopped by user.")
    finally:
        server.stop()