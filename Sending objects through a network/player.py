import pygame

class Player:
    def __init__(self, x, y, width, height, color):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.color = color
        self.rect = (x, y, width, height)
        self.vel = 3
    
    def draw(self, win):
        pygame.draw.rect(win, self.color, self.rect)
    
    def move(self):
        keys = pygame.key.get_pressed() 
        # It returns a dictionary that associates 'pygame.K_LEFT' and other keys to boolean values (True:1 and False:0)
        # according to whether that key was pressed or not

        # USing just the if statement instead of elif as well makes it possible to move the character in a diagonal 
        # direction by pressing two keys at the same time
        if keys[pygame.K_LEFT]:
            self.x -= self.vel

        if keys[pygame.K_RIGHT]:
            self.x += self.vel

        if keys[pygame.K_UP]:
            self.y -= self.vel

        if keys[pygame.K_DOWN]:
            self.y += self.vel
        
        self.update()

    def update(self):
        self.rect = (self.x, self.y, self.width, self.height)