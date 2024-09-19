import socket
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend
from hashlib import sha256
import random
P = 23  # A prime number
G = 9   # A primitive root modulo of P


def generate_dh_key():
    private_key = random.randint(1, P-1)  # Generate private key
    public_key = pow(G, private_key, P)   # Calculate public key
    return private_key, public_key


def compute_shared_key(private_key, public_key_other):
    shared_key = pow(public_key_other, private_key, P)
    return shared_key


def decrypt_message(key, ciphertext):
    aes_key = sha256(str(key).encode()).digest()

    cipher = Cipher(algorithms.AES(aes_key), modes.ECB(),
                    backend=default_backend())
    decryptor = cipher.decryptor()

    decrypted_message = decryptor.update(ciphertext) + decryptor.finalize()

    return decrypted_message.decode().strip()


def read_encrypted_message(filename):
    with open(filename, 'rb') as file:
        encrypted_message = file.read()
    print(f"Encrypted message read from {filename}")
    return encrypted_message


def receiver_program():
    private_key = None
    public_key = None
    shared_key = None

    # Create a socket
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(('localhost', 3333))
    server_socket.listen(1)

    print("Receiver is waiting for connection...")
    client_socket, addr = server_socket.accept()
    print(f"Connected to sender: {addr}")

    while True:
        # Wait for either key exchange or encrypted message
        data = client_socket.recv(1024).decode()

        if data.isdigit():
            # Key exchange
            sender_public_key = int(data)
            print(f"Received sender's public key: {sender_public_key}")

            if private_key is None or public_key is None:
                private_key, public_key = generate_dh_key()
            print("Sending public key to sender...")
            client_socket.send(str(public_key).encode())

            shared_key = compute_shared_key(private_key, sender_public_key)
            print(f"Shared key generated: {shared_key}")

        elif data == 'Message sent.':
            # Receive and decrypt the message
            if shared_key is None:
                print("Shared key not generated yet.")
            else:
                encrypted_message = read_encrypted_message(
                    'encrypted_message.bin')
                decrypted_message = decrypt_message(
                    shared_key, encrypted_message)
                print(f"Decrypted message: {decrypted_message}")

        elif data == 'exit':
            print("Exiting the program...")
            client_socket.close()
            break

        else:
            print(f"Received unexpected data: {data}")


if __name__ == '__main__':
    receiver_program()
