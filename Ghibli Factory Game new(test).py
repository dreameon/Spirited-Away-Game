"""
Name: Evelyn Law
Date: January 5th 2015
Assignment: CPT
Description: Ghibli Factory Game
Template taken from http://programarcadegames.com/python_examples/f.php?file=snake.py
"""

import pygame
import random
 
# Define some colors
WHITE = (255, 255, 255)
BLACK = (0,0,0)
BROWN = (0x99, 0x66, 0x00)


# Image height/width
width = 35

# Set initial speed
x_change = width
x_speed = 0
y_speed = 0


# -- Classes -----------------------------------------------------------------------------------------------------------------------------------------------

# Soot Sprite character taken from Studio Ghibli
# Class for Soots 
class Soot_sprite (pygame.sprite.Sprite):
    """ Class to represent one soot sprite of the line. """
    # -- Methods
    # Constructor function
    def __init__ (self, x, y):
        # Call parent's cunstructor
        super(Soot_sprite, self).__init__()
        self.image = pygame.image.load("soot.png").convert()

        # Make our top-left corner the passed-in location
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

        # Set brown as the transparent color
        self.image.set_colorkey(BROWN)

# Class for rocks      
class Rock(pygame.sprite.Sprite):
    """ Class to represent all the Items that the soot sprites can collide with """
    # -- Methods
    # Constructor function
    def __init__ (self, x, y):
        # Call parent's constructor
        super(Rock, self).__init__()

        # Image taken from: http://platformexplain.com/search/studio-ghibli-gif
        self.image = pygame.image.load("rock.png").convert()
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

        # Set blue as transparent colour
        self.image.set_colorkey(BROWN)

# Class for candies
class Food(pygame.sprite.Sprite):
    # -- Methods
    def __init__ (self, x, y):
        #Call Parent's Constructor 
        super(Food, self).__init__()

        # Image taken from: http://ensemble-stars.wikia.com/wiki/At_Your_Service!_UNDEAD_Cafe
        self.image = pygame.image.load("Konpeito.png").convert()
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

        # Set blue as transparent colour
        self.image.set_colorkey(BROWN)

# -- Function(s) -------------------------------------------------------------------------------------------------------------------------------------------------------------------   

# Subprogram to create rocks
def create_rock():
    rock = True
    rock_x = random.choice(range(0, 350)+ range(418, 765))
    rock_y = random.choice(range(0, 255)+ range(318, 570))
    
    while rock:
        if rock_x < food_x - 33 and rock_x > food_x + 30 and rock_y < food_x - 28 and rock_y > food_y + 31:
            rock_x = random.choice(range(0, 350)+ range(418, 765))
            rock_y = random.choice(range(0, 255)+ range(318, 570))
        else:
            rock = False
                            
    rock = Rock(rock_x, rock_y)
    allobjectslist.add(rock)
    rocklist.add(rock)
    rock_list.append(rock)
    
# ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

# Call this function so the Pygame library can initialize itself
pygame.init()
 
# Create an 800x600 sized screen
screen = pygame.display.set_mode([800, 600])
 
# This sets the name of the window
pygame.display.set_caption('Ghibli Factory Game')
 
# Before the loop, load the sounds (Songs taken from Studio Ghibli movie My Neighbour Totoro. Link: https://www.youtube.com/watch?v=yOs6G16RuTU):
backgroundmusic = pygame.mixer.Sound("BGM.ogg")

# Set positions of graphics
background_position = [0, 0]

# Load and set up graphics.
"""
Background image taken from http://www.desktopwallpapers4.me/abstract/wooden-floor-3244/
Menu image taken from https://share.oculus.com/app/spirited-away-the-boiler-room
Instructions image taken from http://secondhandsusie.blogspot.ca/2014/02/how-to-make-valentines-day-studio-ghibli-soot-sprite-valentines-present-DIY-pompom.html
"""
background_image = pygame.image.load("background.png").convert()
menu_image = pygame.image.load("main_menu.png").convert()
instructions_image = pygame.image.load("menu.png").convert()
game_over_image = pygame.image.load("game_over.png").convert()

allobjectslist = pygame.sprite.Group()
candylist = pygame.sprite.Group()
rocklist = pygame.sprite.Group()
sootlist = pygame.sprite.Group()
rock_list = []
sprite_list = []

# Create an initial soot
x = 383
y = 283
soot_sprite = Soot_sprite(x,y)
sprite_list.append(soot_sprite)
allobjectslist.add(soot_sprite)

# Create initial objects    
# random.choice function taken from http://stackoverflow.com/questions/10666661/can-python-generate-a-random-number-that-excludes-a-set-of-numbers-without-usin
food_x = random.choice(range(0, 353)+ range(418,770))
food_y = random.choice(range(0, 252)+ range(318,569))

candy = Food(food_x, food_y)
allobjectslist.add(candy)
candylist.add(candy)

# Create 5 initial rocks as obstacles
for i in range(5):
    create_rock()

game_over = False
score = 0
menu_start = True

clock = pygame.time.Clock() 
done = False

# Large number to assure that background music is always played.
backgroundmusic.play(100000)

# -- Main Program Loop
while not done:
    
    # -- Start Menu
    while menu_start:
        instructions = True 
        screen.blit(menu_image, background_position)
        large_font = pygame.font.SysFont('Monospace', 40, True, False)
        font = pygame.font.SysFont('Monospace', 30, True, False)
        text = large_font.render("Welcome to the Ghibli Factory", True, WHITE)
        right = font.render("Right key: Play game", True, WHITE)
        left = font. render("Left key: Instructions", True, WHITE)
        screen.blit(text, [50, 10])
        screen.blit(right, [100, 300])
        screen.blit(left, [100, 350])

        # See where to redirect user
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                menu_start = False
                done = True
                
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_e:
                    menu_start = False
                    done = True
                    pygame.quit()
                                   
                elif event.key == pygame.K_RIGHT:
                    menu_start = False
                        
                # Instructions guide
                elif event.key == pygame.K_LEFT:
                    while instructions:
                        screen.blit(instructions_image, background_position)
                        
                        small_font = pygame.font.SysFont('Monospace', 18, True, False)

                        pygame.draw.rect(screen, BLACK, [9, 200, 784, 200])
                        pygame.draw.rect(screen, BLACK, [190, 40, 500, 50])
        
                        instructions_manual = large_font.render("How to play the game", True, WHITE)
                        instructions_guide1 = small_font.render("Direct the soot sprite line using the keyboard keys", True, WHITE)
                        instructions_guide2 = small_font.render("(up, down, left, right) to eat the candies displayed on the screen", True, WHITE)
                        instructions_guide3 = small_font.render("But beware! Don't crash into the walls or the rocks or you'll die!", True, WHITE)
                        instructions_guide4 = small_font.render("Press 'E' to exit at any time.", True, WHITE)
                        instructions_guide5 = small_font.render("Please press the right key to exit menu.", True, WHITE)
                        screen.blit(instructions_manual, [200, 40])
                        screen.blit(instructions_guide1, [40, 210])
                        screen.blit(instructions_guide2, [40, 250])
                        screen.blit(instructions_guide3, [40, 290])
                        screen.blit(instructions_guide4, [40, 330])
                        screen.blit(instructions_guide5, [40, 370])
     
                        # Check to see if user made any movements
                        for event in pygame.event.get():
                            if event.type == pygame.QUIT:
                                instructions = False
                                menu_start = False
                                done = True
                                    
                            elif event.type == pygame.KEYDOWN:
                                if event.key == pygame.K_e:
                                    instructions = False
                                    menu_start = False
                                    done = True
                                    pygame.quit()
                                                    
                                elif event.key == pygame.K_RIGHT:
                                    instructions = False

                        pygame.display.flip()
                        clock.tick(60)
                        
            pygame.display.flip()
            clock.tick(60)
                            
    # -- Game screen
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True
       
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                x_speed = -1 * x_change
                y_speed = 0
            elif event.key == pygame.K_RIGHT:
                x_speed = x_change
                y_speed = 0
            elif event.key == pygame.K_UP:
                y_speed = -1* x_change
                x_speed = 0
            elif event.key == pygame.K_DOWN:
                y_speed = x_change
                x_speed = 0
            elif event.key == pygame.K_e:
                done = True

    # Get rid of last soot of the line
    # .pop() command removes last item in list
    old_soot = sprite_list.pop()
    allobjectslist.remove(old_soot)
    sootlist.remove(old_soot)
 
    # Insert new soot into the list
    sprite_list.insert(0, soot_sprite)
    allobjectslist.add(soot_sprite)

    # Figure out where new soot will be
    x = sprite_list[0].rect.x + x_speed
    y = sprite_list[0].rect.y + y_speed
    soot_sprite = Soot_sprite(x, y)
    
    # Draw everything
    screen.blit(background_image, background_position)

    allobjectslist.draw(screen)

    # Check if soot has collided with any objects
    candy_collision = pygame.sprite.spritecollide(sprite_list[0], candylist, True)
    rock_collision = pygame.sprite.spritecollide(sprite_list[0], rocklist, True)

    self_collision = pygame.sprite.spritecollide(sprite_list[0], sootlist, True)

    # Check if soot collided with self.
    for soot in self_collision:
        game_over = True
            
    # Check if soot collided with rock.
    for soot in rock_collision:
        game_over = True
        
    # Check if soot collided with candy.
    for soot in candy_collision:
        food = True
        score += 1

        # Add soot to line
        new_sootsprite = Soot_sprite(x,y)
        sprite_list.append(new_sootsprite)
        allobjectslist.add(new_sootsprite)
        sootlist.add(new_sootsprite)        

        # Make a new food with new locations
        food_x = random.randrange(0, 770)
        food_y = random.randrange(0, 569)
        
        # Loop to prevent food from landing on soot sprites or rocks
        while food:
            for i in range(len(sprite_list)):
                if food_x > sprite_list[i].rect.x - 30 and food_x < sprite_list[i].rect.x + 35 and food_y > sprite_list[i].rect.y -31 and food_y < sprite_list[i].rect.y +35:
                    food_x = random.randrange(0, 770)
                    food_y = random.randrange(0, 569)
                    i = 0
                
                else:
                    for j in range(5):
                        if food_x > rock_list[j].rect.x - 30 and food_x > rock_list[j].rect.x + 33 and food_y > rock_list[j].rect.y - 31 and food_y < rock_list[j].rect.y + 28:
                            food_x = random.randrange(0, 770)
                            food_y = random.randrange(0, 569)
                            j = 0
                        elif food_x > sprite_list[i].rect.x - 30 and food_x < sprite_list[i].rect.x + 35 and food_y > sprite_list[i].rect.y -31 and food_y < sprite_list[i].rect.y +35:
                            i = 0
                        else:
                            food = False
                    
        candy = Food(food_x, food_y)
        allobjectslist.add(candy)
        candylist.add(candy)

    

    # Check if soot has crashed into wall or self or rock. If so, game message appears and user is redirected to main menu.
    if sprite_list[0].rect.x < -10 or sprite_list[0].rect.x > 775 or sprite_list[0].rect.y < -10 or sprite_list[0].rect.y > 575 or game_over:
        screen.blit(game_over_image, background_position)
        font = pygame.font.SysFont('monospace', 35, True, False)
        text = font.render ("GAME OVER - you died!", True, WHITE)
        screen.blit(text, [150, 180])
        prompt_message = font.render ("Please press 'E' to exit.", True, WHITE)
        screen.blit(prompt_message, [150, 230])
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True
       
            elif event.type == pygame.KEYDOWN:
            
                if event.key == pygame.K_e:
                    done = True

    # Display score    
    font = pygame.font.SysFont('Monospace', 25, True, False)
    text = font.render ("Score: " + str(score), True, WHITE)
    screen.blit(text, [650,10])
   
    pygame.display.flip()
 
    clock.tick(5)
 
pygame.quit()
