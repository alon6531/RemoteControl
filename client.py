import threading

import pygame
import socket
import io
from PIL import ImageGrab


class Client:

    def __init__(self, host='127.0.0.1', port=12345, screen_size=(800, 600)):

        def init_tcp_socket():
            self.client_tcp_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            print(f'Server listening on {host}:{port}')
            self.client_tcp_socket.connect((host, port))
            print(f'Connected to server at {host}:{port}')

        def init_udp_socket():
            self.host = host
            self.port = port
            self.client_udp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            self.MAX_UDP_SIZE = 65507  # Maximum UDP payload size

        def init_pygame():
            pygame.init()
            self.screen = pygame.display.set_mode(screen_size)

        init_tcp_socket()
        init_udp_socket()
        init_pygame()

        threading.Thread(target=self.capture_screen).start()
        threading.Thread(target=self.receive_keys).start()

    def capture_screen(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    raise SystemExit
            # Capture the screen using Pillow
            image = ImageGrab.grab()

            # Convert image to bytes
            byte_arr = io.BytesIO()
            image.save(byte_arr, format='PNG')

            def send_large_message(data):
                # Split data into chunks and send
                chunk_size = self.MAX_UDP_SIZE
                for i in range(0, len(data), chunk_size):
                    self.client_udp_socket.sendto(data[i:i + chunk_size], (self.host, self.port))

            send_large_message(byte_arr.getvalue())

    def receive_keys(self):
        try:
            while True:
                data = self.client_tcp_socket.recv(1024)
                if data:
                    print(f'Received key: {data.decode()}')
                else:
                    break
        except ConnectionError:
            print("Connection to server lost.")
        finally:
            self.client_tcp_socket.close()




if __name__ == "__main__":
    client = Client()
