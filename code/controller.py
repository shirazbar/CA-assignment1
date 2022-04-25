import sys
import easygui as gui
import pygame
import time
import matplotlib.pyplot as plt

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
# Get user input paramaters  - parameters gui                                  #
#------------------------------------------------------------------------------#
title = "Covid19 Cell Automat - Enter parameters" # window title
# message to be displayed
text = "Enter the following parameters, recommended parameters set as default:"

# list of parameters for user to input
input_parameters = ["Please enter number of creatures [N]", 
              "Please enter percentage of sick creatures [D]",
              "Please enter percentage of quick creatures [R]",
              "Please enter number of generations a creature is contagious [X]",
              "Please enter percentage of sick as a threshold [T]",
              "Please enter high probability for creature to get infected from a sick neighbor [P high]",
              "Please enter low probability for creature to get infected from a sick neighborr [P low]"]
default_parameters = ["12000", "0.001", "0.001", "4", "0.01", "0.7", "0.35"] # set default parameters

# output
output = gui.multenterbox(text, title, input_parameters, default_parameters)
N = int(output[0])
D = float(output[1])
R = float(output[2])
X = int(output[3])
T = float(output[4])
P_low = float(output[5])
P_high = float(output[6])

 
#------------------------------------------------------------------------------#
# Main Program Loop                                                            #
#------------------------------------------------------------------------------#
b = Board(N, D, R, T, P_high, P_low, X) # according to user's input
try:
    while b.S > 0 and b.gen < 500:
        for event in pygame.event.get():  # User did something
            if event.type == pygame.QUIT:  # If user clicked close
                sys.exit()
                pygame.quit()
                #sys.exit()
                
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
        ### print(b.get_prob_to_get_sick(), b.D, b.new_sick_only, b.amount_healthy)
except:
    sys.exit()
    pygame.quit() # close IDLE so program exits
    #sys.exit()

# create plot
plt.plot(b.sickness_list)
plt.xlabel('generation')
plt.ylabel('amount of sick')
plt.title("N=" + str(b.N) + " D=" + str(b.D) + " R=" + str(b.R) + " X=" + str(X) + " T=" + str(b.T) + " high P=" + str(b.high_prob) + " low P=" + str(b.low_prob))
plt.show()

