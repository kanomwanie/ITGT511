#!/usr/bin/env python3
# Python 3.6

# Import the Halite SDK, which will let you interact with the game.
import hlt

# This library contains constant values.
from hlt import constants

# This library contains direction metadata to better interface with the game.
from hlt.positionals import Direction
from hlt.positionals import Position as PP
# This library allows you to generate random numbers.
import random

# Logging allows you to save messages for yourself. This is required because the regular STDOUT
#   (print statements) are reserved for the engine-bot communication.
import logging
import heapq
from typing import Protocol, Iterator, Tuple, TypeVar, Optional
""" <<<Game Begin>>> """

# This game object contains the initial game state.
game = hlt.Game()
# At this point "game" variable is populated with initial map data.
# This is a good place to do computationally expensive start-up pre-processing.
# As soon as you call "ready" function below, the 2 second per turn timer will start.
game.ready("L.I.G.M.A. MKII")

# Now that your bot is initialized, save a message to yourself in the log file with some important information.
#   Here, you log here your id, which you can always fetch from the game object by using my_id.
logging.info("Successfully created bot! My Player ID is {}.".format(game.my_id))

T = TypeVar('T')
Location = TypeVar('Location')
GridLocation = Tuple[int, int]
class SquareGrid:
    def __init__(self, width: int, height: int):
        self.width = width
        self.height = height
        self.walls: list[GridLocation] = []
    
    def in_bounds(self, id: GridLocation) -> bool:
        (x, y) = id
        return 0 <= x < self.width and 0 <= y < self.height
    
    def passable(self, id: GridLocation) -> bool:
        return id not in self.walls
    
    def neighbors(self, id: GridLocation) -> Iterator[GridLocation]:
        (x, y) = id
        neighbors = [(x+1, y), (x-1, y), (x, y-1), (x, y+1)] # E W N S
        # see "Ugly paths" section for an explanation:
        if (x + y) % 2 == 0: neighbors.reverse() # S N W E
        results = filter(self.in_bounds, neighbors)
        results = filter(self.passable, results)
        return results

class GridWithWeights(SquareGrid):
    def __init__(self, width: int, height: int):
        super().__init__(width, height)
        self.weights: dict[GridLocation, float] = {}
    
    def cost(self, from_node: GridLocation, to_node: GridLocation,map) -> float:
        p = PP(to_node[0],to_node[1])
        return self.weights.get(to_node, getmovecost(p,map))

class PriorityQueue:
    def __init__(self):
        self.elements: list[tuple[float, T]] = []
    
    def empty(self) -> bool:
        return not self.elements
    
    def put(self, item: T, priority: float):
        heapq.heappush(self.elements, (priority, item))
    
    def get(self) -> T:
        return heapq.heappop(self.elements)[1]

def heuristic(a, b):
   # Manhattan distance on a square grid
   return abs(a[0] - b[0]) + abs(a[1] - b[1])

def starpath(start,goal,graph,map):
    frontier = PriorityQueue()
    frontier.put(start, 0)
    came_from = dict()
    cost_so_far = dict()
    came_from[start] = None
    cost_so_far[start] = 0

    while not frontier.empty():
        current = frontier.get()
        check = PP(current[0],current[1])
        if current != start:
            if not map[check].is_occupied:
                if current == goal:
                    return getpathlist(cost_so_far)
                for next in graph.neighbors(current):
                    new_cost = cost_so_far[current] + graph.cost(current, next,map)
                    if next not in cost_so_far or new_cost < cost_so_far[next]:
                        cost_so_far[next] = new_cost
                        priority = new_cost + heuristic(goal, next)
                        frontier.put(next, priority)
                        came_from[next] = current
        else:
                if current == goal:
                    return getpathlist(cost_so_far)
                for next in graph.neighbors(current):
                    new_cost = cost_so_far[current] + graph.cost(current, next,map)
                    if next not in cost_so_far or new_cost < cost_so_far[next]:
                        cost_so_far[next] = new_cost
                        priority = new_cost + heuristic(goal, next)
                        frontier.put(next, priority)
                        came_from[next] = current

def getpathlist(stuff):
    A = []
    cost = set(stuff.values())
    for i in cost:
        path = (0,0)
        for j in stuff.keys():
            if i == stuff[j]:
                path = j
        A.append(path)
    return A

def get8 (arr,ship):
    A = arr
    for i in range(len(arr)):
        if arr[i].x - ship.position.x ==-1  or arr[i].x- ship.position.x ==1:
            B= PP(arr[i].x,arr[i].x-1)
            C= PP(arr[i].x,arr[i].y+1)
            A.append(B)
            A.append(C)
    return A

def findenemy(ship,map):
    direcmap = ship.position.get_surrounding_cardinals()
    for i in direcmap:
        if map[i].is_occupied:
            map[i].mark_unsafe(ship)

def findsource(ship,map):
    direcmap = cantake(map,ship)
    minHa =map[direcmap[0]].halite_amount
    location =direcmap[0]
    for i in direcmap:
        if minHa< map[i].halite_amount:
            minHa = map[i].halite_amount
            location =i

    return location

def findoff(me,map,ship):
    #find closet drop off
    all = candrop(map,me)
    if len(all)!=0:
        L = all[0]
        for i in all:
            A = map.calculate_distance(ship.position,i)
            B = map.calculate_distance(ship.position,L)
            if B>A:
                L = i
    else:
        return [True,-1]
    return [False,L]

def convert_to_direction(pos,next,map,ship):
    if pos.x-next.x == 1 and pos.y-next.y ==0:
        return Direction.East
    elif pos.x-next.x == -1 and pos.y-next.y ==0:
        return Direction.West
    elif pos.x-next.x == 0 and pos.y-next.y ==1:
        return Direction.North
    elif pos.x-next.x == 0 and pos.y-next.y ==-1:
        return Direction.South
    return map.naive_navigate(ship, PP(next.x,next.y))
    
def getmovecost(position,map):
    if map[position].halite_amount == 0:
        return 0
    return int((100 /map[position].halite_amount)*10)

def candrop(map,me):
    A=[]
    all = me.get_dropoffs()
    if  not map[me.shipyard.position].is_occupied:
        A.append(me.shipyard.position)
    if len(all)!=0:
     for i in all:
        if not map[i.position].is_occupied:
            A.append(i.position)
    return A

def cantake(map,ship):
    A=[]
    direcmap = ship.position.get_surrounding_cardinals()
    for i in direcmap:
        if not map[i].is_occupied:
            A.append(i)
    return A


def moving(me,map,ship):
    #if ship nearby - avoid
    #aim fore nearest area with most stuff
    #when full- aim to drop off
    findenemy(ship,map)
    G = GridWithWeights(map.width,map.height)
    if ship.is_full or ship.halite_amount > 700:
        logging.info(ship.id)
        logging.info("get dropoff")
        logging.info(ship.halite_amount)
        drop = findoff(me,map,ship)
        if drop[0]:
            return ship.stay_still()
        else:
            A = starpath((ship.position.x,ship.position.y),(drop[1].x,drop[1].y),G,map)
            logging.info(A)
            TT = PP(A[1][0],A[1][1])
            return ship.move(convert_to_direction(ship.position,TT,map,ship))
    else:
        logging.info(ship.id)
        logging.info("get halite")
        logging.info(ship.halite_amount)
        A = findsource(ship,map)
        if map[ship.position].halite_amount>10:
            return ship.stay_still()
        return ship.move( map.naive_navigate(ship, A))
    
def leasthalite(me):
    K = me.get_ships()
    T = True
    S=K[0]
    A =K[0].halite_amount
    for ship in me.get_ships():
        if T:
            if ship.halite_amount ==0:
                ship.make_dropoff() 
                T=False
                return [False,ship]
            else:
                if A>ship.halite_amount:
                    A=ship.halite_amount
                    S= ship
    if T:
       command_queue.append( S.make_dropoff() )
       return [False,S]
    

    

""" <<<Game Loop>>> """

while True:
    # This loop handles each turn of the game. The game object changes every turn, and you refresh that state by
    #   running update_frame().
    game.update_frame()
    # You extract player metadata and the updated map metadata here for convenience.
    me = game.me
    game_map = game.game_map

    # A command queue holds all the commands you will run this turn. You build this list up and submit it at the
    #   end of the turn.
    command_queue = []
    trundrop = [True,0]

    if len(me.get_ships())>5 and me.halite_amount > constants.DROPOFF_COST+1000:
       trundrop = leasthalite(me)

    for ship in me.get_ships():
        # For each of your ships, move randomly if the ship is on a low halite location or the ship is full.
        #   Else, collect halite.

        #CONVERTSHIP TO DROPOFF IF HAVE MORETHANT 5 AND HAVE MORE THAN 5K
        if trundrop[0]:
                if game_map[ship.position].halite_amount < constants.MAX_HALITE / 10 or ship.is_full and ship.halite_amount > getmovecost(ship.position,game_map):
                     command_queue.append(moving(me,game_map,ship))
                else:
                    command_queue.append(ship.stay_still())
        else:
            if trundrop[1]!= ship:
                if game_map[ship.position].halite_amount < constants.MAX_HALITE / 10 or ship.is_full and ship.halite_amount > getmovecost(ship.position,game_map):
                    command_queue.append(
                      
                            moving(me,game_map,ship))
                else:
                    command_queue.append(ship.stay_still())

    #Spawan more when money is 7K and dropoff is less than 5
    if me.halite_amount >= 10000 and len(me.get_dropoffs())<3:
         command_queue.append(me.shipyard.spawn())

    # If the game is in the first 200 turns and you have enough halite, spawn a ship.
    # Don't spawn a ship if you currently have a ship at port, though - the ships will collide.
    if len(me.get_ships())<=2 and me.halite_amount >= constants.SHIP_COST and not game_map[me.shipyard].is_occupied:
        command_queue.append(me.shipyard.spawn())

    # Send your moves back to the game environment, ending this turn.
    game.end_turn(command_queue)

