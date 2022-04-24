import subprocess
import pkg_resources
required = {'numpy', 'matplotlib', 'pygame'}
installed = {pkg.key for pkg in pkg_resources.working_set}
missing = required - installed
if missing:
    subprocess.check_call(['pip3', 'install', *missing], stdout=subprocess.DEVNULL)

import pygame
import time
import matplotlib.pyplot as plt
from creature import X
from board import Board
from utils import HEALTHY, CONTAGIOUS, NOT_CONTAGIOUS, MATRIX_SIZE

# define colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREY = (200, 200, 200)
RED = (255, 0, 0)
PURPLE = (127, 0, 255)
 
# set WIDTH and HEIGHT of each grid location
WIDTH = 3 # set WIDTH of each grid location
HEIGHT = 3 # set HEIGHT of each grid location
MARGIN = 1 # set margin between each cell
 
# Initialize pygame
pygame.init()
WINDOW_SIZE = [801, 801] # Set HEIGHT and WIDTH of the screen
screen = pygame.display.set_mode(WINDOW_SIZE)
pygame.display.set_caption('Covid19 Cell Automat') # set title of screen
 
#------------------------------------------------------------------------------#
# Main Program Loop                                                            #
#------------------------------------------------------------------------------#
b = Board()
steps = 50
try:
    while b.D > 0 and b.gen < 500:
        for event in pygame.event.get():  # User did something
            if event.type == pygame.QUIT:  # If user clicked close
                pygame.quit()
        pygame.display.set_caption('Covid19 Cell Automat, Generation: ' + str(b.gen))
        grid = b.matrix
        screen.fill(GREY) # set the screen background
        # draw the grid
        for row in range(MATRIX_SIZE):
            for column in range(MATRIX_SIZE):
                color = WHITE
                if grid[row][column] == HEALTHY:
                    color = BLACK
                if grid[row][column] == CONTAGIOUS:
                    color = RED
                if grid[row][column] == NOT_CONTAGIOUS:
                    color = PURPLE
                pygame.draw.rect(screen, color,
                                 [(MARGIN + WIDTH) * column + MARGIN,
                                  (MARGIN + HEIGHT) * row + MARGIN, WIDTH, HEIGHT])
        # update screen with what we've drawn.
        pygame.display.flip()
        time.sleep(0.05)
        b.step()
        print(b.get_prob_to_get_sick(), b.D, b.new_sick_only, b.amount_healthy)
except:
    pygame.quit() # close IDLE so program exits

# create plot
plt.plot(b.sickness_list)
plt.xlabel('generation')
plt.ylabel('amount of sick')
plt.title("N=" + str(b.N) + " D=" + str(b.D) + " R=" + str(b.R) + " X=" + str(X) + " T=" + str(b.T) + " high P=" + str(b.high_prob) + " low P=" + str(b.low_prob))
plt.show()

