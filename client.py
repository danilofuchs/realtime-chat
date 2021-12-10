import argparse
import json
import socket
import types
import selectors

MAX_CLIENTS = 5

sel = selectors.DefaultSelector()


class Client:
    clients = dict()

    def __init__(self, server_ip, server_port, name):
        self.server_ip = server_ip
        self.server_port = server_port
        self.name = name
        self.server = None

    def start(self):
        self.connect_to_server()

        self.list_commands()
        while self.parse_input():
            pass

    def connect_to_server(self):
        addr = (self.server_ip, self.server_port)
        print(
            f'Connecting client to server at {self.server_ip}:{self.server_port}')
        self.server_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_sock.connect(addr)
        self.server_sock.sendall(self.name.encode('utf-8'))

    def connect_to_client(self, m_host, m_port):
        addr = (m_host, m_port)
        print(
            f'Connecting client to client at {m_host}:{m_port}')
        self.client_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client_sock.connect(addr)

    def client_listen(self):
        # while True:
        print('Waiting connection...')
        self.client_sock.listen(MAX_CLIENTS)
        self.client_sock.setblocking(False)
        sel.register(self.client_sock, selectors.EVENT_READ, data=None)

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

    def parse_input(self):
        command = input('Esperando comandos: ')
        if command == 'exit':
            return self.exit()
        elif command == 'list':
            return self.list_contacts()
        elif command == 'send':
            return self.send()
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

    def send(self):
        target = input('Para quem: ')

        if not target:
            print('Nome inválido')
            return True

        clients = self.list_clients()
        address = self.get_client_address_by_name(clients, target)
        if address is None:
            print('Usuario não conectado')
            return True

        host, port = address
        print('Conectando ao usuario')
        self.connect_to_client(host, port)
        message = input('Digite uma mensagem: ')
        print('Enviando mensagem: "{}"...'.format(message))

        # Pedir lista de clientes para o servidor
        # Enviar uma mensagem por socket para o cliente
        return True

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
    parser.add_argument('--server-ip', type=str)
    parser.add_argument('--server-port', type=int)
    parser.add_argument('--name', type=name_arg)

    args = parser.parse_args()

    client = Client(args.server_ip, args.server_port, args.name)
    client.start()
