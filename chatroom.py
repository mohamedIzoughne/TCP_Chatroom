import threading
import socket

host = '127.0.0.1'
port = 55555

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

server.bind((host, port))

server.listen()

clients = []
nicknames = []

def broadcastMessage(message):
    for client in clients:
        client.send(message)

def handleClient(client):
    while True:
        try:
            message = client.recv(1024)
            broadcastMessage(message)
        except:
            index = clients.index(client)
            clients.remove(client)
            nickname = nicknames[index]
            print(f"{nickname} left the chat !".encode(ascii)) # why encoding in ascii?
            nicknames.remove(nickname)
            break
            # so we're constantly trying to get messages from the client. this will give you an error if a client doesn't exist anymore. it will not give you error if the client doesn't send the message

def receive():
    while True:
        client, address = server.accept() # we're running the accept method all the time and if it gets a connection it returns a client
        ## in this case we're always gonna have one address because we send from the same computer: which means the same ip
        print(f'Connected with {str(address)}')
        client.send("NICK".encode('ascii')) ## send a message to the client
        nickname = client.recv(1024).decode('ascii')
        nicknames.append(nickname)
        clients.append(client)

        broadcastMessage(f"{nickname} has joined the chat room".encode("ascii"))
        client.send("Connected to the server".encode("ascii"))

        # we should run one thread for each client in order to handle both of them at the same time
        thread = threading.Thread(target=handleClient, args=(client,))
        thread.start()

receive()
print("Server is listenning...")

# how to change the color of each one?