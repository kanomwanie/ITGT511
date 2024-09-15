import pygame
import random
import math
from pygame.locals import *
pygame.init()
WIDTH = 640
HEIGHT = 480
screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()
traget=[]
AG=[]
Max = 5
class Agent:
   def __init__(self,x,y):
    self.position = pygame.Vector2(x, y)
    self.velocity = pygame.Vector2(0, 0)
    self.acceleration = pygame.Vector2(0, 0)
    self.mass = 1
            #  self.sight_range = 100
    
   def update(self): 
        self.velocity = self.velocity + self.acceleration
        if self.velocity.length() >Max:
            self.velocity = self.velocity.normalize()*Max
        self.position = self.position +self.velocity
        self.acceleration = pygame.Vector2(0, 0)

   def render(self):
        pygame.draw.circle(screen,"black", self.position,20)

   def apply_force(self,x,y):
       force = pygame.Vector2(x,y)
       self.acceleration = self.acceleration + (force/self.mass)
   def seek(self,x,y):
       d =  pygame.Vector2(x, y) - self.position
       d.normalize()*0.1
       Seek_force =d
       self.apply_force(Seek_force.x, Seek_force.y)

   def coherence(self,agents):
       center_of_mass = pygame.Vector2(0,0)
        agent_in_range_count =0
       for agent in agents:
           if agent!=self:
               center_of_mass  += agent.position
               agent_in_range_count +=1

       center_of_mass /=len(agents)-1
       d = center_of_mass - self.position
       f = d.normalize() * 0.1
       self.apply_force(f.x,f.y)

   def seperetion(self, agents):
       d = pygame.Vector2(0,0)
      
       for agent in agents:
           dist = math.sqrt((self.position.x-agent.position.x)**2 + (self.position.y - agent.position.y)**2)
           if dist<30:
               d = self.position - agent.position
               
       seperation_force = d*0.1
       self.apply_force(seperation_force.x,seperation_force.y)

   def alignment(self,agents):
       v = pygame.Vector2(0,0)
       for agent in agents:
           if agent != self:
               v +=agent.velocity
       v/= len(agents) -1
       alignment_f = v*0.1
       self.apply_force(alignment_f.x,alignment_f.y)



  # def arriveToTragetInRange(self, ver_traget):
       # d = self.position - ver_traget
       # dist = d.magnitude()
        #if (dist <= self.sight_range):
           # max_speed = 0.1
           # energy = 1.0-dist / self.sight_range
           # speed = energy * max_speed
           # d.normalize()
           # d = d * speed
           # self.acceleration = self.acceleration + d
       # else :
           # drag = self.velocity*-0.1
           # self.acceleration = self.acceleration + drag

 
    
  
  



def main():
   global traget
   running = True
   traget = pygame.Vector2(100, 200)
   AGEN = []
   for i in range(5):
           AGEN.append(Agent(random.uniform(0,WIDTH),random.uniform(0,HEIGHT)))
   AGEN[2].apply_force(-5,-5)
   while running:
        # poll for events
        # pygame.QUIT event means the user clicked X to close your window
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
             tAA = pygame.mouse.get_pos()
             traget = pygame.Vector2(tAA[0], tAA[1])

        # fill the screen with a color to wipe away anything from last frame
        screen.fill("grey")

        # RENDER YOUR GAME HERE
        pygame.draw.circle(screen,"red", traget,10)

        for i in AGEN:
            #i.arriveToTragetInRange(traget)
            i.update()
            i.render()
            i.seperetion(AGEN)
            i.coherence(AGEN)
            i.alignment(AGEN)
            i.seek(traget.x,traget.y)


        # flip() the display to put your work on screen
        pygame.display.flip()

        clock.tick(60)  # limits FPS to 60

# Execute game:
main()
