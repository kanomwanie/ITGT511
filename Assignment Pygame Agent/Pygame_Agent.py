import pygame
from pygame.locals import *
pygame.init()
screen = pygame.display.set_mode((640, 480))
clock = pygame.time.Clock()
traget=[]
AG=[];

class Agent:
   def __init__(self,x,y):
    self.position = pygame.Vector2(x, y)
    self.velocity = pygame.Vector2(0, 0)
    self.acceleration = pygame.Vector2(0, 0)
    self.sight_range = 100

   def arriveToTragetInRange(self, ver_traget):
        d = self.position - ver_traget
        dist = d.magnitude()
        if (dist <= self.sight_range):
            max_speed = 0.1
            energy = 1.0-dist / self.sight_range
            speed = energy * max_speed
            d.normalize()
            d = d * speed
            self.acceleration = self.acceleration + d
        else :
            drag = self.velocity*-0.1
            self.acceleration = self.acceleration + drag

   def update(self): 
        self.velocity = self.velocity +  self.acceleration
        if self.velocity.x >1:
            self.velocity.x = 1
        if self.velocity.y >1:
            self.velocity.y = 1
        #self.velocity.limit(1)
        self.position = self.position -self.velocity
        self.acceleration = (0, 0)

   def render(self):
        pygame.draw.circle(screen,"black", self.position,20)
    
  
  



def main():
   global traget
   running = True
   traget = [100,200]
   AGEN = []
   AGEN.append(Agent(100,100))
   AGEN.append(Agent(200,100))
   AGEN.append(Agent(200,200))
   AGEN.append(Agent(50,100))
   AGEN.append(Agent(100,50))
   while running:
        # poll for events
        # pygame.QUIT event means the user clicked X to close your window
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
             traget = pygame.mouse.get_pos()

        # fill the screen with a color to wipe away anything from last frame
        screen.fill("grey")

        # RENDER YOUR GAME HERE
        pygame.draw.circle(screen,"red", traget,10)

        for i in AGEN:
            i.arriveToTragetInRange(traget)
            i.update()
            i.render()


        # flip() the display to put your work on screen
        pygame.display.flip()

        clock.tick(60)  # limits FPS to 60

# Execute game:
main()
