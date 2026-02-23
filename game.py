import pygame
from pygame.locals import *
import random

pygame.init()

clock = pygame.time.Clock()
fps = 60

screen_width = 864
screen_height = 936

# Creating the game window
screen = pygame.display.set_mode((screen_width, screen_height))
# this is the title of the game
pygame.display.set_caption("Opium Flappy")


# Game variables
ground_scroll = 0
scroll_speed = 4
flying = False # Creating a variable to check if the bird is flying
game_over = False # Creating a variable to check if the game is over
pipe_gap = 200 
pipe_frequency = 1500 # milliseconds between pipe spawns
last_pipe = pygame.time.get_ticks() - pipe_frequency

# Load the background image
background = pygame.image.load("img/bg.png")
ground = pygame.image.load("img/ground.png")

# Creating the bird image
# Using the pygame's sprite class to create the bird image
class Bird(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load("img/vamp1.png")
        self.images = []
        self.index = 0
        self.counter = 0 # this will be used to controll the speed of the animation
        # loading all the images of the bird
        for num in range(1, 3):
            img = pygame.image.load(f"img/vamp{num}.png")
            self.images.append(img) # adding the image to the list
        # setting the initial image of the bird
        self.image = self.images[self.index]
        self.rect = self.image.get_rect() # getting the rectangle of the image
        self.rect.center = (x, y) # setting the center of the image
        # Creating the bird's velocity
        self.vel_y = -15  # this is the vertical velocity of the bird
        self.clicked = False # this is used to check if the mouse is clicked
    
    # overiding the update method
    def update(self): 
  
        # Handles the bird's movement
        if flying == True:
            self.vel_y += 1 # this is the gravity
            if self.vel_y > 10:
                self.vel_y = 10 
            if self.rect.bottom < 810: # this is the ground
                self.rect.y += int(self.vel_y) 

        # Jump logic
        if game_over == False:
            if pygame.mouse.get_pressed()[0] == 1 and self.clicked == False: # this is used to check if the mouse is clicked
                self.clicked = True
                self.vel_y = -11
            if pygame.mouse.get_pressed()[0] == 0: # this is used to check if the mouse is not clicked
                self.clicked = False

            # Handles the animation of the bird
            self.counter += 1
            flap_cooldown = 5

            if self.counter > flap_cooldown:
                self.counter = 0
                self.index += 1
                if self.index >= len(self.images):
                    self.index = 0
            self.image = self.images[self.index] 

            # Rotate the bird
            self.image = pygame.transform.rotate(self.images[self.index], self.vel_y * -0.6 ) 
         
# Pipe class
class Pipe(pygame.sprite.Sprite):
    def __init__(self, x, y, position):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load("img/pipe.png")
        self.rect = self.image.get_rect() # getting the rectangle of the image
        # position 1 is bottom pipe, position -1 is top pipe
        if position == 1:
            self.image = pygame.transform.flip(self.image, False, True)
            self.rect.bottomleft = [x, y - int(pipe_gap / 2)] # setting the center of the image 
        if position == -1:
            self.rect.topleft = [x, y + int(pipe_gap / 2)] # setting the center of the image
 
    def update(self):
        self.rect.x -= scroll_speed
        if self.rect.right < 0:
            self.kill()

# creating the bird
bird_group = pygame.sprite.Group()
flappy = Bird(100, int(screen_height / 2))
bird_group.add(flappy)

# Pipe group
pipe_group = pygame.sprite.Group()
# Creating the pipe manually
#btm_pipe = Pipe(300, int(screen_height / 2), -1)
#tp_pipe = Pipe(300, int(screen_height / 2), 1)
#pipe_group.add(btm_pipe)
#pipe_group.add(tp_pipe)


# Creating the game loop 
run = True # initial condition is set to true
# Creating the while loop
# while run is true, the game will run (basically run whatever is in the loop while the condition is true)
while run: 

    clock.tick(fps)

    # in pygame blit is used to draw the image on the screen
    # Draw background first, then ground, then bird (back-to-front order)
    screen.blit(background, (0, 0))

  # drawing the bird and the pipe
    bird_group.draw(screen)
    bird_group.update()
    pipe_group.draw(screen)

    screen.blit(ground, (ground_scroll, 768)) # scrolling the ground image

    # Logic for the bird hitting the pipe
    if pygame.sprite.groupcollide(bird_group, pipe_group, False, False) or flappy.rect.top < 0 :
        game_over = True 

    # check if the bird has hit the ground
    if flappy.rect.bottom >= 790:
        game_over = True
        flying = False

    
    if game_over == False and flying == True:
        # Pipe spawning logic
        time_now = pygame.time.get_ticks()
        if time_now - last_pipe > pipe_frequency:
            pipe_height = random.randint(-100, 100)
            btm_pipe = Pipe(screen_width, int(screen_height / 2) + pipe_height, -1)
            tp_pipe = Pipe(screen_width, int(screen_height / 2) + pipe_height, 1)
            pipe_group.add(btm_pipe) 
            pipe_group.add(tp_pipe) 
            last_pipe = time_now

        # scrolling the ground image
        ground_scroll -= scroll_speed
        if abs(ground_scroll) > 35: # this is used to reset the ground scroll when it reaches a certain point
            ground_scroll = 0
        pipe_group.update() 
    
    # this is an event handler, without this the game will not quit.
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        if event.type == pygame.MOUSEBUTTONDOWN and flying == False and game_over == False:
            flying = True 

    # update the display (basically everything that is in the loop above)
    pygame.display.update() 
    
pygame.quit()