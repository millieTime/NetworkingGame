import socket
import threading
import time
import pickle

BUFFER_SIZE = 1024

class SubObject:

    def __init__(self, number1, number2):
        self.num1 = number1
        self.num2 = number2

    def get_sum(self):
        return self.num1 + self.num2

    def get_num2(self):
        return self.num2


class TestObject:
    
    def __init__(self, number, name, sub_object):
        self.num = number
        self.name = name
        self.s_o = sub_object

    def get_so_sum(self):
        return self.s_o.get_sum()
    
    def get_name(self):
        return self.name

class SocketHandler(threading.Thread):
    most_recent_data = None     # Data structure holding the most up-to-date info.
    has_new_data = False        # Whether there's data to send.
    data_lock = None            # Makes sure there's no half-reading or half-writing going on.
    UDPClientSocket = None      # How we connect to the server.
    address_port = None         # Where to send and receive the information.
    is_done = False

    def __init__(self, address_port, data_lock):
        # Get all the data set up.
        threading.Thread.__init__(self)
        self.UDPClientSocket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)
        self.data_lock = data_lock
        self.address_port = address_port

    def run(self):
        # Begin monitoring the port.
        while not self.is_done:
            msg, _ = self.UDPClientSocket.recvfrom(BUFFER_SIZE)
            with self.data_lock:
                self.most_recent_data = msg
                if self.most_recent_data == b'END OF LINE':
                    self.is_done = True
                self.has_new_data = True
            print(type(msg))
    
    def get_data(self):
        # Returns the most up-to-date information.
        with self.data_lock:
            self.has_new_data = False
            return self.most_recent_data

    def send_to_server(self, to_send):
        # Sends some info to the server.
        self.UDPClientSocket.sendto(to_send, self.address_port)
    
    def set_done(self, val):
        # Tell the client it's done.
        self.is_done = val
    
    def get_done(self):
        # Find out if the client is done.
        return self.is_done

def main():
    msgFromClient       = "Hello UDP Server0"
    bytesToSend         = str.encode(msgFromClient)
    serverAddressPort   = ("127.0.0.1", 20001)

    # Create a UDP socket at client side
    lock = threading.Lock()
    s_hand = SocketHandler(serverAddressPort, lock)
    s_hand.send_to_server(str.encode("opening UDP connection. . ."))

    s_hand.start()
    count = 0
    while True:
        message = input("> ")
        sub_object = SubObject(count * 2, count / 2)
        test_obj = TestObject(count, message, sub_object)
        #bytesToSend = str.encode(message)
        pickled_obj = pickle.dumps(test_obj)
        s_hand.send_to_server(pickled_obj)
        time.sleep(5)
        response_strings = s_hand.get_data()
        
        count += 1

def main2():
    serverAddressPort   = ("127.0.0.1", 20001)

    # Create a UDP socket at client side
    lock = threading.Lock()
    s_hand = SocketHandler(serverAddressPort, lock)
    s_hand.send_to_server(pickle.dumps("opening UDP connection. . ."))
    s_hand.start()
    name = input("> ")

    sub_object = SubObject(5, 7)
    test_obj = TestObject(3, name, sub_object)
    pickled_obj = pickle.dumps(test_obj)
    s_hand.send_to_server(pickled_obj)
    #get new data
    while not s_hand.has_new_data:
        pass
    bytes_received = s_hand.get_data()
    #unpickle the data
    unpickled_list = pickle.loads(bytes_received)
    for index in range(len(unpickled_list)):
        unpickled_list[index] = pickle.loads(unpickled_list[index])
    for test_object in unpickled_list:
        if type(test_object) == str:
            print(test_object)
        else:
            print(test_object.get_name(), test_object.get_so_sum())

    name = input("> ")

    sub_object = SubObject(5, 7)
    test_obj = TestObject(3, name, sub_object)
    pickled_obj = pickle.dumps(test_obj)
    s_hand.send_to_server(pickled_obj)
    # get new data
    while not s_hand.has_new_data:
        pass
    bytes_received = s_hand.get_data()
    # unpickle the data
    unpickled_list = pickle.loads(bytes_received)
    for index in range(len(unpickled_list)):
        unpickled_list[index] = pickle.loads(unpickled_list[index])
    for test_object in unpickled_list:
        if type(test_object) == str:
            print(test_object)
        else:
            print(test_object.get_name(), test_object.get_so_sum())
    

if __name__ == "__main__":
    main2()