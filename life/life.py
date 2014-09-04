import time
import os

# simulation configuration
GENERATIONS = 1000
TIMEOUT = 0.1
WORLD_CONFIG = "world.txt"

# cell states
ALIVE = 'o'
DEAD = '.'
DIE = 'x'
BORN = '*'
EDGE = '+'


def compute_next_cycle(world):
    """
    Compute next cycle of life according to the rules below.

    1. Any live cell with fewer than two live neighbours dies, as if caused by
       under-population.
    2. Any live cell with two or three live neighbours lives on to the next
       generation.
    3. Any live cell with more than three live neighbours dies, as if by
       overcrowding.
    4. Any dead cell with exactly three live neighbours becomes a live cell,
       as if by reproduction.
    --------------------------------------------------------------------------
     input:
      - world (list of lists): matrix of the world

    [i,j]
    -----
    i: row index
    j: column index

    [1,3] => 1: row index, 3: column index
    -----
    [0,0] [0,1] [0,2] [0,3]
    [1,0] [1,1] [1,2] [0,3]
    [2,0] [2,1] [2,2] [3,3]
    [3,0] [3,1] [2,2] [3,3]

    """
    # i: row index (from 0)
    for i in range(len(world)):
        # j: column index (from 0)
        for j in range(len(world[0])):
            if on_the_edge(world, i, j) == True:
                # skip if we are on the edge of the world
                continue
            n = neighbors_alive(world, i, j)

            ### rule 1
            if n < 2 and world[i][j] == ALIVE:
                world[i][j] = DIE

            ### rule 2
            if n == 2 or n == 3 and world[i][j] == ALIVE:
                pass

            ### rule 3
            if n > 3 and world[i][j] == ALIVE:
                world[i][j] = DIE

            ### rule 4
            if n == 3 and world[i][j] == DEAD:
                world[i][j] = BORN
            
            


def neighbors_alive(world, i, j):
    cylon = 0 # number of neighbors alive(action stations!)
    if world[i-1][j-1] == ALIVE:
        cylon = cylon + 1
    if world[i][j-1] == ALIVE:
        cylon = cylon + 1
    if world[i+1][j-1] == ALIVE:
        cylon = cylon + 1
    if world[i+1][j] == ALIVE:
        cylon = cylon + 1
    if world[i+1][j+1] == ALIVE:
        cylon = cylon + 1
    if world[i][j+1] == ALIVE:
        cylon = cylon + 1
    if world[i-1][j+1] == ALIVE:
        cylon = cylon + 1
    if world[i-1][j] == ALIVE:
        cylon = cylon + 1
    return cylon
    

def run(generations, world_config):
    """
    Run simulation.
    ---------------
     input:
      - generations (integer): number of generations to let simulation running
      - world_config (filename): fie where initial world configurations is stored
    """
    world = get_world(world_config)
    
    for i in range(generations):
        print
        print "generation: %d" % i
        time.sleep(TIMEOUT)
        compute_next_cycle(world)
        print_world(world)


def on_the_edge(world, i, j):
    """
    Check if we are on the edge of the world.
    -----------------------------------------
     input:
      - world (list of lists): matrix of the world
      - i (integer): row index
      - j (integer): column index
     output:
      - True: if we are on the edge
      - False: otherwise
    """
    if i == 0 or i == len(world)-1 or j == 0 or j == len(world[0])-1:
        return True
    return False


def print_world(world):
    """
    Print world to the screen.
    --------------------------
     input:
      - world (list of lists): world matrix
    """
    for i in range(len(world)):
        for j in range(len(world[0])):
            if world[i][j] == ALIVE:
                print ALIVE,
            if world[i][j] == DEAD:
                print DEAD,
            if world[i][j] == DIE:
                print ALIVE,
                world[i][j] = DEAD
            if world[i][j] == BORN:
                print DEAD,
                world[i][j] = ALIVE
            if world[i][j] == EDGE:
                print EDGE,
        print


def get_world(world_config):
    """
    Load world from file and return it as matrix.
    ---------------------------------------------
     input:
      - world_config (filename): file where initial world configuration is stored
     output:
      - world (list of lists): matrix of the world
    """
    world = [] # empty world
    world_file = open(world_config, "r")

    for line in world_file:
        row = []
        for character in line:
            if character == '\n':
                # do not add new-line character
                continue
            row.append(character)
        world.append(row)
    return world


def clear():
    """
    Clear shell/terminal window. Should work on UNIX/Windows
    """
    os.system('cls' if os.name == 'nt' else 'clear')


# Action stations! Action stations! This is not a drill!
run(GENERATIONS, WORLD_CONFIG)
