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
        #s.connect = ((HOST, PORT))
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.bind((host, port))
        self.server_listen()

    def server_listen(self):
        # while True:
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

        print('accepted connection from', addr)
        host, port = addr
        name = conn.recv(1024).decode('utf-8')

        self.connected_clients[name] = {'host': host, 'port': port}

        data = types.SimpleNamespace(addr=addr, in_bytes=b'', out_bytes=b'')
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
        recv_data = sock.recv(1024)
        if recv_data:
            # Deal with message
            if (recv_data.decode('utf-8') == 'list'):
                data.out_bytes = json.dumps(
                    self.connected_clients).encode('utf-8')
        else:
            print('closing connection to', data.addr)
            sel.unregister(sock)
            sock.close()

    def write_message(self, key):
        sock = key.fileobj
        data = key.data
        if data.out_bytes:
            print('echoing', repr(data.out_bytes), 'to', data.addr)
            sent = sock.send(data.out_bytes)  # Should be ready to write
            data.out_bytes = data.out_bytes[sent:]

    def exit(self):
        self.sock.close()
        return False

# Lista de clientes
#   - ID
#   - IP
#   - Porta
#   - Nome
#   - Disponível
# IP do servidor
# Porta do servidor


if __name__ == "__main__":
    server = Server()
    server.start(HOST, PORT)
