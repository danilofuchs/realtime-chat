import argparse
import json
import socket
import types
import selectors
import sys
import threading
import queue

sel = selectors.DefaultSelector()

HOST = socket.gethostbyname(socket.gethostname())
MAX_CLIENTS = 5


def add_input(input_queue):
    while True:
        input_queue.put(sys.stdin.read(1))


class Client:
    clients = dict()
    input_queue = queue.Queue()

    def __init__(self, host, port, server_ip, server_port, name):
        self.server_ip = server_ip
        self.server_port = server_port
        self.name = name
        self.server = None

        self.host = host
        self.port = port

        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.bind((host, port))

    def start(self):
        self.connect_to_server()

        self.list_commands()

        self.client_listen()

        self.init_input_thread()

        while True:
            if not self.input_queue.empty():
                command = ''
                while not self.input_queue.empty():
                    char = self.input_queue.get()
                    if char == '\n':
                        break
                    command += char
                self.parse_input(command)
            events = sel.select(timeout=-1)
            for key, mask in events:
                if key.data is None:
                    self.accept_connection(key)
                else:
                    self.service_connection(key, mask)

    def init_input_thread(self):
        input_thread = threading.Thread(
            target=add_input, args=(self.input_queue,))
        input_thread.daemon = True
        input_thread.start()

    def connect_to_server(self):
        addr = (self.server_ip, self.server_port)
        print(
            f'Connecting client to server at {self.server_ip}:{self.server_port}')
        self.server_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_sock.connect(addr)
        body = {'name': self.name, 'host': self.host, 'port': self.port}
        self.server_sock.sendall(json.dumps(body).encode('utf-8'))

    def client_listen(self):
        print('Waiting connection...')
        self.sock.listen(MAX_CLIENTS)
        self.sock.setblocking(False)
        sel.register(self.sock, selectors.EVENT_READ, data=None)

    def accept_connection(self, key):
        sock = key.fileobj
        conn, addr = sock.accept()
        conn.setblocking(False)

        print('accepted connection from', addr)

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
            recv_data = recv_data.decode('utf-8')
            print('msg recebida: ', recv_data)
        else:
            print('closing connection to', data.addr)
            sel.unregister(sock)
            sock.close()

    def write_message(self, key):
        sock = key.fileobj
        data = key.data
        if data.out_bytes:
            sent = sock.send(data.out_bytes)  # Should be ready to write
            data.out_bytes = data.out_bytes[sent:]

    def parse_input(self, command):
        if command == 'exit':
            return self.exit()
        elif command == 'list':
            return self.list_contacts()
        elif command.startswith('send'):
            # send <name> <message>
            command_args = command.split(' ')
            if len(command_args) < 3:
                print('Comando inválido. Use: send <name> <message>')
                return True
            name = command_args[1]
            message = ' '.join(command_args[2:])

            return self.send(name, message)
        elif command == 'gsend':
            return self.group_send()
        return self.list_commands()

    def exit(self):
        self.server_sock.close()
        return False

    def list_commands(self):
        print('Comandos aceitos: exit, list, send, gsend')
        return True

    def list_contacts(self):
        clients = self.list_clients()
        # Pedir lista de clientes para o servidor
        print(f'Contatos: {clients}')
        return True

    def send(self, name, message):
        if not name:
            print('Nome inválido')
            return True

        clients = self.list_clients()
        address = self.get_client_address_by_name(clients, name)
        if address is None:
            print('Usuario não conectado')
            return True

        host, port = address
        print('Conectando ao usuario')
        self.connect_to_client(host, port)
        print('Enviando mensagem: "{}"...'.format(message))

        # Pedir lista de clientes para o servidor
        # Enviar uma mensagem por socket para o cliente
        return True

    def connect_to_client(self, m_host, m_port):
        addr = (m_host, m_port)
        print(
            f'Connecting client to client at {m_host}:{m_port}')
        remote_client_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        remote_client_sock.connect(addr)

    def group_send(self):
        targets_str = input('Nomes dos destinatários: ')
        targets = targets_str.split(' ')
        message = input('Digite uma mensagem: ')
        print('Enviando mensagem de grupo para {}: "{}"'.format(targets, message))
        # Enviar uma mensagem por socket para o servidor
        return True

    def list_clients(self):
        self.server_sock.send(b'list')
        as_bytes = self.server_sock.recv(1024)
        as_string = as_bytes.decode('utf-8')
        as_json = json.loads(as_string)
        return as_json

    def get_client_address_by_name(self, clients, name):
        if name in clients:
            client = clients[name]
            print('usuario encontrado {}'.format(client))
            return (client['host'], client['port'])
        else:
            return None

    def send_message_to_group(self, names):
        # Usar socket com servidor para enviar mensagem para os clients
        pass


def name_arg(value):
    if not value:
        raise argparse.ArgumentTypeError('Nome não pode ser vazio')
    if (len(value) > 30):
        raise argparse.ArgumentTypeError(
            'Nome muito grande (max 30 caracteres)')
    return value


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--port', type=int)
    parser.add_argument('--server-ip', type=str)
    parser.add_argument('--server-port', type=int)
    parser.add_argument('--name', type=name_arg)

    args = parser.parse_args()

    client = Client(HOST, args.port, args.server_ip,
                    args.server_port, args.name)
    client.start()
