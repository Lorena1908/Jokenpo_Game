class Game:
    def __init__(self, id):
        self.player1_moved = False
        self.player2_moved = False
        self.ready = False # When True there are two people connected to the same game
        self.id = id # This determines which client plays with which
        self.moves = [None, None] # Rock, paper or scissors
        self.wins = [0,0]
        self.ties = 0

    def get_player_move(self, p):
        # p is 0 or 1 and this function will return the move made by the other player
        return self.moves[p]
    
    def play(self, player, move):
        # Update moves and check which player has already played
        self.moves[player] = move
        if player == 0:
            self.player1_moved = True
        else:
            self.player2_moved = True
    
    def connected(self): # Check if the two player are conected to the game
        return self.ready

    def both_players_moved(self):
        return self.player1_moved and self.player2_moved
    
    def winner(self):
        player1 = self.moves[0].upper()[0] # Get the firt letter of the player move
        player2 = self.moves[1].upper()[0]

        winner = -1
        # Player one wins -> winner = 0
        # Player two wins -> winner = 1
        # Tie = -1

        if player1 == 'R' and player2 == 'S':
            winner = 0
        elif player1 == 'S' and player2 == 'R':
            winner = 1
        elif player1 == 'P' and player2 == 'R':
            winner = 0
        elif player1 == 'R' and player2 == 'P':
            winner = 1
        elif player1 == 'S' and player2 == 'P':
            winner = 0
        elif player1 == 'P' and player2 == 'S':
            winner = 1
        
        return winner
    
    def reset_moves(self):
        self.player1_moved = False
        self.player2_moved = False