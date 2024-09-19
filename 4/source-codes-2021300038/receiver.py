import socket
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

# Function to decrypt a message using AES


def decrypt_message(key, ciphertext):
    # Hash the shared key to create a 256-bit key for AES
    aes_key = sha256(str(key).encode()).digest()

    # Initialize AES cipher in ECB mode
    cipher = Cipher(algorithms.AES(aes_key), modes.ECB(),
                    backend=default_backend())
    decryptor = cipher.decryptor()

    decrypted_message = decryptor.update(ciphertext) + decryptor.finalize()

    # Remove padding
    return decrypted_message.decode().strip()

# Receiver (Server) implementation


def receiver_program():
    private_key, public_key = generate_dh_key()

    # Create a socket
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(('localhost', 3333))
    server_socket.listen(1)

    print("Receiver is waiting for connection...")
    client_socket, addr = server_socket.accept()
    print(f"Connected to sender: {addr}")

    # Exchange public keys
    sender_public_key = int(client_socket.recv(1024).decode())
    print(f"Received sender's public key: {sender_public_key}")

    print("Sending public key to sender...")
    client_socket.send(str(public_key).encode())

    # Compute shared key
    shared_key = compute_shared_key(private_key, sender_public_key)
    print(f"Shared key generated: {shared_key}")

    # Receive encrypted message
    encrypted_message = client_socket.recv(1024)
    decrypted_message = decrypt_message(shared_key, encrypted_message)

    print(f"Decrypted message: {decrypted_message}")

    client_socket.close()


if __name__ == '__main__':
    receiver_program()
