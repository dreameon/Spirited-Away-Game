#Computer Science Culminating Performance 
#Course: ICS 3U1-02
#Authors: Susheel Kona, Pranav Krishnan, William Wang
#Date Modified: 1/12/2016

from random import randint #Include the randrange function from the random module
import pygame #Include the pygame module

#GLOBAL CONSTANTS

#Colours
BLACK    = (  0,   0,   0)
WHITE    = (255, 255, 255)
GREEN    = (0,   230,  77)
RED      = (255,   0,   0)
BROWN    = (131,  81,  54)
SKYBLUE  = (102, 194, 255)
ORANGE   = (255, 128,   0)
YELLOW   = (255, 255,   0)
PEAGREEN = (  0, 153,   0)
LAVARED  = (255,  50,   0)
LOGLST   = ["Welcome to The Quest for the Golden Head", "Press 1 for help text"]

#-------------------------------------------------------------------------------
class MovingSprite(pygame.sprite.Sprite):
    image = None
    currentLevel = None
    velocityX = None
    velocityY = None
    ammo = None
    currentFrame = None
    
    def __init__(self):
        #Call the parent constructor from sprite library
        super(MovingSprite, self).__init__()
        
        #Sets the surface of sprite
        self.image = pygame.Surface([30, 60])
        self.image.set_colorkey(WHITE)
        
        #Sets default ammo of enemy
        self.ammo = 99999
        
        #Set speed to 0 for both horizontal and vertical movement
        self.velocityX = 0
        self.velocityY = 0

        self.currentFrame = 0
        
        #Create a rect to set the location of the sprite
        self.rect = self.image.get_rect()
        
    def update(self):
        #Calculate the Gravity
        self.getGravity()
        
        #Move left and right
        self.rect.x += self.velocityX
            
        #Check if update of position cause sprite to collide with an object
        collisionList = pygame.sprite.spritecollide(self, self.currentLevel.platforms, False)
        for item in collisionList:
            #If we are moving right, set sprite's right to the wall/platform's left side
            if self.velocityX > 0:
                self.rect.right = item.rect.left
            #If we are moving left, do the exact opposite
            else:
                self.rect.left = item.rect.right
        
        #Move up and down
        self.rect.y += self.velocityY
        
        #Check if update of position cause sprite to collide with an object
        collisionList = pygame.sprite.spritecollide(self, self.currentLevel.platforms, False)
        for item in collisionList:
            #If we are moving down, set sprite's bottom to the wall/platform's top side
            if self.velocityY > 0:
                self.rect.bottom = item.rect.top
            #If we are moving up, do the exact opposite
            else:
                self.rect.top = item.rect.bottom
            self.velocityY = 0

        self.currentFrame += 1
    
    def getGravity(self):
        #Increase sprite's downward speed
        self.velocityY += 0.45
        
        #If sprite is on the ground and is moving downward, set sprite vertical speed to 0
        '''
        if self.rect.y > 731 and self.velocityY >= 0:
            self.velocityY = 0
            self.rect.y = 718
        '''
        
    def jump(self):
        #Increase y position by 2 to check if it is okay to jump
        self.rect.y += 2
        
        #Make a collision list to check if sprite collides with platform when moved down
        collisionList = pygame.sprite.spritecollide(self, self.currentLevel.platforms, False)
        
        #Reset y position of sprite to original value
        self.rect.y -= 2
        
        #If sprite hit a platform when y pos was increased (means it is on a platform), 
        #or if the sprite is on the ground, make sprite jump
        if len(collisionList) > 0 or self.rect.y > 717:
            self.velocityY = -10
    
    def move(self, change):
        #Move sprite according to parameter
        self.velocityX = change
        
    def stopMoving(self):
        #Set sprite's speed to 0
        self.velocityX = 0
        
        
    def shoot(self, bulletVelocity):
        #Creates a bullet if sprite has ammo
        if (self.ammo > 0):
            
            #Subtract 1 from ammo and create a bullet
            self.ammo -= 1
            
            #Check if it's an enemy or player bullet being fired
            if (self in self.currentLevel.enemies):
                bullet = Bullet(self, bulletVelocity, RED)
                self.currentLevel.enemyBullets.add(bullet)
            else:
                bullet = Bullet(self, bulletVelocity, PEAGREEN)
                self.currentLevel.playerBullets.add(bullet)
                
            
            
            #Add this bullet to the current level's all sprites list, so that it can be updated
            self.currentLevel.allSprites.add(bullet)
            
             
#-------------------------------------------------------------------------------
class Player(MovingSprite):
    #ATTRIBUTES
    hasArms = None
    hasLegs = None
    health = None
    ammo = None
    currentLevel = None
    score = None
    coins = None
    level1 = None
    level2 = None
    indexWalk = None
    imageLstLevel2 = []
    levelFinished = None
    isKicking = None
    
    #Constructor methid
    def __init__(self):
        super(Player, self).__init__()
        
        #Override default ammo of moving sprite class and set defualt ammo of player
        self.ammo = 20
        
        #Set the initial score and health of the player
        self.score = 0
        self.health = 100
        self.coins = 0

        #Load Player Images
        self.level1 = importImage("images/player/Level1.png")
        self.level2 = importImage("images/player/Level2.png")
        self.imageLstLevel2.append(importImage("images/player/Level2Walk1.png"))
        self.imageLstLevel2.append(importImage("images/player/Level2Walk2.png"))

        #Set the player's image
        self.image = self.level2
        self.image.set_colorkey(WHITE)
        
        #Set the start position of the player
        self.rect.x = 150
        self.rect.y = 150

        #Set the initial walk image
        self.indexWalk = 0
        
        isKicking = False
        #Add Sprite Image list to update
        
    def shoot(self, bulletVelocity):
        
        #Call the parent shoot method to fire bullet
        super(Player, self).shoot(bulletVelocity)
            
    def walk(self):

        #If 15 frames have passed, change walk image
        if (self.velocityX != 0):
            self.image = self.imageLstLevel2[self.indexWalk]

            #If all images have been run through change the image back to the 1st
            if (self.indexWalk == 1):
                self.indexWalk = 0
            else:
                self.indexWalk += 1
                
#-------------------------------------------------------------------------------       
class Enemy(MovingSprite):
    jumpTime = None
    orgPos = None
    
    def __init__(self, pos):
        
        #Call the parent MovingSprite Constructor
        super(Enemy, self).__init__()
        
        #Set the enemy position based on parameter
        self.rect.x = pos[0]
        self.rect.y = pos[1]
        self.orgPos = pos
        
        #Set the image of the enemy
        self.image = importImage("images/enemy.png")
        self.image.set_colorkey(WHITE)        
        
        #Give the enemy almost unlimited ammo
        self.ammo = 2e64
        
        #Set the interval between jumps to random
        self.jumpTime = randint(45, 120)
    
        
    
    
    #Shoots the player (Overrided method)
    #Parameters: target to shoot (player)
    def shoot(self, target):
        
        #Check where the target it relative to this enemy, and fire in the direction of the target
        if (target.rect.x < self.rect.x):
            bulletVelocity = -15
        else:
            bulletVelocity = 15
            
        #Only shoot if the player is near the enemy
        if (abs(target.rect.x - self.rect.x) < 500 and abs(target.rect.y - self.rect.y) < 50):
            #Call the parent bullet method to shoot the bullet
            super(Enemy, self).shoot(bulletVelocity)
            
    #Makes the enemy jump (Overrided Method)
    def jump(self, player):
        
        #Only jump if the player is near
        if (abs(player.rect.x - self.rect.x) < 700 and abs(player.rect.y - self.rect.y) < 400):
            super(Enemy, self).jump()
            

#-------------------------------------------------------------------------------
class Platform(pygame.sprite.Sprite):
    #ATTRIBUTES
    image= None
    rect = None
    
    #Constructor Method
    #Parameters: position of platform, and dimensions of platform 
    def __init__(self, pos, dimensions, imageType):
        
        super(Platform, self).__init__()
        
        #Set the dimensions of the plaform, and color it brown
        self.image = pygame.Surface(dimensions)
        
        if (imageType == "platform"):
            self.image.blit(importImage("images/grassPlat.png"), [0,0])
        elif (imageType == "ground"):
            self.image.blit(importImage("images/grassGround.png"), [0,0])

        else:
            self.image.fill(BROWN)
        
        #Set the location of the platform
        self.rect=self.image.get_rect()
        self.rect.x=pos[0]
        self.rect.y=pos[1]
        
#-------------------------------------------------------------------------------
class Obstacle(pygame.sprite.Sprite):
    resetPos = []
    
    #Constructor Method
    def __init__(self, pos, dimensions, image):
        
        #Call the parent pygame constructor
        super(Obstacle, self).__init__()
        
        #Set the dimensions of the obstacle
        self.image = pygame.Surface(dimensions)
        
        #Set the position of the obstacle
        self.rect = self.image.get_rect()
        self.rect.x = pos[0]
        self.rect.y = pos[1]
        
        if (image == 'lava'):
            self.image.fill(LAVARED)
            
        else:
            pass

        
#-------------------------------------------------------------------------------
class Level(object):
    #ATTRIBUTES
    platforms = None
    coins = None
    enemies = None
    obstacles = None
    allSprites = None
    worldShift = None
    maxWorldShift = None
    playerBullets = None
    enemyBullets = None
    textList = None
    images = None
    #backgroundImg = None
    
    #Constructor Method
    def __init__(self):
        
        #Initialize the Sprite lists
        self.collisionObjects = pygame.sprite.Group()
        self.enemies = pygame.sprite.Group()
        self.allSprites = pygame.sprite.Group()
        self.platforms = pygame.sprite.Group()
        self.coins = pygame.sprite.Group()
        self.playerBullets = pygame.sprite.Group()
        self.enemyBullets = pygame.sprite.Group()
        self.obstacles = pygame.sprite.Group()
        
        #Control the world shift
        self.worldShift = 0 #This controls how much to shift the world
        self.maxWorldShift = 1000 # This is the world shift necessary for the level to end
        
        self.textList = []
        self.images = []
    
     
    #Method to generate the platforms and enemies
    #Parameters: 2D list of platform info, 2D list of enemy positions, 2D list of coin positions, list of text box positions
    def generateLevel(self, platforms, enemies, coins, text, imageList, obstacles = []):
        
        #Iterate through the supplied platform information and create Platform objects
        for plat in platforms:
            platform = Platform([plat[0], plat[1]], [plat[2], plat[3]], plat[4])
            
            #Add the created platforms to the respective sprite lists
            self.platforms.add(platform)
            self.allSprites.add(platform)
            
        #Iterate through the supplied enemy position and create Enemy objects
        for enem in enemies:
            enemy = Enemy([enem[0], enem[1]])
            enemy.currentLevel = self
            
            #Add the created enemy to the respective sprite lists
            self.enemies.add(enemy)
            self.allSprites.add(enemy)
            
        #Iterate through the supplied coin positions and create Coin objects
        for coinPos in coins:
            coin = Coin(coinPos)
            
            #Add the created coin to the respective sprite lists
            self.coins.add(coin)
            self.allSprites.add(coin)
            
        #Iterate throught the supplied text box information and create text boxes
        for texts in text:
            self.textList.append(texts)
            
        #Iterate through the supplied image information and create images
        for img in imageList:
            self.images.append([importImage(img[0]), img[1], img[2]])
            
        #Iterate through the supplied image information and create images
        for obs in obstacles:
            obstacle = Obstacle([obs[0], obs[1]], [obs[2], obs[3]], obs[4])
            self.obstacles.add(obstacle)
            self.allSprites.add(obstacle)

    
    #Shifts the level (called when player approches right side of screen)
    #Parameters: Value to shift level
    def scroll(self, value):
        
        #Keep track of how much the level has been shifted
        self.worldShift += value
        
        #Shift all the platforms
        for sprite in self.platforms:
            sprite.rect.x += value
        
        #Shift all the coins
        for sprite in self.coins:
            sprite.rect.x += value
            
        #Shift the texts
        for texts in self.textList:
            texts[1] += value
            
        #Shift the images
        for img in self.images:
            img[1] += value
            pass
        
        #Shift all of the obstacles
        for obs in self.obstacles:
            obs.rect.x += value
        
        #Shift all of the enemies
        for enem in self.enemies:
            enem.rect.x += value
        
        
    #Method to update all sprites and draw the level to the screen
    #Parameters: Screen to draw on
    def draw(self, screen):
        
        #Draw the background
        screen.fill(WHITE)
        
        #Draw the sprites
        self.allSprites.draw(screen)
        
        #Draw texts
        for texts in self.textList:
            text = font1.render(texts[0], True, BLACK)
            screen.blit(text, [texts[1], texts[2]])
            
        #Draw images
        for img in self.images:
            screen.blit(img[0], [img[1], img[2]])
            

        
#-------------------------------------------------------------------------------
class Coin(pygame.sprite.Sprite):
    #ATTRIBUTES
    image=None
    
    #Constructor Method
    #Parameters: position of coin
    def __init__(self, pos):
        
        #Call the parent pygame sprite constructor
        super(Coin, self).__init__()
        
        #Set the coin's size, graphic and position
        self.image = pygame.Surface([45, 50])
        self.image = importImage("images/coin.png")
        self.image.set_colorkey(WHITE)
        self.rect = self.image.get_rect()
        self.rect.x = pos[0]
        self.rect.y = pos[1]
        

#-------------------------------------------------------------------------------
class Bullet(pygame.sprite.Sprite):
    
    #ATTRIBUTES
    velocityX = None
    image=None
    
    #Constructor Method
    #Parameters: sprite who shoots bullet, algebraic speed of bullet, color
    def __init__(self, shooter, velocityX, color):
        
        #Call the parent pygame sprite constructor
        super(Bullet, self).__init__()
        
        #Create the Bullet image
        self.image = pygame.Surface([10, 10])
        self.rect=self.image.get_rect()
        self.image.fill(color)
        #Set the bullet's position to the shooter
        self.rect.x = shooter.rect.x 
        self.rect.y = shooter.rect.y
        
        #Set the x velocity based on parameter
        self.velocityX = velocityX
    
    #Updates the position of the bullet
    def update(self):
        
        #Move the bullet
        self.rect.x += self.velocityX
    

#-------------------------------------------------------------------------------
def displayHud(level, health, coin, ammo, score, disHud, disLog, logLst):                
    # HUD
    # If player toggles HUD on, display HUD
    if (disHud == True):
        # HUD background
        pygame.draw.rect(screen, SKYBLUE, [0, 0, 1366, 50], 0)
        # Change colour of health box based on health remaining
        if (health <= 10):
            boxColour = RED
        elif (health <= 25):
            boxColour = ORANGE
        elif (health <= 50):
            boxColour = YELLOW
        else:
            boxColour = GREEN

        # Draw health bar based on health remaining
        if (health > 0):
            pygame.draw.rect(screen, boxColour, [235, 10, 2*health , 30], 0)   
        
        # Render text
        levelText  = font1.render('Level: ' + str(level), True, BLACK)
        healthText = font1.render('Health', True, BLACK)
        # Health bar displays a minimum of 0 health
        if (health < 0):
            healthNum  = font1.render('0/100', True, BLACK)
        else:
            healthNum  = font1.render(str(health) + '/100', True, BLACK)
        coinsText  = font1.render('Coins: x' + str(coin).zfill(3), True, BLACK)
        ammoText   = font1.render('Ammo: ' + str(ammo) + '/20'   , True, BLACK)
        scoreText  = font1.render('Score: ' + str(score).zfill(6), True, BLACK)
        timeText   = font1.render('Time: ' + str(time).zfill(3)  , True, BLACK)
        # Display text
        screen.blit(levelText ,  [15, 15])
        screen.blit(healthText, [150, 15])
        screen.blit(healthNum , [300, 15])
        screen.blit(coinsText , [485, 15])
        screen.blit(ammoText  , [650, 15])
        screen.blit(scoreText , [815, 15])
        screen.blit(timeText  ,[1000, 15])

    # Log
    # If player toggles log on, display log
    if (disLog == True):
        pygame.draw.rect(screen, BLACK, [965, 50, 400, 155], 2)
        
        logPos = 190
        # Text in log is only printed within  box
        for i in range(-1, -len(logLst)-1, -1):
            # Render text
            bottom = font2.render(logLst[i], True, BLACK)
            # Display text 
            if (logPos >= 50):
                screen.blit(bottom, [970, logPos])
            logPos -= 15

            
#-------------------------------------------------------------------------------
#Imports an image
#Parameters: path of image
def importImage(path):
    image = pygame.image.load(path)
    return image

    
#-------------------------------------------------------------------------------
#Ends the game
#Parameters: Screen to draw on, player that ended game, reason for ending
def displayEndScreen(screen, player, reason):
        #Render the text to display score
        score = gameOverFont.render("Your score was: " + str(player.score), True, WHITE)
        bgMusic.fadeout(500)
        
        #Check the reason for ending the game
        if (reason == 'lose'):
            
            #Color the screen Red
            screenColor = RED
            
            #Render text
            msg   = gameOverFont.render("Oh dear, you died!", True, WHITE)
            
        elif (reason == 'time'):
            screenColor = ORANGE
            msg = gameOverFont.render("Looks like you're out of time!", True, WHITE)
        else:
            
            #Color the screen Green
            screenColor = PEAGREEN
            
            #Render text
            msg = gameOverFont.render("Yay! You Won!", True, WHITE)
            
            
        #Display text and color screen
        screen.fill(screenColor)
        screen.blit(msg  , [500, 350])
        screen.blit(score, [550, 450])
            
    
'''
MAIN PROGRAM
'''
if (__name__=='__main__'):
    
    pygame.init()
    
    #Set time limit
    time = 180
    
    #Fonts
    font1        = pygame.font.SysFont("Consolas", 20, False, False)
    font2        = pygame.font.SysFont("Consolas", 14, False, False)
    gameOverFont = pygame.font.SysFont("Consolas", 30, False, False)
    
    #Sounds
    coinSound = pygame.mixer.Sound("sounds/coin.ogg")
    coinSound.set_volume(0.05)
    playCoinSound = True
    bgMusic = pygame.mixer.Sound("sounds/bgMusic.ogg")
    bgMusic.set_volume(0.25)
    jumpSound = pygame.mixer.Sound("sounds/jump.ogg")
    playBgMusic = True
    shootSound = pygame.mixer.Sound("sounds/shoot.ogg")
    bgMusic.play()
    
    #Set the width and height of the screen [width, height]
    size = (1366, 768)
    screen = pygame.display.set_mode(size)
    
    #Set the Screen Title
    pygame.display.set_caption("The Quest for the Golden Head")
     
    #Main Loop Control
    done = False
     
    #Used to manage how fast the screen updates
    clock = pygame.time.Clock()
    
    #List of levels
    allLevels=[]
    
    #Generate the levels
    for i in range(3):
        
        #Check which level should be generated next, then make the level information
        if (i==0):
            platformInfo = [ [  700, 728, 1200,  50,   'ground'], 
                             [ 2450, 728,  550,  50,   'ground'], 
                             [ 3625, 728, 1375,  50,   'ground'],
                             [ 6500, 728, 1275,  50,   'ground'],
                             [ 9510, 728,  490,  50,   'ground'],
                             #----------------------------------
                             [ -350,   0,  350, 768,     'wall'], 
                             [    0, 268,  700, 500,   'ground'],
                             [ 1000, 628,  300,  50, 'platform'], 
                             [ 1450, 528,  300,  50, 'platform'],
                             [ 1900, 528,  550, 240,   'ground'],
                             #----------------------------------
                             [ 3175, 628,  300,  50, 'platform'],
                             [ 3650, 528, 1000,  50, 'platform'],
                             #----------------------------------
                             [ 5000, 678,  100, 100, 'platform'],
                             [ 5100, 628,  100, 150, 'platform'],
                             [ 5200, 578,  100, 200, 'platform'],
                             [ 5300, 528,  100, 250, 'platform'],
                             [ 5400, 478,  100, 300, 'platform'],
                             [ 5500, 428,  100, 350, 'platform'],
                             [ 5600, 378,  100, 400, 'platform'],
                             #----------------------------------
                             [ 5800, 378,  100, 400, 'platform'],
                             [ 5900, 428,  100, 350, 'platform'],
                             [ 6000, 478,  100, 300, 'platform'],
                             [ 6100, 528,  100, 250, 'platform'],
                             [ 6200, 578,  100, 200, 'platform'],
                             [ 6300, 628,  100, 150, 'platform'],
                             [ 6400, 678,  100, 100, 'platform'],
                             #----------------------------------
                             [ 6200, 378,  300,  50, 'platform'],
                             [ 6600, 268,  300,  50, 'platform'],
                             [ 7000, 628,  750,  20, 'platform'],
                             [ 7925, 528,  200,  50, 'platform'],
                             [ 8300, 428,  200,  50, 'platform'],
                             [ 8675, 328,  200,  50, 'platform'],
                             [ 8775, 678,  200,  50, 'platform'],
                             #----------------------------------
                             [ 9000, 678,  500, 100,   'ground'],
                             [ 8990, 563,  310,  50, 'platform'],
                             [ 9150, 448,  350,  50, 'platform'],
                             [ 9300, 333,  100,  50, 'platform'],
                             [ 9150, 303,  100,  50, 'platform'],
                             [ 9000, 273,  100,  50, 'platform'],
                             [ 9050, 158,  460,  50, 'platform'],
                             #----------------------------------
                             [ 8990, 158,   10, 405, 'platform'],
                             [ 9500, 208,   10, 615,     'wall'],
                             [10000,   0,  150, 768,     'wall'] ]
                                                      
            coinPos = [ [  780, 118], 
                        [  830, 148],
                        [  870, 188],
                        [ 1510, 675],
                        [ 1565, 675],
                        [ 1620, 675],
                        [ 1310, 520], 
                        [ 1350, 480],
                        [ 1400, 450],
                        #-----------
                        [ 2075, 378],
                        [ 2130, 378],
                        [ 2185, 378],
                        #-----------
                        [ 3035, 620],
                        [ 3075, 580],
                        [ 3125, 550],
                        [ 3510, 520],
                        [ 3550, 480],
                        [ 3600, 450],
                        [ 4700, 450],
                        [ 4750, 480],
                        [ 4790, 520],
                        #-----------
                        [ 5675, 258],
                        [ 5725, 228],
                        [ 5775, 258],
                        [ 6100, 370],
                        [ 6140, 330],
                        [ 6190, 300],
                        [ 6500, 260],
                        [ 6540, 220],
                        [ 6590, 190],
                        #-----------
                        [ 7270, 678],
                        [ 7320, 678],
                        [ 7370, 678],
                        [ 7420, 678],
                        [ 7470, 678],
                        #-----------
                        [ 7785, 520],
                        [ 7825, 480],
                        [ 7875, 450],
                        [ 8160, 420],
                        [ 8200, 380],
                        [ 8250, 350],
                        [ 8535, 320],
                        [ 8575, 280],
                        [ 8625, 250],
                        #-----------
                        [ 8930, 398], 
                        [ 8930, 448],
                        [ 8930, 488],
                        [ 9300, 508], 
                        [ 9340, 528],
                        [ 9380, 558],
                        [ 9060, 440], 
                        [ 9100, 400],
                        [ 9150, 370],
                        #-----------
                        [ 9630,  78],
                        [ 9680, 108],
                        [ 9720, 148], 
                        [ 9750, 198],
                        [ 9770, 258] ]
            
            enemyPos = [ [ 2145, 468],
                         [ 3300, 568],
                         [ 4135, 468],
                         [ 5035, 618],
                         [ 5435, 418],
                         [ 6335, 318],
                         [ 6735, 208],
                         [ 8760, 268],
                         [ 9235, 618],
                         [ 9085, 503],
                         [ 9185, 503],
                         [ 9285, 388],
                         [ 9335, 273],
                         [ 9185, 243] ]
            
            obstacles = [ [3000, 738,  625,  40, 'lava'],
                          [5700, 468,  100, 300, 'lava'],
                          [7775, 743, 1275,  50, 'lava'] ]
                         
            text = [ ["Press M for Help and Controls", 100, 75] ]
            imgList=[]
            
        elif (i==1):
            platformInfo=[ [ -150,   0,  150,  768,   'wall'],
                           [ 1950,   0,  150,  768,   'wall'],
                           [    0, 750, 1950, 1950, 'ground'],
                           [  150, 680,  200,   50,'platform'],
                           [  325, 580,  200,   50,'platform'],
                           [  500, 480,  200,   50,'platform'] ]
    
                    
            imgList = []           
            coinPos = []
            text = []
            enemyPos = []
            
        #Generate the level
        level = Level()
        level.generateLevel(platformInfo, enemyPos, coinPos, text, imgList, obstacles)
        allLevels.append(level)
        
    allLevels[0].maxWorldShift = 9900
        
    currentLevelNo = 0
    
    #Player
    player = Player()
    player.currentLevel = allLevels[currentLevelNo]
    
    #Lists
    players = pygame.sprite.Group()
    players.add(player)
    
    dispHud = True
    dispLog = False
    playerWon = False
    outOfTime = False
    
    #-------- Main Program Loop -----------
    while (not done):
        
        # --- Main event loop
        for event in pygame.event.get():
            if (event.type == pygame.QUIT):
              done = True
              
            if (event.type  == pygame.KEYDOWN):
                #Help text
                if (event.key == pygame.K_1):
                    LOGLST.append("Use arrow keys to move left/right.")
                    LOGLST.append("Press SPACE to jump.")
                    LOGLST.append("Press A to shoot left and D to shoot right.")
                    LOGLST.append("Press M to toggle log.")
                    LOGLST.append("Press H to toggle HUD.")
                    LOGLST.append("Press 3 to remove coin sound.")   
                #Toggle coin sound
                if (event.key == pygame.K_3):
                    if (playCoinSound == True):
                        playCoinSound = False
                        LOGLST.append("You toggled coin sound off")
                    else:
                        playCoinSound = True
                        LOGLST.append("You toggled coin sound on")
                #Player movement controls
                if (event.key == pygame.K_LEFT):
                    player.move(-6)
                if (event.key == pygame.K_RIGHT):
                    player.move(6)
                if (event.key == pygame.K_SPACE):
                    jumpSound.play()
                    player.jump()
                #Player shooting controls
                if (event.key == pygame.K_a):
                    player.shoot(-15)
                    shootSound.play()
                if (event.key == pygame.K_d):
                    player.shoot(15)
                    shootSound.play()
                #Fly hack
                if (event.key == pygame.K_RETURN):
                    player.velocityY -= 10
                    
                if (event.key == pygame.K_l):
                    player.health = 100

                '''
                if (event.key == pygame.K_a):
                    player.image = importImage("images/player/Level2KickLeft.png")
                    enemiesCollided = pygame.sprite.spritecollide(player, player.currentLevel.enemies, True)
                    for enem in enemiesCollided:
                        score += 50
                if (event.key == pygame.K_d):
                    player.image = importImage("images/player/Level2KickRight.png")
                    enemiesCollided = pygame.sprite.spritecollide(player, player.currentLevel.enemies, True)
                    for enem in enemiesCollided:
                        player.score += 50
                '''

                #Toggle HUD
                if (event.key == pygame.K_h):
                    if (dispHud == False):
                        dispHud = True
                    else:
                        dispHud = False
                #Toggle log
                if (event.key == pygame.K_m):
                    if (dispLog == False):
                        dispLog = True
                    else:
                        dispLog = False
                        
            if (event.type == pygame.KEYUP):
                if ((event.key  ==  pygame.K_RIGHT and player.velocityX > 0) or (event.key == pygame.K_LEFT and player.velocityX < 0)):
                    player.move(0)
                    player.image = player.level2
                if (event.key == pygame.K_a or event.key == pygame.K_d):
                    player.image = player.level2
                    isKicking = False


        #--- Game logic --------------------------------------------------------
        grossPosition = player.rect.x - player.currentLevel.worldShift
        
        #--COLLISIONS
        
        #Check if the player collects any coins
        coinList = pygame.sprite.spritecollide(player, player.currentLevel.coins, True)
        
        #Iterate through the coins the player collided with
        for coin in coinList:
            #Give the player points and play sound
            player.score += 100
            if (playCoinSound == True):
                coinSound.play()
            
            #Remove the collected coins from the sprite lists to prevent redrawing
            player.currentLevel.allSprites.remove(coin)
            player.currentLevel.coins.remove(coin)
            
            #Add 1 to the player's coins, and give him a small jump
            player.coins += 1
            player.rect.y -= 5
        
        #Check if the player collided with any obstacles
        obsCollided = pygame.sprite.spritecollide(player, player.currentLevel.obstacles, False)
        
        #Iterate through the collided obstacles
        for obs in obsCollided:
            player.health -= 20
            player.rect.x = obs.rect.x - 200
            player.rect.y = obs.rect.y - 200
            LOGLST.append("You fell in lava! That's deadly")
        
        enemiesCollided = pygame.sprite.spritecollide(player, player.currentLevel.enemies, True)
        
        for enem in enemiesCollided:
            player.rect
            player.health -= 20
            LOGLST.append("You ran into an enemy! Be careful!")
            
        #BULLET COLLISIONS:
        for bull in player.currentLevel.playerBullets:
            bulletsCollidedEnem = pygame.sprite.spritecollide(bull, player.currentLevel.enemies, True)
            
            for item in bulletsCollidedEnem:
                player.currentLevel.playerBullets.remove(bull)
                player.currentLevel.allSprites.remove(bull)
                player.currentLevel.playerBullets.remove(item)
                player.currentLevel.allSprites.remove(item)
                player.score += 250
                LOGLST.append("You shot an enemy!")

        for bull in player.currentLevel.playerBullets:
            bulletsCollidedPlats = pygame.sprite.spritecollide(bull, player.currentLevel.platforms, False)
            
            for item in bulletsCollidedPlats:
                player.currentLevel.playerBullets.remove(bull)
                player.currentLevel.allSprites.remove(bull)
                
        for bull in player.currentLevel.enemyBullets:
            bulletsCollidedPlats = pygame.sprite.spritecollide(bull, player.currentLevel.platforms, False)
            
            for item in bulletsCollidedPlats:
                player.currentLevel.enemyBullets.remove(bull)
                player.currentLevel.allSprites.remove(bull)
                
            bulletsCollidedPlayer = pygame.sprite.spritecollide(player, player.currentLevel.enemyBullets, False)
            player.health -= (5*len(bulletsCollidedPlayer))
            
            for bull in bulletsCollidedPlayer:
                player.rect.x -= -bull.velocityX
                player.currentLevel.allSprites.remove(bull)
                player.currentLevel.enemyBullets.remove(bull)

        #Check if player has reached the right side of the screen
        if (player.rect.x >= 1000):
            distancePast = 1000 - player.rect.x
            player.rect.x = 1000
            player.currentLevel.scroll(distancePast)
        
        #Check if the player has reached the left side of the screen
        if (player.rect.x < 300):
            distancePast = 300 - player.rect.x
            player.rect.x = 300
            player.currentLevel.scroll(distancePast)
            
        #Check if the player has reached the  end of the level
        if (grossPosition >= player.currentLevel.maxWorldShift):
            
            #If the player is not on the last level, advance levels
            if( currentLevelNo == 1):
                playerWon = True
            else:
                #Change the variable that controls the level
                currentLevelNo += 1

                #Reset the player's position
                player.rect.x = 150
                player.rect.y = 150

                #Set the player's new sprite
                player.image = player.level2
                player.rect.height = 60
                
    
        #Set the player's current Level to the selected level
        player.currentLevel = allLevels[currentLevelNo]
            
        #Walking animation every 15 frames
        if (player.currentFrame % 15 == 0):
            player.walk()
            
        #Make enemies shoot every 30 frames 
        if (player.currentFrame % 30 == 0):
            
            #Iterate through all the enemies in the level
            for enemy in player.currentLevel.enemies:
                enemy.shoot(player)
        
        #Time
        if (player.currentFrame % 60 == 0):
            time -= 1
                
        #Make every enemy jump at their interval
        for enemy in player.currentLevel.enemies:
            
            #Check if this frame is the interval between jumps for this enemy
            if (player.currentFrame % enemy.jumpTime == 0):
                enemy.jump(player)

        #Update the position of the player, and all of the sprites in the current Level
        player.update()
        player.currentLevel.allSprites.update()
        
        #--- Drawing code
        
        #If the player dies, display the end screen
        if (player.health <= 0):
            displayEndScreen(screen, player, 'lose')
            
            #Stop the player from moving
            player.rect.x = 50
            player.rect.y = 50
        
        elif (playerWon):
            displayEndScreen(screen, player, 'won')
            
            #Stop the player from moving
            player.rect.x = 50
            player.rect.y = 50
            
        elif (time <= 1):
            displayEndScreen(screen, player, 'time')
            
            #Stop the player from moving
            player.rect.x = 50
            player.rect.y = 50
        
        else:
            player.currentLevel.draw(screen)
            players.draw(screen)
            displayHud(currentLevelNo + 1, player.health, player.coins, player.ammo, player.score, dispHud, dispLog, LOGLST)

        #--- Update the screen
        #print ("Pos: "+str(player.rect)+'\nGross: '+str(grossPosition)+'\nScore: '+str(player.score)+'\nAmmo: '+str(player.ammo)+'\nLevel: '+str(currentLevelNo+1))
        pygame.display.flip()
     
        #--- Limit to 60 frames per second
        clock.tick(60)
    
    #Close the Window
    pygame.quit()
