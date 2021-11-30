# Read for context: https://realpython.com/python-sockets/
import socket
import selectors
import types
sel = selectors.DefaultSelector()

HOST = socket.gethostbyname(socket.gethostname())
PORT = 5000
MAX_CLIENTS = 5


class Server:
    connected_clients = list()

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
                    self.accept_wrapper(key.fileobj)
                else:
                    self.service_connection(key, mask)

    def accept_wrapper(self, sock):
        conn, addr = sock.accept()  # Should be ready to read
        print('accepted connection from', addr)
        conn.setblocking(False)
        data = types.SimpleNamespace(addr=addr, inb=b'', outb=b'')
        events = selectors.EVENT_READ | selectors.EVENT_WRITE
        sel.register(conn, events, data=data)

    def service_connection(self, key, mask):
        sock = key.fileobj
        data = key.data
        if mask & selectors.EVENT_READ:
            recv_data = sock.recv(1024)  # Should be ready to read
            if recv_data:
                data.outb += recv_data
            else:
                print('closing connection to', data.addr)
                sel.unregister(sock)
                sock.close()
        if mask & selectors.EVENT_WRITE:
            if data.outb:
                print('echoing', repr(data.outb), 'to', data.addr)
                sent = sock.send(data.outb)  # Should be ready to write
                data.outb = data.outb[sent:]

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
