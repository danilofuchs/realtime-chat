import argparse


class Client:
    def start(self):
        print('Starting Client')
        parser = argparse.ArgumentParser()
        parser.add_argument('--ip', type=str)
        parser.add_argument('--port', type=str)
        parser.add_argument('--name', type=str)

        args = parser.parse_args()
        self.serverIp = args.ip
        self.serverPort = args.port
        self.name = args.name

        # Conectar com o servidor

        while self.parse_input():
            pass
            

    def parse_input(self):
        command = input('Esperando comandos: ')
        if command == 'exit':
            return False
        elif command == 'list':
            # Pedir lista de clientes para o servidor
            print('Listando clientes')
        elif command == 'send':
            target = input('Para quem: ')
            print('Enviando mensagem para {}...'.format(target))
            message = input('Digite uma mensagem: ')
            # Pedir lista de clientes para o servidor
            # Enviar uma mensagem por socket para o cliente
            print(message)
        elif command == 'gsend':
            list = input('Nomes dos destinatários: ')
            targets = list.split(' ')
            print('Enviando mensagem de grupo para {}'.format(targets))
            message = input('Digite uma mensagem: ')
            # Enviar uma mensagem por socket para o servidor
            print(message)
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
    client = Client()
    client.start()
