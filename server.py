import socket
import pickle

localIP     = "127.0.0.1"
localPort   = 20001
bufferSize  = 1024

# Create a datagram socket
UDPServerSocket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)

# Bind to address and ip
UDPServerSocket.bind((localIP, localPort))
print("UDP server up and listening")

# Listen for incoming datagrams
count = 0
clients = set() # We want to keep track of which clients we're paired with.
messages = {}   # And what their most recent message is so we can echo it.
while(True):
    bytesAddressPair = UDPServerSocket.recvfrom(bufferSize)
    count += 1
    message = bytesAddressPair[0]
    address = bytesAddressPair[1]
    clientMsg = "Message from Client, IP Address:{}".format(address)
    print(clientMsg)
    print(count)

    clients.add(address)
    str_address = f"{address}"
    messages[str_address] = message
    # Sending an update to all clients
    bytes_to_send = pickle.dumps([*messages.values()])
    for client in clients:
        UDPServerSocket.sendto(bytes_to_send, client)