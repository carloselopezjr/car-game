import pygame
from pygame.locals import *
import sys
import random
import time

pygame.init() # initialize pygame engine
pygame.mixer.music.load("background.wav")
pygame.mixer.music.play(-1)  # -1 means loop forever


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

# Game Vars
SPEED = 5
SCORE = 0

# Font
font = pygame.font.SysFont("Verdana", 60)
font_small = pygame.font.SysFont("Verdana", 20)
game_over = font.render("Game Over", True, BLACK)

background = pygame.image.load("AnimatedStreet.png")

# Player car
# Self -> Refer to the current instance of the class ('this' in java)
class Player(pygame.sprite.Sprite): # Player inherits from pygame.sprite.Sprite
    # Constructor called automatically to set player initial state when player object is made (P1 = Player())
    def __init__(self): 
        super().__init__() # Initialize Sprite parent class
        self.image = pygame.image.load("Player.png") 
        self.rect = self.image.get_rect() # Defines border for collision
        self.rect.center = (160, 520) # Defines starting position for player
    
    # Player movement
    def move(self):
        pressed_keys = pygame.key.get_pressed()

        # -5 = up 5 = down

        if self.rect.top > 0:
            if pressed_keys[K_UP] or pressed_keys[K_w]:
                self.rect.move_ip(0,-5)
        if self.rect.bottom < SCREEN_HEIGHT:
            if pressed_keys[K_DOWN] or pressed_keys[K_s]:
                self.rect.move_ip(0,5)

        

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
        self.image = pygame.image.load("Enemy.png")
        self.rect = self.image.get_rect()
        self.rect.center = (random.randint(40,SCREEN_WIDTH-40),0) # Randomized spawnpoint
    
    def move(self):
        self.rect.move_ip(0,SPEED)
        global SCORE
        if (self.rect.bottom > SCREEN_HEIGHT):
            SCORE += 1
            self.rect.top = 0
            self.rect.center = (random.randint(30, 370), 0)
    
    def draw(self, surface):
        surface.blit(self.image, self.rect)


# Instantiate entity object
P1 = Player()
E1 = Enemy()
E2 = Enemy()

# Creating Sprites Groups
# Better management of entities
enemies = pygame.sprite.Group()
enemies.add(E1)


all_sprites = pygame.sprite.Group()
all_sprites.add(E1)

all_sprites.add(P1)

# Adding a new user event
INC_SPEED = pygame.USEREVENT + 1
pygame.time.set_timer(INC_SPEED,1000)


# Gameplay loop

while True:

    # Cycle through ocurring events
    for event in pygame.event.get():
        # Very cool
        if event.type == INC_SPEED:
            SPEED += 2
            print(SPEED)
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
    
    DISPLAY.blit(background, (0,0))
    scores = font_small.render(str(SCORE), True, BLACK)
    DISPLAY.blit(scores, (10,10))


  

    for entity in all_sprites:
        DISPLAY.blit(entity.image, entity.rect)
        entity.move()
    
    # If collision occurs between cars
    if pygame.sprite.spritecollideany(P1, enemies):
        pygame.mixer.Sound('crash.wav').play()
        time.sleep(0.5)

        print("collision")
        # DISPLAY.fill(RED)
        pygame.display.update()
        for entity in all_sprites:
            entity.kill()
        time.sleep(2)
        pygame.quit()
        sys.exit()

    
    pygame.display.update() 
    FPS.tick(60) # Limit framerate to 60