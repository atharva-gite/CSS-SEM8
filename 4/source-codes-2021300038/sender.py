import socket
import random
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend
from hashlib import sha256

P = 23  # A prime number
G = 9   # A primitive root modulo of P


def generate_dh_key():
    private_key = random.randint(1, P-1)  # Generate private key
    public_key = pow(G, private_key, P)   # Calculate public key
    return private_key, public_key


def compute_shared_key(private_key, public_key_other):
    shared_key = pow(public_key_other, private_key, P)
    return shared_key


def encrypt_message(key, plaintext):
    aes_key = sha256(str(key).encode()).digest()

    cipher = Cipher(algorithms.AES(aes_key), modes.ECB(),
                    backend=default_backend())
    encryptor = cipher.encryptor()

    padding_length = 16 - len(plaintext) % 16
    plaintext += ' ' * padding_length

    ciphertext = encryptor.update(plaintext.encode()) + encryptor.finalize()
    return ciphertext


def save_encrypted_message(filename, encrypted_message):
    with open(filename, 'wb') as file:
        file.write(encrypted_message)
    print(f"Encrypted message saved to {filename}")


def sender_program():
    private_key = None
    public_key = None
    shared_key = None

    # Create a socket
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect(('localhost', 3333))

    print("Connected to the receiver.")

    while True:
        print("\n--- MENU ---")
        print("1. Generate Diffie-Hellman key")
        print("2. Send an encrypted message")
        print("3. Exit")
        choice = input("Choose an option: ")

        if choice == '1':
            # Generate and exchange keys
            private_key, public_key = generate_dh_key()
            print("Sending public key to receiver...")
            client_socket.send(str(public_key).encode())

            receiver_public_key = int(client_socket.recv(1024).decode())
            print(f"Received receiver's public key: {receiver_public_key}")

            shared_key = compute_shared_key(private_key, receiver_public_key)
            print(f"Shared key generated: {shared_key}")

        elif choice == '2':
            if shared_key is None:
                print("You must generate a shared key first (Option 1).")
            else:
                message = input("Enter a message (1000+ characters): ")
                encrypted_message = encrypt_message(shared_key, message)

                # Save the encrypted message to a file
                save_encrypted_message(
                    'encrypted_message.bin', encrypted_message)

                # Notify receiver that the message is saved
                client_socket.send(b'Message sent.')

        elif choice == '3':
            print("Exiting the program...")
            client_socket.send(b'exit')
            client_socket.close()
            break

        else:
            print("Invalid choice. Please try again.")


if __name__ == '__main__':
    sender_program()
