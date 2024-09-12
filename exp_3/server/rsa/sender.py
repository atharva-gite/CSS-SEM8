import socket
from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP, AES
from Crypto.Random import get_random_bytes

class Sender:
    def __init__(self, third_party_host='localhost', third_party_port=4444, receiver_host='localhost', receiver_port=3333):
        self.third_party_host = third_party_host
        self.third_party_port = third_party_port
        self.receiver_host = receiver_host
        self.receiver_port = receiver_port
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

    def send_message(self):
        receiver_identity = input("Enter receiver's identity: ")
        message = input("Enter your message: ")

        # Get receiver's public key
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.connect((self.third_party_host, self.third_party_port))
            s.send(f"GET:{receiver_identity}".encode('utf-8'))
            receiver_public_key = s.recv(1024).decode('utf-8')

        if receiver_public_key == "Identity not found":
            print("Receiver not registered")
            return

        # Generate and encrypt symmetric key
        symmetric_key = get_random_bytes(32)
        rsa_key = RSA.import_key(receiver_public_key)
        cipher_rsa = PKCS1_OAEP.new(rsa_key)
        encrypted_symmetric_key = cipher_rsa.encrypt(symmetric_key)

        # Encrypt message
        cipher_aes = AES.new(symmetric_key, AES.MODE_EAX)
        ciphertext, tag = cipher_aes.encrypt_and_digest(message.encode('utf-8'))

        # Send to receiver
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.connect((self.receiver_host, self.receiver_port))
            s.send(encrypted_symmetric_key + cipher_aes.nonce + tag + ciphertext)

        print("Message sent successfully")

    def run(self):
        while True:
            print("\n1. Register")
            print("2. Send message")
            print("3. Exit")
            choice = input("Enter your choice: ")

            if choice == '1':
                self.register()
            elif choice == '2':
                self.send_message()
            elif choice == '3':
                break
            else:
                print("Invalid choice")

if __name__ == "__main__":
    sender = Sender()
    sender.run()