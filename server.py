import socket
from _thread import *
import pickle
from game import Game

server = '192.168.100.5' # The server.py script has to be runing on this machine
port = 5555

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

try:
    s.bind((server, port))
except socket.error as e:
    print(e)

s.listen() # This listen for two clint connections
print('Waiting for a connection, Server Started')

games = {}
id_count = 0

def threaded_client(connection, player, game_id): 
    # Each client has one version of this function running in the background at the same time
    global id_count
    connection.send(str.encode(str(player)))

    reply = ''
    while True: # It runs once for every frame
        try:
            data = connection.recv(4096).decode() # it Receives string from the client
            # If this connection return an empty byte it means the client closed the connection and the loop is terminated

            if game_id in games: 
                # This checks if the game still exists, because if the client disconnects from the game we'll delete it
                game = games[game_id]

                if not data:
                    break
                else:
                    if data == 'reset':
                        game.reset_moves()
                    elif data != 'get':
                        game.play(player, data)
                    
                    connection.sendall(pickle.dumps(game)) 
                    # The client receives this through the 'send()' method from the 'Network()' class
            else:
                break
        except:
            break
    print('Lost connection')
    try:
        del games[game_id]
        print('Closing game:', game_id)
    except:
        pass
    id_count -= 1 # One client was closed
    connection.close()

while True: # This runs once for every connection made
    connection, address = s.accept() # connection -> new socket object; address -> address of the sockect from the other device
    print('Connected to: ', address)

    id_count += 1 # This represents the number of clients
    player = 0
    game_id = (id_count - 1) // 2 # This will make a single game id for every two people that connect to the server
    if id_count % 2 == 1: 
        # if the result is 0, it means that there are even clients playing the game, but if it is 1,
        # it means that there are odd clients playing the game
        games[game_id] = Game(game_id) # It creates a new game when there are odd clients
        print('Creating a new game...')
    else:
        games[game_id].ready = True
        player = 1

    # start_new_thread(function, arguments)
    start_new_thread(threaded_client, (connection, player, game_id))
