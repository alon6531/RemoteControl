import pygame
import socket
import threading
import io
from PIL import Image
import keyboard


class Server:
    client_socket = 0

    def __init__(self, host='192.168.1.212', port=12345, screen_size=(1920, 1080)):

        def init_tcp_socket():
            self.server_tcp_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.server_tcp_socket.bind((host, port))
            self.server_tcp_socket.listen(5)
            print(f'Server listening on {host}:{port}')

        def init_udp_socket():
            self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            self.sock.bind((host, port))

        def init_pygame():
            pygame.init()
            self.screen = pygame.display.set_mode(screen_size)

        init_tcp_socket()

        init_udp_socket()

        init_pygame()

        self.accept_connections()

    def accept_connections(self):
        threading.Thread(target=self.display_image).start()
        threading.Thread(target=self.keyboard).start()
        while True:
            self.client_socket, client_address = self.server_tcp_socket.accept()
            print(f'Connection from {client_address}')

    def display_image(self):
        def receive_large_message():
            data = bytearray()
            while True:
                chunk, _ = self.sock.recvfrom(65507)  # Adjust buffer size if necessary
                if not chunk:
                    break
                data.extend(chunk)
                # Simple heuristic to detect end of message; adjust if necessary
                if len(chunk) < 65507:
                    break
            return bytes(data)

        while True:
            image_data = receive_large_message()
            if image_data:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        raise SystemExit
                try:
                    # Open the image from the byte data
                    image = Image.open(io.BytesIO(image_data))

                    # Convert PIL image to Pygame surface
                    pygame_image = pygame.image.fromstring(image.tobytes(), image.size, image.mode)

                    # Display the image on the Pygame screen
                    self.screen.blit(pygame_image, (0, 0))
                    pygame.display.flip()
                except Exception as e:
                    print(f"Error displaying image: {e}")

    def keyboard(self):
        def on_key_event(event):
            key = event.name
            self.client_socket.sendall(key.encode())
            print(f'Sent key: {key}')

        print("Press ESC to stop capturing keys.")
        keyboard.on_press(on_key_event)
        keyboard.wait('esc')


if __name__ == "__main__":
    server = Server()