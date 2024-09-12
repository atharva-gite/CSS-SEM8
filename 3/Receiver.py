import socket
import pickle
from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP, AES


def register_identity(identity, public_key):
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect(('localhost', 4444))
    request = {'type': 'register',
               'identity': identity, 'public_key': public_key}
    client.send(pickle.dumps(request))
    response = client.recv(1024)
    print(response.decode())
    client.close()


def receive_message(private_key):
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind(('localhost', 3333))
    server.listen(5)
    print("Waiting for messages...")

    while True:
        client_socket, addr = server.accept()
        data = client_socket.recv(4096)
        received_data = pickle.loads(data)

        # Step 1: Decrypt the symmetric key using the private key
        rsa_cipher = PKCS1_OAEP.new(private_key)
        symmetric_key = rsa_cipher.decrypt(received_data['encrypted_key'])

        # Step 2: Decrypt the message using the symmetric key
        aes_cipher = AES.new(symmetric_key, AES.MODE_EAX,
                             nonce=received_data['nonce'])
        plaintext = aes_cipher.decrypt(received_data['ciphertext'])

        print("Received message:", plaintext.decode())
        client_socket.close()


def menu(identity, private_key, public_key):
    while True:
        print("\n--- Receiver Menu ---")
        print("1. Register identity")
        print("2. Wait for messages")
        print("3. Exit")

        choice = input("Enter your choice: ")

        if choice == '1':
            register_identity(identity, public_key)
        elif choice == '2':
            print("Receiver is waiting for messages...")
            receive_message(private_key)
        elif choice == '3':
            print("Exiting receiver service...")
            break
        else:
            print("Invalid choice! Please try again.")


if __name__ == '__main__':
    identity = 'vedant'
    key = RSA.generate(2048)
    public_key = key.publickey().export_key()

    # Start the menu
    menu(identity, RSA.import_key(key.export_key()), public_key)
