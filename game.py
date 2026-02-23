import pygame
from pygame.locals import *

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
                self.vel_y = -15
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
            self.image = pygame.transform.rotate(self.images[self.index], self.vel_y * -0.5 ) 

         

         

# creating a group of birds
bird_group = pygame.sprite.Group()
flappy = Bird(100, int(screen_height / 2))
bird_group.add(flappy)
 
# Creating the game loop 
run = True # initial condition is set to true
# Creating the while loop
# while run is true, the game will run (basically run whatever is in the loop while the condition is true)
while run: 

    clock.tick(fps)

    # in pygame blit is used to draw the image on the screen
    # Draw background first, then ground, then bird (back-to-front order)
    screen.blit(background, (0, 0))

  # drawing the bird
    bird_group.draw(screen)
    bird_group.update() 

    screen.blit(ground, (ground_scroll, 768)) # scrolling the ground image

    # check if the bird has hit the ground
    if flappy.rect.bottom > 790:
        game_over = True
        flying = False
 

    # scrolling the ground image
    if game_over == False:
        ground_scroll -= scroll_speed
        if abs(ground_scroll) > 35: # this is used to reset the ground scroll when it reaches a certain point
            ground_scroll = 0
    
    # this is an event handler, without this the game will not quit.
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        if event.type == pygame.MOUSEBUTTONDOWN and flying == False and game_over == False:
            flying = True 

    # update the display (basically everything that is in the loop above)
    pygame.display.update() 
    
pygame.quit()