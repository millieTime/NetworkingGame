import socket
import pickle
from game import constants

localIP     = socket.gethostbyname( '0.0.0.0' )
localPort   = 20001
bufferSize  = 1024

# Create a datagram socket
UDPServerSocket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)

# Bind to address and ip
UDPServerSocket.bind((localIP, localPort))
print("UDP server up and listening")

# Listen for incoming datagrams
name_incr = 0
clients = set() # We want to keep track of which clients we're paired with.
messages = {}   # And what their most recent message is so we can echo it.
while(True):
    bytesAddressPair = UDPServerSocket.recvfrom(bufferSize)
    message = bytesAddressPair[0]
    address = bytesAddressPair[1]
    
    if address not in clients:
        print("New client connected, returning. . .")
        # It's a new client requesting a name
        bytes_to_send = pickle.dumps(constants.PLAYER_NAMES[name_incr])
        name_incr += 1
        UDPServerSocket.sendto(bytes_to_send, address)
        clients.add(address)
    else:
        print("Return client connected, returning. . .")
        # It's an update of a player's location, store it and broadcast all.
        str_address = f"{address}"
        messages[str_address] = message
        # Sending an update to all clients
        bytes_to_send = pickle.dumps([*messages.values()])
        for client in clients:
            UDPServerSocket.sendto(bytes_to_send, client)