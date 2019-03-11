'''
This program is a version on conway's game of life using pygame 
'''

#import built in modules
import sys
import random

#import pygame
import pygame

#game of life rules
UNDERPOP = 2
OVERPOP = 3
REPRODUCE = 3

#map size in cells
MAP_WIDTH = 40
MAP_HEIGHT = 40

#cell size in pixels
CELL_WIDTH = 10
CELL_HEIGHT = 10

#colors and sufaces
WHITE = pygame.Color(255, 255, 255)
BLACK = pygame.Color(0, 0, 0)
ALIVE_SURFACE = pygame.Surface((CELL_WIDTH-1, CELL_HEIGHT-1))
ALIVE_SURFACE.fill(BLACK)
DEAD_SURFACE = pygame.Surface((CELL_WIDTH-1, CELL_HEIGHT-1))
DEAD_SURFACE.fill(WHITE) 

#screen size based on map size and cell size
SCREEN_WIDTH = MAP_WIDTH*CELL_WIDTH
SCREEN_HEIGHT = MAP_HEIGHT*CELL_HEIGHT

#   ____ _                         
#  / ___| | __ _ ___ ___  ___  ___ 
# | |   | |/ _` / __/ __|/ _ \/ __|
# | |___| | (_| \__ \__ \  __/\__ \
#  \____|_|\__,_|___/___/\___||___/
class Cell:
    ''' a class for a cell '''
    def __init__(self, x, y, alive):
        ''' takes an x, y and if the cell is alive'''
        self.x = x
        self.y = y
        self.alive = alive
        self.next_alive = alive
        #self.color = BLACK

    def draw(self):
        ''' chooses a surface depending on if the cell is alive or dead then blits the surface to the main display '''
        if self.alive:
            #ALIVE_SURFACE.fill(self.color)
            main_surface.blit(ALIVE_SURFACE, (self.x*CELL_WIDTH, self.y*CELL_HEIGHT))
        else:
            main_surface.blit(DEAD_SURFACE, (self.x*CELL_WIDTH, self.y*CELL_HEIGHT))
        

    def check_update(self):
        ''' goes through the eight neighboring cells and if the are alive then using the rules determines the fate of the cell and stores it for later '''
        neighbors = 0
        for x in range(-1, 2):
            for y in range(-1, 2):
                try:
                    if main_map[(self.x+ x + MAP_WIDTH) % MAP_WIDTH][(self.y + y + MAP_HEIGHT) % MAP_HEIGHT].alive and main_map[(self.x+ x + MAP_WIDTH) % MAP_WIDTH][(self.y + y + MAP_HEIGHT) % MAP_HEIGHT] is not self:
                        neighbors += 1
                except:
                    pass

        if self.alive:
            if neighbors < UNDERPOP or neighbors > OVERPOP:
                self.next_alive = False
            else:
                self.next_alive = True
        elif neighbors == REPRODUCE:
            self.next_alive = True

    def update(self):
        ''' updates the cell's status based on a previous check '''
        self.alive = self.next_alive



#  __  __             
# |  \/  | __ _ _ __  
# | |\/| |/ _` | '_ \ 
# | |  | | (_| | |_) |
# |_|  |_|\__,_| .__/ 
#              |_|    
def map_make():
    '''makes a map by randomly selecting cells to be alive or dead and returning a 2d array'''
    new_map = [[Cell(x, y, False) for y in range(MAP_HEIGHT)] for x in range(MAP_WIDTH)]
    for x in range(MAP_WIDTH):
        for y in range(MAP_HEIGHT):
            rand = random.randint(0, 1)
            if rand == 0:
                new_map[x][y].alive = False
            else:
                new_map[x][y].alive = True
    return new_map

def map_clear():
    ''' clears the map by setting all cells to be dead '''
    for x in range(MAP_WIDTH):
        for y in range(MAP_HEIGHT):
            main_map[x][y].alive = False
            main_map[x][y].next_alive = False

def map_check_update():
    ''' goes through all the cells and check neigboors '''
    for x in range(MAP_WIDTH):
        for y in range(MAP_HEIGHT):
            main_map[x][y].check_update()

def map_update():
    ''' goes through each cell and updates it status after checking it '''
    map_check_update()
    for x in range(MAP_WIDTH):
        for y in range(MAP_HEIGHT):
            main_map[x][y].update()

#  ____                     
# |  _ \ _ __ __ ___      __
# | | | | '__/ _` \ \ /\ / /
# | |_| | | | (_| |\ V  V / 
# |____/|_|  \__,_| \_/\_/  
def draw_cells():
    ''' goes through each cell and draws it '''
    for x in range(MAP_WIDTH):
        for y in range(MAP_HEIGHT):
            main_map[x][y].draw()

def draw_all():
    ''' reset thi display by filling it with black draw the cells and update the display '''
    main_surface.fill(BLACK)
    draw_cells()
    pygame.display.flip()


#   ____                      
#  / ___| __ _ _ __ ___   ___ 
# | |  _ / _` | '_ ` _ \ / _ \
# | |_| | (_| | | | | | |  __/
#  \____|\__,_|_| |_| |_|\___|
def game_init():
    ''' set up pygame, the map, and the display '''
    global main_map, main_surface, clock
    pygame.init()

    clock = pygame.time.Clock()

    main_map = map_make()

    pygame.display.set_caption('Game of Life')
    main_surface = pygame.display.set_mode((SCREEN_WIDTH,SCREEN_HEIGHT))

def game_handle_input():
    '''goes through each event and handles it'''
    event_list = pygame.event.get()

    for event in event_list:
        if event.type == pygame.QUIT:
            return 'quit'
        elif event.type == pygame.KEYDOWN:
            key = pygame.key.name(event.key)

            if key == 'space':
                return 'step'
            elif key == 'p':
                return 'loop'
            elif key == 'r':
                return 'reset'
            elif key == 'c':
                return 'clear'

        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse_x, mouse_y = event.pos
            button = event.button

            x = mouse_x//CELL_WIDTH
            y = mouse_y//CELL_HEIGHT

            if button == 1:
                main_map[x][y].alive = True
                main_map[x][y].check_update()
            elif button == 3:
                main_map[x][y].alive = False
                main_map[x][y].check_update()


def game_main():
    ''' sets up the game and starts a loop that handles input and updates cells and draws everything '''
    global main_map

    game_init()
    # draw_all()
    # pygame.image.save(main_surface, 'start.png')

    quit = False
    step = False
    loop = False

    while not quit:
        action = game_handle_input()

        if action == 'quit':
            quit = True
        elif action == 'reset':
            main_map = map_make()
            draw_all()
            step = False
            loop = False
        elif action == 'clear':
            map_clear()
        elif action == 'step':
            if step == False:
                step = True
            else:
                step = False
        elif action == 'loop':
            if loop == False:
                step = False
                loop = True
            else:
                loop = False 

        if step:
            loop = False
            map_update()
            step = False
        elif loop:
            map_update()

        draw_all()
        clock.tick()

    # pygame.image.save(main_surface, 'end.png')
    sys.exit()

if __name__ == '__main__':
    game_main()
