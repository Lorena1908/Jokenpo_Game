import socket
from _thread import *
import sys
from player import Player
import pickle

server = '192.168.100.5' # The server.py script has to be runing on this machine
port = 5555

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

try:
    s.bind((server, port))
except socket.error as e:
    print(e)

s.listen(2) # This will listen for connections between computers (people who want to play the game)
print('Waiting for a connection, Server Started')

players = [Player(0,0,50,50,(255,0,0)), Player(100,100,50,50,(0,0,255))]

def threaded_client(connection, player):
    connection.send(pickle.dumps(players[player])) # The player object is sent to the client
    reply = ''

    while True:
        try:
            data = pickle.loads(connection.recv(2048)) # This is the player object that is received from the client to the server
            players[player] = data # It updates the player object in the 'players' list

            if not data: # If data is empty
                print('Disconnected')
                break
            else:
                # It send the object of the other player, not the current one
                if player == 1:
                    reply = players[0] # This is sent from the server to the client
                else:
                    reply = players[1] # This is sent from the server to the client
                
                print('Received: ', data)
                print('Sending: ', reply)
            connection.sendall(pickle.dumps(reply)) # Send the data to the client
        except:
            break
    print('Lost connection')
    connection.close()

current_player = 0
while True:
    connection, address = s.accept() # connection -> new socket object; address -> address of the sockect from the other device
    print('Connected to: ', address)

    # start_new_thread(function, arguments)
    start_new_thread(threaded_client, (connection, current_player))
    current_player += 1