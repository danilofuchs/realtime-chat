# Read for context: https://realpython.com/python-sockets/
import socket
import selectors
import types
import json

sel = selectors.DefaultSelector()

HOST = socket.gethostbyname(socket.gethostname())
PORT = 5000
MAX_CLIENTS = 5


class Server:
    connected_clients = dict()

    def start(self, host, port):
        print(f'Starting Server at {host}:{port}')
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.bind((host, port))
        self.server_listen()

    def server_listen(self):
        print('Waiting connection...')
        self.sock.listen(MAX_CLIENTS)
        self.sock.setblocking(False)
        sel.register(self.sock, selectors.EVENT_READ, data=None)

        while True:
            events = sel.select(timeout=None)
            for key, mask in events:
                if key.data is None:
                    self.accept_connection(key)
                else:
                    self.service_connection(key, mask)

    def accept_connection(self, key):
        sock = key.fileobj
        conn, addr = sock.accept()
        conn.setblocking(False)

        body = json.loads(conn.recv(1024).decode('utf-8'))

        name = body['name']
        print(f'accepted connection from {addr} {name}')

        self.connected_clients[name] = {
            'host': body['host'],
            'port': body['port'],
        }

        data = types.SimpleNamespace(
            addr=addr,
            name=name,
            in_bytes=b'',
            out_bytes=b'',
        )
        events = selectors.EVENT_READ | selectors.EVENT_WRITE
        sel.register(conn, events, data=data)

    def service_connection(self, key, mask):
        if mask & selectors.EVENT_READ:
            self.read_message(key)
        if mask & selectors.EVENT_WRITE:
            self.write_message(key)

    def read_message(self, key):
        sock = key.fileobj
        data = key.data
        try:
            recv_data = sock.recv(1024)
            if recv_data:
                data.out_bytes = json.dumps(self.route(
                    recv_data.decode('utf-8'))).encode('utf-8')
            else:
                self.disconnect_client(sock, data)
        except ConnectionResetError:
            self.disconnect_client(sock, data)

    def disconnect_client(self, sock, data):
        print('closing connection to', data.addr)

        self.remove_client_from_list(data.name)

        sel.unregister(sock)
        sock.close()

    def remove_client_from_list(self, name):
        if name in self.connected_clients:
            del self.connected_clients[name]

    def write_message(self, key):
        sock = key.fileobj
        data = key.data
        if data.out_bytes:
            sent = sock.send(data.out_bytes)  # Should be ready to write
            data.out_bytes = data.out_bytes[sent:]

    def route(self, command):
        if command == 'list':
            return self.connected_clients
        if command.startswith('gsend:'):
            body = json.loads(command.replace('gsend:', ''))
            names = body['names']
            message = body['message']

            return self.send_to_group(names, message)
        return 'Unknown command'

    def send_to_group(self, names, message):
        for name in names:
            if name in self.connected_clients:
                self.send_message(name, message)

    def send_message(self, name, message):
        client = self.connected_clients[name]
        address = (client['host'], client['port'])
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as remote_sock:
            remote_sock.connect(address)
            body = {'name': name, 'message': message}
            self.send_using_socket(remote_sock, json.dumps(body))

    def send_using_socket(self, socket, message):
        socket.sendall(message.encode('utf-8'))


if __name__ == "__main__":
    server = Server()
    server.start(HOST, PORT)
