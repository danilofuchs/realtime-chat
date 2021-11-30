import argparse
import socket

# Trabalhando com IPV4
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)


class Client:
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
        s.connect(addr)
        print(
            f'Connecting client to server at {self.server_ip}:{self.server_port}')
        clients_list = s.recv(1024)
        if clients_list:
            print(
                f'Connected clients : {clients_list}')
        # TODO: Connect with server with a Socket

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
        s.close()
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
        message = input('Digite uma mensagem: ')
        print('Enviando mensagem para {}: "{}"...'.format(target, message))
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
        # Usar socket com servidor para listar todos os clients
        return []

    def send_message_to_client(self, name):
        # Listar todos os clients
        clients = self.list_clients()
        # Encontrar client correto pelo name
        # Conectar por socket e enviar mensagem para o cliente
        pass

    def send_message_to_group(self, names):
        # Usar socket com servidor para enviar mensagem para os clients
        pass


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--server-ip', type=str)
    parser.add_argument('--server-port', type=int)
    parser.add_argument('--name', type=str)

    args = parser.parse_args()

    client = Client(args.server_ip, args.server_port, args.name)
    client.start()
