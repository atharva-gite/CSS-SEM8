import socket
import random
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
import base64

def generate_key(p, g, a):
    return pow(g, a, p)

def encrypt_message(key, message):
    key = key.to_bytes(32, byteorder='big')
    cipher = AES.new(key, AES.MODE_ECB)
    padded_message = pad(message.encode(), AES.block_size)
    encrypted_message = cipher.encrypt(padded_message)
    return base64.b64encode(encrypted_message).decode()

def main():
    host = '127.0.0.1'
    port = 3333

    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((host, port))

    while True:
        print("\n1. Generate key using Diffie-Hellman")
        print("2. Send a message")
        print("3. Exit")
        choice = input("Enter your choice: ")

        if choice == '1':
            p = int(input("Enter prime number p: "))
            g = int(input("Enter primitive root g: "))
            a = random.randint(1, p-1)
            A = generate_key(p, g, a)
            
            client_socket.send(f"DH:{p},{g},{A}".encode())
            response = client_socket.recv(1024).decode()
            B = int(response.split(':')[1])
            
            shared_secret = generate_key(p, B, a)
            print(f"Shared secret: {shared_secret}")

        elif choice == '2':
            message = input("Enter message to send (at least 1000 characters): ")
            if len(message) < 1000:
                print("Message must be at least 1000 characters long.")
                continue
            
            encrypted_message = encrypt_message(shared_secret, message)
            client_socket.send(f"MSG:{encrypted_message}".encode())
            print("Message sent successfully.")

        elif choice == '3':
            print("Exiting...")
            break

        else:
            print("Invalid choice. Please try again.")

    client_socket.close()

if __name__ == "__main__":
    main()