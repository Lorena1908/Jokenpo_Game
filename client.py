import pygame
from network import Network
pygame.font.init()

width = 700
height = 700
win = pygame.display.set_mode((width, height))
pygame.display.set_caption('Client')

class Button:
    def __init__(self, text, x, y, color):
        self.text = text
        self.x = x
        self.y = y 
        self.color = color
        self.width = 150
        self.height = 100
    
    def draw(self, win):
        pygame.draw.rect(win, self.color, (self.x, self.y, self.width, self.height))
        font = pygame.font.SysFont('comicsans', 40)
        text = font.render(self.text, 1, (255,255,255))
        win.blit(text, (self.x + round(self.width/2) - round(text.get_width()/2), self.y + round(self.height/2) - round(text.get_height()/2) ))

    def click(self, clicked_position):
        x1 = clicked_position[0]
        y1 = clicked_position[1]

        if self.x <= x1 <= self.x + self.width and self.y <= y1 <= self.y + self.height:
            return True
        else:
            return False

def redraw_window(win, game, player):
    win.fill((128,128,128))
    
    if not(game.connected()):
        font = pygame.font.SysFont('comicsans', 80)
        text = font.render('Waiting for Player...', 1, (255,0,0))
        win.blit(text, (width/2 - text.get_width()/2, height/2 - text.get_height()/2))
    else:
        font = pygame.font.SysFont('comicsans', 60)
        text = font.render('Your move', 1, (0,255,255))
        win.blit(text, (80,200))

        text = font.render('Opponents', 1, (0,255,255))
        win.blit(text, (380,200))

        move1 = game.get_player_move(0)
        move2 = game.get_player_move(1)

        if game.both_players_moved():
            text1 = font.render(move1, 1, (0,0,0))
            text2 = font.render(move2, 1, (0,0,0))
        else:
            if game.player1_moved and player == 0:
                text1 = font.render(move1, 1, (0,0,0))
            elif game.player1_moved:
                text1 = font.render('Locked in', 1, (0,0,0))
            else:
                text1 = font.render('Waiting...', 1, (0,0,0))
            
            if game.player2_moved and player == 1:
                text2 = font.render(move2, 1, (0,0,0))
            elif game.player2_moved:
                text2 = font.render('Locked in', 1, (0,0,0))
            else:
                text2 = font.render('Waiting...', 1, (0,0,0))
        
        if player == 1:
            win.blit(text2, (100,350))
            win.blit(text1, (400,350))
        else:
            win.blit(text1, (100,350))
            win.blit(text2, (400,350))

        for button in buttons:
            button.draw(win)
    pygame.display.update()

buttons = [Button('Rock', 50, 500, (0,0,0)), Button('Scissors', 250, 500, (255,0,0)), Button('Paper', 450, 500, (0,255,0))]
def main():
    run = True
    clock = pygame.time.Clock()
    n = Network() # Use the Network() class to connect to the server
    player = int(n.get_player())
    print('You are player', player)

    while run:
        clock.tick(60)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                position = pygame.mouse.get_pos()
                for button in buttons:
                    if button.click(position) and game.connected():
                        if player == 0:
                            if not game.player1_moved:
                                n.send(button.text)
                        else:
                            if not game.player2_moved:
                                n.send(button.text)

        try:
            game = n.send('get') # Gets the game object
            # If this doesn't work it'll be because one of the clients have already exited and the game was deleted
        except:
            run = False
            print('Coudn\'t get the game')
            break

        if game.both_players_moved():
            redraw_window(win, game, player)
            pygame.time.delay(1000)
            try:
                game = n.send('reset')
            except:
                run = False
                print('Coudn\'t get the game')
                break
            
            font = pygame.font.SysFont('comicsans', 90)
            if (game.winner() == 1 and player == 1) or (game.winner() == 0 and player == 0):
                text = font.render('You Won!', 1, (255,0,0))
            elif game.winner() == -1:
                text = font.render('Tie Game!', 1, (255,0,0))
            else:
                text = font.render('You Lost!', 1, (255,0,0))
            
            win.blit(text, (width/2 - text.get_width()/2, height/2 - text.get_height()/2))
            pygame.display.update()
            pygame.time.delay(2000)
        redraw_window(win, game, player)

def menu_screen():
    run = True
    clock = pygame.time.Clock()
    
    while run:
        clock.tick(60)
        win.fill((128,128,128))
        font = pygame.font.SysFont('comicsans', 60)
        text = font.render('Click to Play!', 1, (255,0,0))
        win.blit(text, (width/2 - text.get_width()/2, height/2 - text.get_height()/2))
        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                run = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                run = False
    
    main()
            
while True:
    menu_screen()