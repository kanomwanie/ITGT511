#!/usr/bin/env python3
# Python 3.6

# Import the Halite SDK, which will let you interact with the game.
import hlt

# This library contains constant values.
from hlt import constants

# This library contains direction metadata to better interface with the game.
from hlt.positionals import Direction

# This library allows you to generate random numbers.
import random

# Logging allows you to save messages for yourself. This is required because the regular STDOUT
#   (print statements) are reserved for the engine-bot communication.
import logging

""" <<<Game Begin>>> """

# This game object contains the initial game state.
game = hlt.Game()
# At this point "game" variable is populated with initial map data.
# This is a good place to do computationally expensive start-up pre-processing.
# As soon as you call "ready" function below, the 2 second per turn timer will start.
game.ready("L.I.G.M.A. MKI")

# Now that your bot is initialized, save a message to yourself in the log file with some important information.
#   Here, you log here your id, which you can always fetch from the game object by using my_id.
logging.info("Successfully created bot! My Player ID is {}.".format(game.my_id))

def findenemy(ship,map):
    direcmap = ship.position.get_surrounding_cardinals()
    for i in direcmap:
        if map[i].is_occupied:
            map[i].mark_unsafe(ship)

def findsource(ship,map):
    direcmap = ship.position.get_surrounding_cardinals()
    minHa =map[direcmap[0]].halite_amount
    location =direcmap[0]
    for i in direcmap:
        if minHa< map[i].halite_amount:
            minHa = map[i].halite_amount
            location =i

    return location

def findoff(me,map,ship):
    #find closet drop off
    all = me.get_dropoffs()
    L = me.shipyard.position
    if len(all)!=0:
        for i in all:
            A = map.calculate_distance(ship.position,i.position)
            B = map.calculate_distance(ship.position,L)
            if B>A:
                L = i.position
    return L

def convert_to_direction(pos,next):
    if pos.x-next.x == 1 and pos.y-next.y ==0:
        return Direction.East
    elif pos.x-next.x == -1 and pos.y-next.y ==0:
        return Direction.West
    elif pos.x-next.x == 0 and pos.y-next.y ==1:
        return Direction.North
    elif pos.x-next.x == 0 and pos.y-next.y ==-1:
        return Direction.South

def moving(me,map,ship):
    #if ship nearby - avoid
    #aim fore nearest area with most stuff
    #when full- aim to drop off
    findenemy(ship,map)
    if ship.is_full or ship.halite_amount > 300:
        drop = findoff(me,map,ship)
        return map.naive_navigate(ship, drop)
    else:
        A = findsource(ship,map)
        return map.naive_navigate(ship, A)
    
def leasthalite(me):
    K = me.get_ships()
    T = True
    S=K[0]
    A =K[0].halite_amount
    for ship in me.get_ships():
        if ship.halite_amount ==0:
            ship.make_dropoff() 
            T=False
            break
        else:
            if A>ship.halite_amount:
                A=ship.halite_amount
                S= ship
    if T:
        S.make_dropoff() 
    

    

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
    if len(me.get_ships())>5 and me.halite_amount > constants.DROPOFF_COST+1000:
       leasthalite(me)

    for ship in me.get_ships():
        # For each of your ships, move randomly if the ship is on a low halite location or the ship is full.
        #   Else, collect halite.

        #CONVERTSHIP TO DROPOFF IF HAVE MORETHANT 5 AND HAVE MORE THAN 5K
        if game_map[ship.position].halite_amount < constants.MAX_HALITE / 10 or ship.is_full:
            command_queue.append(
                ship.move(
                    moving(me,game_map,ship)))
        else:
            command_queue.append(ship.stay_still())

    # If the game is in the first 200 turns and you have enough halite, spawn a ship.
    # Don't spawn a ship if you currently have a ship at port, though - the ships will collide.
    if len(me.get_ships())<=1 and me.halite_amount >= constants.SHIP_COST and not game_map[me.shipyard].is_occupied:
        command_queue.append(me.shipyard.spawn())

    # Send your moves back to the game environment, ending this turn.
    game.end_turn(command_queue)

