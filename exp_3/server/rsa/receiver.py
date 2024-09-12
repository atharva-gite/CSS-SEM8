import socket
import threading
from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP, AES

class Receiver:
    def __init__(self, host='localhost', port=3333, third_party_host='localhost', third_party_port=4444):
        self.host = host
        self.port = port
        self.third_party_host = third_party_host
        self.third_party_port = third_party_port
        self.identity = None
        self.key_pair = None

    def register(self):
        self.identity = input("Enter your identity: ")
        self.key_pair = RSA.generate(2048)
        public_key = self.key_pair.publickey().export_key().decode()

        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.connect((self.third_party_host, self.third_party_port))
            s.send(f"REGISTER:{self.identity}:{public_key}".encode('utf-8'))
            response = s.recv(1024).decode('utf-8')
            print(response)

    def receive_messages(self):
        server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server.bind((self.host, self.port))
        server.listen()

        print(f"Receiver listening on {self.host}:{self.port}")

        while True:
            client, address = server.accept()
            thread = threading.Thread(target=self.handle_message, args=(client,))
            thread.start()

    def handle_message(self, client):
        data = client.recv(4096)
        encrypted_symmetric_key = data[:256]
        nonce = data[256:272]
        tag = data[272:288]
        ciphertext = data[288:]

        # Decrypt symmetric key
        cipher_rsa = PKCS1_OAEP.new(self.key_pair)
        symmetric_key = cipher_rsa.decrypt(encrypted_symmetric_key)

        # Decrypt message
        cipher_aes = AES.new(symmetric_key, AES.MODE_EAX, nonce)
        message = cipher_aes.decrypt_and_verify(ciphertext, tag).decode('utf-8')

        print(f"Received message: {message}")

    def run(self):
        while True:
            print("\n1. Register")
            print("2. Start receiving messages")
            print("3. Exit")
            choice = input("Enter your choice: ")

            if choice == '1':
                self.register()
            elif choice == '2':
                thread = threading.Thread(target=self.receive_messages)
                thread.start()
            elif choice == '3':
                break
            else:
                print("Invalid choice")

if __name__ == "__main__":
    receiver = Receiver()
    receiver.run()