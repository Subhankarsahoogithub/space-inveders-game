#import library:
import pygame
#to generate random numbers
import random 
#math libreary:
import math 
#to add music:
from pygame import mixer

#initialize our game:
pygame.init()

#create our screen:           (width,height)
screen=pygame.display.set_mode((800, 600))
#origine(0,0)-->top-left of screen

#Tittle and icon:
pygame.display.set_caption("SPACE-INVADERS")
icon=pygame.image.load('ufo.png')
pygame.display.set_icon(icon)

#Background:
background_image=pygame.image.load('Background3.jpg')

#Background Music-->
mixer.music.load('background.wav')
mixer.music.play(-1)

#Missile
missile_image=pygame.image.load('bullet.png')
missileX=0
missileY=480
missileX_change=0
missileY_change=0.91
missile_state="ready"

def fire(x,y):
    #to fire a missile:
    global missile_state
    missile_state="fired"

    #for multiple missiles-->when it's y-coordinate intersepts boundary ,new missile reloaded
    if y<=0:
       global missileY
       missile_state="ready"
       missileY=playerY


    screen.blit(missile_image,(x+16,y+10))    




#player:
player_image=pygame.image.load('player.png')
playerX=370
playerY=480

def player(x,y):  #to display our player
    #to make it not to go beyond our screen-boundry: 
    if x<0:
        x=0  
    if x>736:
        x=736
    if y<0:
        y=0 
    if y>536:
        y=536
    
    #built-in function for display on screen:
    screen.blit(player_image,(x,y))


#score of our player:
score_value=0
#for every collision-->score++

#player's score on screen:
font=pygame.font.Font('freesansbold.ttf',32)
#display on top left corner:
textX=10
textY=10

def show_score(x,y):
    score=font.render("Score : "+ str(score_value),True,(255,255,255))
    screen.blit(score,(x,y))


#Game-over text on screen after gameover-->
over=pygame.font.Font('freesansbold.ttf', 64)
def game_over_text():
    over_text=over.render("GAME-OVER! ",True,(255,255,255))
    screen.blit(over_text,(200,250))



#enemy:
enemyX=[]
enemyX_change=[]
enemyY=[]
enemyY_change=[]
x=[]
y=[]
num_of_enemies=8

i=0
for i in range(num_of_enemies):
     enemy_image=pygame.image.load('alien.png')
     enemyX.append(random.randint(0,800))
     enemyY.append(random.randint(50,150))
     enemyX_change.append(0.3)
     enemyY_change.append(10)
     y.append(enemyY[i])
     x.append(enemyX[i])




def enemy(x,y):
    #built-in function for dispaly on screen:
     screen.blit(enemy_image,(x,y))


#collision:   

#for collision detection between missile and enemy:
def is_collision(enemyX,enemyY,missileX,missileY):
      distance=math.sqrt((math.pow(enemyX-missileX,2))+(math.pow(enemyY-missileY,2)))
      if distance<77:
        return True
      else:
        return False



#event--> anything that's happening inside game window

running=True
while running:
    for event  in pygame.event.get():
        if event.type==pygame.QUIT:
            running=False

    # to catch any keyboard_events:
    if event.type==pygame.KEYDOWN:
        if event.key==pygame.K_LEFT:
            playerX-=0.5
        if event.key==pygame.K_RIGHT:
            playerX+=0.5
        if event.key==pygame.K_UP:
            playerY-=0.5
        if event.key==pygame.K_DOWN:
            playerY+=0.5  
        if event.key==pygame.K_LSHIFT:
            missileX=playerX
            #laser sound-->
            missile_sound=mixer.Sound('laser.wav')
            missile_sound.play()
            fire(missileX,missileY)
            #the X-coordinate of the missile remains constant till next fire

            
             

            

    
    #RGB-->red,green,blue
    screen.fill(((0,0,0)))  
    #Background-image
    screen.blit(background_image,(0,0))

    player(playerX,playerY)
    show_score(textX,textY)

    #missile movement:
    if missile_state == "fired":
        fire(missileX,missileY)
        #the Y-coordinate keeps on decressing
        missileY-=missileY_change
    else:
        missileY=playerY


    #for multiple enemies's movement and collision:    
    i=0
    for i in range(num_of_enemies):    
    #enemy movement:
        x[i]+=enemyX_change[i]
        #after collission it comes closer and started moving in opposite x-direction:
        if x[i]<18:
            enemyX_change[i]=0.4
            y[i]+=enemyY_change[i]
            enemyY[i]=y[i]
        elif x[i]>736:
             enemyX_change[i]=-0.4
             y[i]+=enemyY_change[i]
             enemyY[i]=y[i]


    #collision-->
    # True-->if collision has occered  else False:
        collision=is_collision(enemyX[i],enemyY[i],missileX,missileY)
        if collision:
            missileY=playerY
            missile_state="ready"
            score_value+=1
            print(score_value)
            
            #collision sound:
            collision_sound=mixer.Sound('explosion.wav')
            collision_sound.play()

            enemyX[i]=random.randint(4,785)
            enemyY[i]=random.randint(50,150)
            x[i]=enemyX[i]
            y[i]=enemyY[i]
    
        enemy(x[i],y[i])
    
    k=0
    for k in range(num_of_enemies):
        if enemyY[k]>440:
            #Game-over
            j=0
            for j in range(num_of_enemies):
                y[j]=2000
            game_over_text()
            break


    pygame.display.update()      