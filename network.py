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
            return self.client.recv(2048).decode() # It receives a string which is 0 or 1
        except Exception as e:
            print(e)
    
    def send(self, data):
        try:
            self.client.send(str.encode(data)) # It sends a string to the server
            return pickle.loads(self.client.recv(2048*2)) # It receives a object from the server
        except socket.error as e:
            print(e)