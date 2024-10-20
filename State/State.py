# Example file showing a basic pygame "game loop"
import pygame
import random

# Set up the screen dimensions and maximum speed for agents
WIDTH = 1280
HEIGHT = 720
MAX_SPEED = 5
NUMBER_AGENT = 100  # Number of agents in the simulation

# Factors controlling the behavior of the agents
COHERENCE_FACTOR = 0.01 # Controls how strongly agents are attracted to the center of mass
ALIGNMENT_FACTOR = 0.1  # Controls how strongly agents align their direction with others
SEPARATION_FACTOR = 0.05  # Controls how strongly agents avoid each other
SEPARATION_DIST = 30  # Minimum distance to maintain between agents
PRATROL_STATE =0 
IDEL_STATE = 1
CHASE_STATE =2
STATE=0
INVES_STATE = 3
ALERT_STATE=4
# -----------------------------------------------------------------------
# Agent class represents each moving entity in the simulation
# -----------------------------------------------------------------------


class Agent:
    def __init__(self, x, y,) -> None:
        # Initialize agent's position and velocity with random values
        self.position = pygame.Vector2(x, y)
        self.velocity = pygame.Vector2(
            random.uniform(-MAX_SPEED, MAX_SPEED), random.uniform(-MAX_SPEED, MAX_SPEED))
        self.acceleration = pygame.Vector2(0, 0)
        self.mass = 1  # Mass of the agent used in force calculation
        self.hunger = 100
        self.sight_range = 100
        self.current_state = IDEL_STATE
        self.spritecount =0
        self.sprite = [pygame.image.load('fish0.png'), pygame.image.load('fish1.png'), pygame.image.load('fish2.png'), pygame.image.load('fish3.png'),pygame.image.load('fish0.png')]


    def update(self):
        # Update velocity and position of the agent based on current acceleration
        self.velocity += self.acceleration
        if self.velocity.length() > MAX_SPEED:
            # Limit the speed to MAX_SPEED
            self.velocity = self.velocity.normalize() * MAX_SPEED
        self.position += self.velocity
        # Reset acceleration after each update
        self.acceleration = pygame.Vector2(0, 0)

    def apply_force(self, x, y):
        # Apply a force to the agent, adjusting acceleration based on mass
        force = pygame.Vector2(x, y)
        self.acceleration += force / self.mass
    

    def seek(self, x, y):
        # Calculate the direction towards a target point and apply a small force in that direction
        d = pygame.Vector2(x, y) - self.position
        d = d.normalize() * 0.1  # Adjust the force magnitude
        seeking_force = d
        self.apply_force(seeking_force.x, seeking_force.y)


    def coherence(self, agents):
        # Steer towards the average position (center of mass) of neighboring agents
        center_of_mass = pygame.Vector2(0, 0)
        agent_in_range_count = 0
        for agent in agents:
            if agent != self:
                dist = self.position.distance_to(agent.position)
                if dist < 100:  # Only consider nearby agents within 100 units
                    center_of_mass += agent.position
                    agent_in_range_count += 1

        if agent_in_range_count > 0:
            center_of_mass /= agent_in_range_count  # Calculate average position
            d = center_of_mass - self.position
            f = d * COHERENCE_FACTOR  
            self.apply_force(f.x, f.y)  # Apply coherence force

    def separation(self, agents):
        # Steer to avoid crowding neighbors (separation behavior)
        d = pygame.Vector2(0, 0)
        for agent in agents:
            if agent != self:
                dist = self.position.distance_to(agent.position)
                if dist < SEPARATION_DIST:  # Only consider agents within separation distance
                    d += self.position - agent.position

        separation_force = d * SEPARATION_FACTOR  
        # Apply separation force
        self.apply_force(separation_force.x, separation_force.y)

    def separation_rock(self, agent):
        # Steer to avoid crowding neighbors (separation behavior)
        d = pygame.Vector2(0, 0)
        for agent in agents:
            if agent != self:
                dist = self.position.distance_to(agent.position)
                if dist < 100:  # Only consider agents within separation distance
                    d += self.position - agent.position

        separation_force = d * SEPARATION_FACTOR  
        # Apply separation force
        self.apply_force(separation_force.x, separation_force.y)

    def alignment(self, agents):
        # Steer towards the average heading (velocity) of nearby agents (alignment behavior)
        v = pygame.Vector2(0, 0)
        agent_in_range_count = 0
        for agent in agents:
            if agent != self:
                dist = self.position.distance_to(agent.position)
                if dist < 100:  # Only consider nearby agents within 100 units
                    v += agent.velocity
                    agent_in_range_count += 1

        if agent_in_range_count > 0:
            v /= agent_in_range_count  # Calculate average velocity
            alignment_force = v * ALIGNMENT_FACTOR  # Apply alignment force
            self.apply_force(alignment_force.x, alignment_force.y)

    def draw(self, screen):
        # Draw the agent as a red circle on the screen
      #  pygame.draw.circle(screen, "red", self.position, 10)
        
        IMAGE_BIG = pygame.transform.rotozoom(self.sprite[self.spritecount//10], 0, 1.5)
        screen.blit(IMAGE_BIG, (self.position.x-32,self.position.y-32))
        if self.spritecount == 40:
            self.spritecount = 0
        else:
            self.spritecount = self.spritecount+1
        


# -----------------------------------------------------------------------
#  Begin 
# -----------------------------------------------------------------------
pygame.init()
# Create a window with the specified dimensions
screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()  # Initialize a clock to manage frame rate
BG = [pygame.image.load('bg1.png'), pygame.image.load('bg2.png'), pygame.image.load('bg3.png'), pygame.image.load('bg4.png'),pygame.image.load('bg1.png')]
# Set up font for displaying FPS (frames per second)
font = pygame.font.Font(None, 36)
# Create a list of agents at random positions within the screen
agents = [Agent(random.uniform(0, WIDTH), random.uniform(0, HEIGHT))
          for _ in range(NUMBER_AGENT)]

foods = []
bgcount =0
rocks = [Rock(200,200),Rock(1000,500)]
# ----- GAME LOOP ------------
running = True  # Variable to control the main loop
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:  # Check if the user closed the window
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN:
              pass

    # Fill the screen with gray color to clear the previous frame
    screen.blit(BG[bgcount//10], (0,0))


    # Calculate and display FPS (frames per second) in the top-right corner of the screen
    fps = int(clock.get_fps())
    fps_text = font.render(f"FPS: {fps}", True, pygame.Color('white'))
    screen.blit(fps_text, (WIDTH - fps_text.get_width() - 10, 10))

    pygame.display.flip()  # Update the screen with the drawn frame
    clock.tick(60)  # Limit the frame rate to 60 frames per second

pygame.quit()  # Clean up and close the game window when the loop ends