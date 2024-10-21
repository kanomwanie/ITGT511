import pygame
import random
import pygame_gui
import math
from enum import Enum
from abc import ABC, abstractmethod

WIDTH, HEIGHT = 800, 600
NUM_AGENTS = 1
FISH_SIZE = 5
FOOD_SIZE = 3
MAX_SPEED = 2
NUM_BONE = 5
SOUND_AREA = 70


pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
manager = pygame_gui.UIManager((WIDTH, HEIGHT))
food_rate_slider = pygame_gui.elements.UIHorizontalSlider(
    relative_rect=pygame.Rect((10, 10), (200, 20)),
    start_value=500,
    value_range=(100, 2000),
    manager=manager
)
pygame.display.set_caption("State Machine")

# Load Orc Sprite Sheet

# Animation frame rate
FRAME_RATE = 0.4

# States------------
class AgentState(Enum):
    PATROL_STATE = 0
    CHASE_STATE = 1
    IDLE_STATE = 2
    INVEST_STATE= 3
#---------------------
class StateMachine():
    def __init__(self) -> None:
        self.states = {
            'patrol': PatrolState(),
            'chase': ChaseState(),
            'idle': IdleState(),
            'Invest': InvestState()
        }
        self.curret_state = 'idle'

    def update(self, agent, target,bone):
        new_state = self.states[self.curret_state].update(agent, target,bone)
        if new_state:
            self.transition_to(agent, new_state)

    def transition_to(self, agent, new_state):
        self.states[self.curret_state].exit(agent)
        self.curret_state = new_state
        self.states[self.curret_state].enter(agent)



class State(ABC):
    @abstractmethod
    def enter(self, agent):
        pass

    @abstractmethod
    def update(self, agent, target,bone):
        pass
    
    @abstractmethod
    def exit(self, agent):
        pass

class PatrolState(State):
    def enter(self, agent):
        print("patrol")

    def update(self, agent, target,bone):
        agent.velocity.x = random.randint(0, 600)
        agent.velocity.y = random.randint(0, 600)
        if agent.velocity.length() > MAX_SPEED:
            agent.velocity.scale_to_length(MAX_SPEED)
        agent.position += agent.velocity

        # transition that could change to other stages
        dist=(target[0].position - agent.position).length()
        for i in target:
             d = (i.position - agent.position).length()
             if abs(d) < dist:
                dist = d
        if dist < 50:
            return 'chase'
        elif agent.timer ==0:
            agent.reset()
            return 'idle'
        else:
            chase = False
            A=0
            dist=(bone[0].position - agent.position).length()
            for i in range(len(bone)):
                if bone[i].status:
                    d = (bone[i].position - agent.position).length()
                    if abs(d) <= dist and d<=SOUND_AREA:
                        dist = d
                        chase = True
                        A=bone[i]

            if dist <= SOUND_AREA and chase:
                agent.hear(A)
                return 'Invest'
      

    def exit(self, agent):
        pass

class InvestState(State):
    def enter(self, agent):
        print("invest")

    def update(self, agent, target,bone):
       A = agent.alertt
       a = (A.position - agent.position).normalize() * 5
       agent.velocity += a
       if agent.velocity.length() > MAX_SPEED:
            agent.velocity.scale_to_length(MAX_SPEED)
       agent.position += agent.velocity

        # transition that could change to other stages
       di=(target[0].position - agent.position).length()
       for i in target:
             d = (i.position - agent.position).length()
             if abs(d) < di:
                di = d
       if di < 50:
            return 'chase'
       else:
        dist = (A.position - agent.position).length()
        if dist < 1:
                agent.reset()
                return 'idle'


    def exit(self, agent):
        pass

class ChaseState(State):
    def enter(self, agent):
        print("chase")

    def update(self, agent, target,bone):
        W=0
        dist=(target[0].position - agent.position).length()
        for i in range(len(target)) :
             d = (target[i].position - agent.position).length()
             if abs(d) < dist:
                W =i
                
        a = (target[W].position - agent.position).normalize() * 5
        agent.velocity += a
        if agent.velocity.length() > MAX_SPEED:
            agent.velocity.scale_to_length(MAX_SPEED)
        agent.position += agent.velocity

        # transition that could change to other stages
        dist=(target[0].position - agent.position).length()
        for i in range(len(target)) :
             d = (target[i].position - agent.position).length()
             if abs(d) < dist:
                dist = d
                W =i
        if dist >= 100:
            agent.reset()
            return 'patrol'
        if dist <= 32:
            target[i].ded()
            agent.reset()
            return 'idle'

    def exit(self, agent):
        pass


class IdleState(State):
    def enter(self, agent):
       
       print("idle")

    def update(self, agent, target,bone):
        if agent.timer == 0:
            agent.reset()
            return 'patrol'
        else:

            dist=(target[0].position - agent.position).length()
            for i in target:
                d = (i.position - agent.position).length()
                if abs(d) < dist:
                    dist = d
            if dist < 50:
                return 'chase'
            chase = False
            A=0
            dist=(bone[0].position - agent.position).length()
            for i in range(len(bone)):
                if bone[i].status:
                    d = (bone[i].position - agent.position).length()
                    if abs(d) <= dist and d<=SOUND_AREA:
                        dist = d
                        chase = True
                        A=bone[i]

            if dist <= SOUND_AREA and chase:
                agent.hear(A)
                return 'Invest'
    def exit(self, agent):
        pass

class Robber:
    def __init__(self,x,y):
        self.position = pygame.Vector2(x, y)
        self.sprite = pygame.image.load('gnome.png')
        self.status = True
        self.velocity = pygame.Vector2(random.uniform(-1, 1), random.uniform(-1, 1)).normalize() * MAX_SPEED

    def ded(self):
        self.status = False

    def update(self):
        self.velocity.x = random.randint(0, 600)
        self.velocity.y = random.randint(0, 600)
        if self.velocity.length() > MAX_SPEED:
            self.velocity.scale_to_length(MAX_SPEED)
        self.position += self.velocity

        if self.position.x > WIDTH:
            self.position.x = 0
        elif self.position.x < 0:
            self.position.x = WIDTH
        if self.position.y > HEIGHT:
            self.position.y = 0
        elif self.position.y < 0:
            self.position.y = HEIGHT


    def draw(self, screen):
        screen.blit(self.sprite, (self.position.x-32,self.position.y-32))


class Bone:
    def __init__(self,x,y):
        self.position = pygame.Vector2(x, y)
        self.sprite = pygame.image.load('bone.png')
        self.status = False
        self.red = SOUND_AREA
        self.anim = 1
    
    def alert(self):
        self.status=True

    def draw(self, screen):
        if self.status:
           pygame.draw.circle(screen, (255, 0, 0), (int(self.position.x-16), int(self.position.y-16)), self.anim)
           self.anim +=1
           if self.anim>self.red:
               self.anim=1
               self.status=False
        screen.blit(self.sprite, (self.position.x-32,self.position.y-32))


class Agent:
    def __init__(self):
        self.position = pygame.Vector2(random.uniform(0, WIDTH), random.uniform(0, HEIGHT))
        self.velocity = pygame.Vector2(random.uniform(-1, 1), random.uniform(-1, 1)).normalize() * MAX_SPEED
        self.frame_index = 0
        self.state_machine = StateMachine()
        self.alertt=0
        self.timer = 50
        self.sprite = pygame.image.load('Guard.png')

    def update(self, target,B):
        self.state_machine.update(self, target,B)
        self.timer -=1 
        # Warp around
        if self.position.x > WIDTH:
            self.position.x = 0
        elif self.position.x < 0:
            self.position.x = WIDTH
        if self.position.y > HEIGHT:
            self.position.y = 0
        elif self.position.y < 0:
            self.position.y = HEIGHT

        return True
    def reset(self):
        self.timer = 50

    def hear(self,target):
        self.alertt = target

    def draw(self, screen):
        # Update frame index for animation
        current_frame =self.sprite
        if self.velocity.x < 0:
            current_frame = pygame.transform.flip(self.sprite, True, False)

        if self.state_machine.curret_state == 'patrol':
            screen.blit(current_frame, (self.position.x-32,self.position.y-32))
        elif self.state_machine.curret_state == 'chase':
           screen.blit(current_frame, (self.position.x-32,self.position.y-32))
        elif self.state_machine.curret_state == 'idle':
           screen.blit(current_frame, (self.position.x-32,self.position.y-32))
        elif self.state_machine.curret_state == 'Invest':
           screen.blit(current_frame, (self.position.x-32,self.position.y-32))
        


# ------------------------------------------------------------------------------------------------


def main():
    agents = [Agent() for _ in range(NUM_AGENTS)]
    Gnome = []
    Bones = [Bone(random.uniform(10, WIDTH), random.uniform(10, HEIGHT))
          for _ in range(NUM_BONE)]
    clock = pygame.time.Clock()

    running = True
    while running:
        time_delta = clock.tick(60) / 1000.0
        screen.fill((100, 100, 100))
        manager.update(time_delta)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            manager.process_events(event)
            if event.type == pygame.MOUSEBUTTONDOWN:
                traget = pygame.mouse.get_pos()
                GN = Robber(traget[0],traget[1])
                Gnome.append(GN)

        screen.fill("darkslateblue")
        #agents = [fish for fish in agents if fish.update(target)]
        for B in Bones:
            if not B.status:
                for G in Gnome:
                    dist = (B.position - G.position).length()
                    if dist<=30:
                        B.alert()
            B.draw(screen)
        for GN in Gnome:
            if not GN.status:
                Gnome.remove(GN)
            else:
              GN.update()
              GN.draw(screen)
        for agent in agents:
            if len(Gnome)!=0:
             agent.update(Gnome,Bones)
            agent.draw(screen)



        manager.draw_ui(screen)
        pygame.display.flip()
        clock.tick(60)

    pygame.quit()

if __name__ == "__main__":
    main()
