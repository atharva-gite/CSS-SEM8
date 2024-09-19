import socket
import random
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
import base64

def generate_key(p, g, b):
    return pow(g, b, p)

def decrypt_message(key, encrypted_message):
    key = key.to_bytes(32, byteorder='big')
    cipher = AES.new(key, AES.MODE_ECB)
    decoded_message = base64.b64decode(encrypted_message)
    decrypted_message = unpad(cipher.decrypt(decoded_message), AES.block_size)
    return decrypted_message.decode()

def main():
    host = '127.0.0.1'
    port = 3333

    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((host, port))
    server_socket.listen(1)

    print(f"Receiver listening on {host}:{port}")

    conn, addr = server_socket.accept()
    print(f"Connected by {addr}")

    shared_secret = None

    while True:
        data = conn.recv(1024).decode()
        if not data:
            break

        if data.startswith("DH:"):
            _, params = data.split(":")
            p, g, A = map(int, params.split(","))
            b = random.randint(1, p-1)
            B = generate_key(p, g, b)
            conn.send(f"DH:{B}".encode())
            
            shared_secret = generate_key(p, A, b)
            print(f"Shared secret: {shared_secret}")

        elif data.startswith("MSG:"):
            _, encrypted_message = data.split(":")
            decrypted_message = decrypt_message(shared_secret, encrypted_message)
            print(f"Received message: {decrypted_message}")

    conn.close()

if __name__ == "__main__":
    main()