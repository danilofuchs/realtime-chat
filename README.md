# Realtime chat

Very simple multiple-client chat application in Python.

## Installing

```
pip install -r requirements.txt
```

## Running

- Start a server:

```bash
python server.py
```

- Start a client:

```bash
python client.py --server-ip 127.0.0.1 --server-port 5000 --name bob
```

- Start a 2nd client:

```bash
python client.py --server-ip 127.0.0.1 --server-port 5000 --name ted
```

## Objetivos

- Cliente: Enviar mensagens para um outro cliente diretamente ou para vários através do servidor
- Servidor: Gerenciar lista de clientes conectados e enviar mensagens para todos os clientes

## Requisitos funcionais

### Cliente

- Input do IP e porta do servidor
- Input da Porta do cliente
- Cliente deve ter um nome
- Conectar ao servidor com socket
- Requisitar endereços de clientes do servidor e saber se estão disponíveis
- Enviar uma mensagem para um outro cliente específico sem intermédio do servidor, por sockets
- Mostrar as mensagens recebida, data e nome dos remetentes
- Cria um socket somente no momento em que precisar enviar mensagem para outro cliente
- Desconecta o socket logo após enviar a mensagem

### Servidor

- Atender a requisição de um cliente para se conectar ao chat
- Atender chamada de mensagem de grupo, enviando a mensagem para todos os clientes escolhidos
- Enviar a lista atualizada ao usuário assim que ele requisitar por meio do comando list
- Mostrar ao usuário qual o IP e porta do servidor para que os clientes se conectem
- Não pode ter mais de um cliente com o mesmo nome

## Requisitos não funcionais

- Usando Python 3
- Não vai ter interface gráfica (interação pelo terminal)
- Deve ter suporte para IPv4
