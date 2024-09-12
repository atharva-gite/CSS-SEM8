import socket
import pickle
from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP, AES
from Crypto.Random import get_random_bytes


def register_identity(identity, public_key):
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect(('localhost', 4444))
    request = {'type': 'register',
               'identity': identity, 'public_key': public_key}
    client.send(pickle.dumps(request))
    response = client.recv(1024)
    print(response.decode())
    client.close()


def get_public_key(identity):
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect(('localhost', 4444))
    request = {'type': 'get_key', 'identity': identity}
    client.send(pickle.dumps(request))
    public_key = pickle.loads(client.recv(1024))
    client.close()
    return public_key


def send_message(receiver_identity, message):
    # Step 1: Generate a symmetric key (AES key)
    symmetric_key = get_random_bytes(16)

    # Step 2: Get receiver's public key
    receiver_public_key = get_public_key(receiver_identity)
    rsa_cipher = PKCS1_OAEP.new(RSA.import_key(receiver_public_key))

    # Step 3: Encrypt the symmetric key using the receiver's public key
    encrypted_key = rsa_cipher.encrypt(symmetric_key)

    # Step 4: Encrypt the message using the symmetric key
    aes_cipher = AES.new(symmetric_key, AES.MODE_EAX)
    ciphertext, tag = aes_cipher.encrypt_and_digest(message.encode())

    # Step 5: Send encrypted key and message to receiver
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect(('localhost', 3333))
    client.send(pickle.dumps({'encrypted_key': encrypted_key,
                'ciphertext': ciphertext, 'nonce': aes_cipher.nonce}))
    client.close()


if __name__ == '__main__':
    identity = 'alice'
    key = RSA.generate(2048)
    public_key = key.publickey().export_key()

    # Step 1: Register identity
    register_identity(identity, public_key)

    # Step 2: Send encrypted message to receiver
    message = "This is a large secret message over 1000 characters..." * \
        10  # Sample large message
    send_message('bob', message)
