import pygame
from pygame.locals import *
import sys
import random

pygame.init() # initialize pygame engine

# FPS
FPS = pygame.time.Clock()

# Colors
BLUE = (0,0,255)
RED = (255,0,0)
GREEN = (0,255,0)
BLACK = (0,0,0)
WHITE =(255,255,255)

# Screen
SCREEN_WIDTH = 400
SCREEN_HEIGHT = 600
DISPLAY = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
DISPLAY.fill(WHITE)
pygame.display.set_caption("vroom")

# Player car
# Self -> Refer to the current instance of the class ('this' in java)
class Player(pygame.sprite.Sprite): # Player inherits from pygame.sprite.Sprite
    # Constructor called automatically to set player initial state when player object is made (P1 = Player())
    def __init__(self): 
        super().__init__() # Initialize Sprite parent class
        self.image = pygame.image.load("player.png") 
        self.rect = self.image.get_rect() # Defines border for collision
        self.rect.center = (160, 520) # Defines starting position for player
    
    # Player movement
    def update(self):
        pressed_keys = pygame.key.get_pressed()

        

        if self.rect.left > 0: # Ensure player isnt off screen (left)
            if pressed_keys[K_LEFT] or pressed_keys[K_a]:
                self.rect.move_ip(-5,0)
        if self.rect.right < SCREEN_WIDTH: # Ensure player isnt off screen (right)
            if pressed_keys[K_RIGHT] or pressed_keys[K_d]:
                self.rect.move_ip(5,0)
    
    def draw(self, surface):
        surface.blit(self.image, self.rect) # Draw player img onto screen at location specified by self.rect

# Enemy Car
class Enemy(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load("enemy.png")
        self.rect = self.image.get_rect()
        self.rect.center = (random.randint(40,SCREEN_WIDTH-40),0) # Randomized spawnpoint
    
    def move(self):
        self.rect.move_ip(0,10)
        if (self.rect.bottom > SCREEN_HEIGHT):
            self.rect.top = 0
            self.rect.center = (random.randint(30, 370), 0)
    
    def draw(self, surface):
        surface.blit(self.image, self.rect)



P1 = Player()
E1 = Enemy()


# Gameplay loop

while True:
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
    P1.update()
    E1.move()

    DISPLAY.fill(WHITE)
    P1.draw(DISPLAY)
    E1.draw(DISPLAY)

    pygame.event.get() # delete later
    
    pygame.display.update() 
    FPS.tick(60) # Limit framerate to 60