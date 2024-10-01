import random
import pygame
from utility import MarbleBag as bag
from utility import Predeteermination as pre
from utility import progressive as pro
from utility import fixedReateProb as fix

seed = 500
WIDTH = 1280
HEIGHT = 720

def setseed(seed):
    random.seed(seed)

def mineral_roll():
    chance = random.randint(1, 20)
    if chance== 20:
        return 3
    else:
        chance = random.randint(1, 10)
        if chance <=3:
            return 2
        else:
            return 1

# -----------------------------------------------------------------------
#  Begin 
# -----------------------------------------------------------------------
pygame.init()
# Create a window with the specified dimensions
screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()  # Initialize a clock to manage frame rate
# Set up font for displaying FPS (frames per second)
font = pygame.font.Font(None, 36)
# Create a list of agents at random positions within the screen
friend = [pygame.image.load('F1.png'), pygame.image.load('F2.png')]
butt = [pygame.image.load('1.png'), pygame.image.load('2.png'), pygame.image.load('3.png'), pygame.image.load('4.png')]
dirt = pygame.image.load('dirt.png')
dirts = pygame.transform.rotozoom(dirt, 0, 0.2)
dia= pygame.image.load('diamond.png')
diamond= pygame.transform.rotozoom(dia, 0, 0.2)
ir= pygame.image.load('iron.png')
gol= pygame.image.load('gold.png')
iron= pygame.transform.rotozoom(ir, 0, 0.2)
gold=pygame.transform.rotozoom(gol, 0, 0.2)
R = "Click on big dirt to mine."
click = False
jail = False

D = pygame.Vector2(380,120)
Invent = [0,0,0,0]# 0=dirt. 1 irom 2 gold 3 diamond
#chance diamond 10  gold  30  iron 70
No = ["No", "Nope", "Nuh uh", "Mine Harder!"]
broke = fix(30,3)
broke.setseed(seed)
# ----- GAME LOOP ------------
running = True  # Variable to control the main loop
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:  # Check if the user closed the window
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            traget = pygame.mouse.get_pos()
            p = pygame.Vector2(traget[0],traget[1])
            if not jail:
                if (p.x>=30 and p.x<= 230)and (p.y>=450 and p.y<=520 ):
                    if Invent[3]>= 1000:
                        Invent[3]-=1000
                        jail = True
            if (p.x>=950 and p.x<= 1250)and (p.y>=100 and p.y<=200 ):
                if Invent[0]>=10:
                    Invent[0]-=10
                    Invent[1]+=1
            if (p.x>=950 and p.x<= 1250)and (p.y>=250 and p.y<=350 ):
                if Invent[1]>=10:
                    Invent[1]-=10
                    Invent[2]+=1
            if (p.x>=950 and p.x<= 1250)and (p.y>=400 and p.y<=500 ):
                if Invent[2]>=10:
                    Invent[2]-=10
                    Invent[3]+=1
            if (p.x>=D.x and p.x<= 840)and (p.y>=D.y and p.y<=520 ):
                chance = random.randint(0, 1)
                if chance == 1:
                     
                     if broke.attempt():
                         W = mineral_roll()
                         if W == 1:
                             R= "You got Iron!!!"
                             Invent[1] +=1
                         if W == 2 :
                             R= "You got Gold!!!"
                             Invent[2] +=1
                         if W == 3 :
                             R= "You got Diamond!!!"
                             Invent[3] +=1
                         
                     else:
                         R= "You got Dirt!"
                         Invent[0] +=1
                         
                else:
                    u = random.randint(0, 3)
                    R = No[u]
               



    # Fill the screen with gray color to clear the previous frame
    screen.fill("grey")
    screen.blit(dirt, (380,120))
    screen.blit(dirts, (100,600))
    screen.blit(iron, (400,600))
    screen.blit(gold, (700,600))
    screen.blit(diamond, (1000,600))
    screen.blit(butt[0], (950,100))
    screen.blit(butt[1], (950,250))
    screen.blit(butt[2], (950,400))
    if jail:
        screen.blit(friend[1], (30,30))
    else:
        screen.blit(friend[0], (30,30))
        screen.blit(butt[3], (30,450))
    # Calculate and display FPS (frames per second) in the top-right corner of the screen
    fps = int(clock.get_fps())
    fps_text = font.render(f"FPS: {fps}", True, pygame.Color('white'))
    screen.blit(fps_text, (WIDTH - fps_text.get_width() - 10, 10))
    result = font.render(f"{R}", True, pygame.Color('black'))
    screen.blit(result, (WIDTH - result.get_width() - 600, 50))
    d = font.render(f"{Invent[0]}", True, pygame.Color('black'))
    screen.blit( d, (200, 620))
    i = font.render(f"{Invent[1]}", True, pygame.Color('black'))
    screen.blit( i, (500, 620))
    g = font.render(f"{Invent[2]}", True, pygame.Color('black'))
    screen.blit( g, (800, 620))
    di = font.render(f"{Invent[3]}", True, pygame.Color('black'))
    screen.blit( di, (1100, 620))

    pygame.display.flip()  # Update the screen with the drawn frame
    clock.tick(60)  # Limit the frame rate to 60 frames per second

pygame.quit()  # Clean up and close the game window when the loop ends