import pygame
from network import Network
from player import Player

width = 500
height = 500
win = pygame.display.set_mode((width, height))
pygame.display.set_caption('Client')

def redraw_window(win, player1, player2):
    win.fill((255,255,255))
    player1.draw(win)
    player2.draw(win)
    pygame.display.update()

def main():
    run = True
    n = Network()
    clock = pygame.time.Clock()
    player1 = n.get_player()

    while run: # Runs every frame
        clock.tick(60)
        player2 = n.send(player1) # Sends the player1 back to the server and return the player2 object

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()
        player1.move() # This makes the current player move, not the other player because the other player will be updated by itself
        redraw_window(win, player1, player2)

main()