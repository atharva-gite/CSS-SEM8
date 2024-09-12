import socket
import threading
from Crypto.PublicKey import RSA

class ThirdParty:
    def __init__(self, host='localhost', port=4444):
        self.host = host
        self.port = port
        self.registered_keys = {}

    def start(self):
        server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server.bind((self.host, self.port))
        server.listen()

        print(f"Third Party Entity listening on {self.host}:{self.port}")

        while True:
            client, address = server.accept()
            thread = threading.Thread(target=self.handle_client, args=(client,))
            thread.start()

    def handle_client(self, client):
        while True:
            try:
                message = client.recv(1024).decode('utf-8')
                if message.startswith("REGISTER"):
                    _, identity, public_key = message.split(":", 2)
                    self.registered_keys[identity] = public_key
                    client.send("Registration successful".encode('utf-8'))
                elif message.startswith("GET"):
                    _, identity = message.split(":")
                    if identity in self.registered_keys:
                        client.send(self.registered_keys[identity].encode('utf-8'))
                    else:
                        client.send("Identity not found".encode('utf-8'))
                else:
                    client.send("Invalid request".encode('utf-8'))
            except:
                break
        client.close()

if __name__ == "__main__":
    third_party = ThirdParty()
    third_party.start()