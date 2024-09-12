import socket
import pickle
from Crypto.PublicKey import RSA


class ThirdPartyEntity:
    def __init__(self):
        self.keys = {}

    def register_key(self, identity, public_key):
        self.keys[identity] = public_key

    def get_key(self, identity):
        return self.keys.get(identity, None)


def run_third_party():
    entity = ThirdPartyEntity()
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind(('localhost', 7777))
    server.listen(5)
    print("Third party service started on port 7777")

    while True:
        client_socket, addr = server.accept()
        data = client_socket.recv(1024)
        request = pickle.loads(data)

        if request['type'] == 'register':
            entity.register_key(request['identity'], request['public_key'])
            client_socket.send(b"Key registered successfully")
        elif request['type'] == 'get_key':
            public_key = entity.get_key(request['identity'])
            client_socket.send(pickle.dumps(public_key))
        client_socket.close()


if __name__ == '__main__':
    run_third_party()
