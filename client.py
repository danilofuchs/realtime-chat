import argparse


class Client:
    def __init__(self, server_ip, server_port, name):
        self.server_ip = server_ip
        self.server_port = server_port
        self.name = name

    def start(self):
        self.connect_with_server()

        self.list_commands()
        while self.parse_input():
            pass

    def connect_with_server(self):
        print(
            f'Connecting client with server at {self.server_ip}:{self.server_port}')
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
        return False

    def list_commands(self):
        print('Comandos aceitos: exit, list, send, gsend')
        return True

    def list_contacts(self):
        # Pedir lista de clientes para o servidor
        print('Listando clientes')
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
# ID
# Nome
# Lista de clientes
#   - ID
#   - IP
#   - Porta
#   - Nome
#   - Disponível
# IP do servidor
# Porta do servidor
# Socket com o servidor


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--server-ip', type=str)
    parser.add_argument('--server-port', type=str)
    parser.add_argument('--name', type=str)

    args = parser.parse_args()

    client = Client(args.server_ip, args.server_port, args.name)
    client.start()
