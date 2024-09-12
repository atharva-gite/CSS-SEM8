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
    print("Receiver service started on port 3333")

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
    server.close()


if __name__ == '__main__':
    identity = 'vedant'
    key = RSA.generate(2048)
    public_key = key.publickey().export_key()

    # Step 1: Register identity
    register_identity(identity, public_key)

    # Step 2: Wait and receive messages
    receive_message(RSA.import_key(key.export_key()))
