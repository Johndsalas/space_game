
import pygame
import random as r
import math as m

from pygame import mixer

# initilize pygame
pygame.init()

# create the screen
screen= pygame.display.set_mode((800, 600))

# title and icon 32 X 32 for icon
pygame.display.set_caption("Space Game")

icon = pygame.image.load('alien_32.png')
pygame.display.set_icon(icon)

# create background
background = pygame.image.load('space.png')

# create sound loop
mixer.music.load("background.wav")
mixer.music.play(-1)

# player
# Load player icon and starting position
player_img = pygame.image.load('spaceship_64.png')
playerX = 370
playerY = 530
playerX_change = 0

# enemy
enemy_img = []
enemyX = []
enemyY = []
enemyX_change = []
enemyY_change = []
num_of_enemies = 6

for i in range(num_of_enemies):
    enemy_img.append(pygame.image.load('alien_64.png'))
    enemyX.append(r.randint(0,735))
    enemyY.append(r.randint(50,150))
    enemyX_change.append(4)
    enemyY_change.append(40)

# bullet
# ready means you can't see bulet on the screen
# fire means the bullet is moving
bullet_img = pygame.image.load('bullet_32.png')
bulletX = 0
bulletY = 480
bulletX_change = 0
bulletY_change = 10
bullet_state = "ready"

# score
score_value = 0
font = pygame.font.Font('freesansbold.ttf',32)

textX = 10
textY = 10

# Game Over
over_font = pygame.font.Font('freesansbold.ttf', 64)


def player(x,y):
    '''takes in updated coordinats and displays player image on the screen at given coordinates'''

    screen.blit(player_img,(x,y))
    
def enemy(x,y,i):
    '''takes in updated coordinats and displays enemy image on the screen at given coordinates'''

    screen.blit(enemy_img[i],(x,y))
    
def fire_bullet(x,y):
    '''takes in updated coordinats and displays bullet immage and moves bullet accross the screen'''

    global bullet_state
    bullet_state = "fire"
    screen.blit(bullet_img,(x+16,y+10))
    
def is_collision(enemyX,enemyY,bulletX,bulletY):
    '''detects collision of bullet and enemy'''

    distance = m.sqrt((m.pow(enemyX-bulletX,2)) + (m.pow(enemyY-bulletY,2)))
    if distance < 40:
        return True
    else:
        return False
    
def show_score(x,y):
    '''displays score value'''

    score = font.render("Score: " + str(score_value),True,(255,255,255))
    screen.blit(score,(x,y))
    
def game_over_text():
    '''displays game over text'''

    over_text = font.render("GAME OVER",True,(255,255,255))
    screen.blit(over_text,(300,200))
    
# game loop
while True:
    
    # check for events
    for event in pygame.event.get():

        # closes the program if window is closed
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
    
        # if keystroke is pressed check for left or right key
        if event.type == pygame.KEYDOWN:
                        
            # move ship to the right if a
            if event.key == pygame.K_a:
                playerX_change = - 5
                
            # move ship to the left if s
            if event.key == pygame.K_s:
                playerX_change = + 5
                
            # fire bullet if space
            if event.key == pygame.K_SPACE:
                if bullet_state == "ready":
                    bullet_sound = mixer.Sound('laser.wav')
                    bullet_sound.play()
                    bulletX = playerX
                    fire_bullet(bulletX,bulletY)
                    
        # stop ship from moving if a or s is released
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_a or pygame.K_s:
                playerX_change = 0
            
    # RGB red green blue 0-255
    screen.fill((0,0,0))
    
    # background image
    screen.blit(background,(0,0))
    
    # adds change in movement from button input to player location
    playerX += playerX_change
    

    # keep the player from moving off the screen
    if playerX <=0:
        playerX = 0
        
    elif playerX >= 736:
        playerX = 736
        
    # enemy movement
    for i in range(num_of_enemies):
        
        # Game Over
        if enemyY[i] > 500:
            for j in range(num_of_enemies):
                enemyY[j] = 2000
            game_over_text()
            break
        
        enemyX[i] += enemyX_change[i]
    
        if enemyX[i] <=0:
            enemyX_change[i] = 4
            enemyY[i] += enemyY_change[i]
        
        elif enemyX[i] >= 736:
            enemyX_change[i] = -4
            enemyY[i] += enemyY_change[1]
        
        # detect collision
        collision = is_collision(enemyX[i],enemyY[i],bulletX,bulletY)
        if collision:
            if bullet_state == "fire":
                collision_sound = mixer.Sound('explosion.wav')
                collision_sound.play()
                bulletY = 480
                bullet_state = "ready"
                score_value += 1
                enemyX[i] = r.randint(0,735)
                enemyY[i] = r.randint(50,150)
        
        # display enemy icon at given x and y
        enemy(enemyX[i],enemyY[i],i)
            
    # bullet movement
    if bulletY <= 0:
        bulletY = 480
        bullet_state = "ready"
    
    if bullet_state is "fire":
        fire_bullet(bulletX,bulletY)
        bulletY -= bulletY_change
    
    # display player icon at given x and y
    player(playerX,playerY)
    
    # display score
    show_score(textX,textY)
       
    # add to update game display
    pygame.display.update()
