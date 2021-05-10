import socket
import pickle

class Network:
    def __init__(self):
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server = '192.168.100.5'
        self.port = 5555
        self.address = (self.server, self.port)
        self.player = self.connect()
    
    def get_player(self):
        return self.player
    
    def connect(self):
        try:
            self.client.connect(self.address) # It connects to the server
            return pickle.loads(self.client.recv(2048)) # Returns the player object
        except:
            pass
    
    def send(self, data):
        try:
            self.client.send(pickle.dumps(data)) # It sends to the server
            return pickle.loads(self.client.recv(2048))
        except socket.error as e:
            print(e)