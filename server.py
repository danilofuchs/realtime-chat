import socket
HOST = socket.gethostbyname(socket.gethostname())
PORT = 5000
MAX_CLIENTS = 5

# Trabalhando com IPV4
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

connected_clients = list()


class Server:
    def start(self):
        print(f'Starting Server at {HOST}:{PORT}')
        #s.connect = ((HOST, PORT))
        s.bind((HOST, PORT))
        self.server_listen()

    def server_listen(self):
        # while True:
        print('Waiting connection...')
        s.listen(MAX_CLIENTS)
        conn, addr = s.accept()
        with conn:
            print('Connected by', addr)
            connected_clients.append(addr)
            # conn.sendall(connected_clients)
            print(connected_clients)

    def exit(self):
        s.close()
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
    server.start()
