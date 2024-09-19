import socket
import random
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend
from hashlib import sha256

# Diffie-Hellman Key Exchange Parameters
P = 23  # A prime number
G = 9   # A primitive root modulo of P

# Function to generate a Diffie-Hellman key


def generate_dh_key():
    private_key = random.randint(1, P-1)  # Generate private key
    public_key = pow(G, private_key, P)   # Calculate public key
    return private_key, public_key

# Function to compute shared key using the other party's public key


def compute_shared_key(private_key, public_key_other):
    shared_key = pow(public_key_other, private_key, P)
    return shared_key

# Function to encrypt a message using AES


def encrypt_message(key, plaintext):
    # Hash the shared key to create a 256-bit key for AES
    aes_key = sha256(str(key).encode()).digest()

    # Initialize AES cipher in ECB mode
    cipher = Cipher(algorithms.AES(aes_key), modes.ECB(),
                    backend=default_backend())
    encryptor = cipher.encryptor()

    # Pad the plaintext to a multiple of 16 bytes
    padding_length = 16 - len(plaintext) % 16
    plaintext += ' ' * padding_length

    ciphertext = encryptor.update(plaintext.encode()) + encryptor.finalize()
    return ciphertext

# Sender (Client) implementation


def sender_program():
    private_key, public_key = generate_dh_key()

    # Create a socket
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect(('localhost', 3333))

    print("Connected to the receiver.")

    # Exchange public keys
    print("Sending public key to receiver...")
    client_socket.send(str(public_key).encode())

    receiver_public_key = int(client_socket.recv(1024).decode())
    print(f"Received receiver's public key: {receiver_public_key}")

    # Compute shared key
    shared_key = compute_shared_key(private_key, receiver_public_key)
    print(f"Shared key generated: {shared_key}")

    # Send a large message
    message = input("Enter a message (1000+ characters): ")
    encrypted_message = encrypt_message(shared_key, message)

    # Send encrypted message
    client_socket.send(encrypted_message)
    print("Encrypted message sent.")

    client_socket.close()


if __name__ == '__main__':
    sender_program()
