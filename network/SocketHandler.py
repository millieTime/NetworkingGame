import threading
import socket
BUFFER_SIZE = 1024

class SocketHandler(threading.Thread):
    most_recent_data = None     # Data structure holding the most up-to-date info.
    has_new_data = False        # Whether there's data to send.
    data_lock = None            # Makes sure there's no half-reading or half-writing going on.
    UDPClientSocket = None      # How we connect to the server.
    address_port = None         # Where to send and receive the information.
    is_done = False

    def __init__(self, address_port):
        # Get all the data set up.
        threading.Thread.__init__(self)
        self.UDPClientSocket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)
        self.data_lock = threading.Lock()
        self.address_port = address_port

    def run(self):
        # Begin monitoring the port.
        while not self.is_done:
            self.run_once()
            
    
    def run_once(self):
        msg, _ = self.UDPClientSocket.recvfrom(BUFFER_SIZE)
        with self.data_lock:
            self.most_recent_data = msg
            if self.most_recent_data == b'END OF LINE':
                self.is_done = True
            self.has_new_data = True

    
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