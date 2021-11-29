
class Server:
    def start(self):
        #Trabalhando com IPV4
        print('Starting Server')
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect = ((HOST, PORT))

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
