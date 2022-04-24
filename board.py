import numpy as np
import random
from creature import Creature
from utils import raffle, EMPTY, HEALTHY, CONTAGIOUS, NOT_CONTAGIOUS, MATRIX_SIZE

#------------------------------------------------------------------------------#
# Board class represents the Covid19 Cell Automat's board                      #
#------------------------------------------------------------------------------#
class Board:
    def __init__(self, N=12000, D=0.001, R=0.001, T=0.01, P_high=0.4, P_low=0.35):
        self.N = N
        self.D = D
        self.R = R
        self.T = T
        self.low_prob = P_low ### SMALL
        self.high_prob = P_high ### BIG
        
        self.creatures = {} # dictionary id:creature obj
        self.matrix = np.zeros((MATRIX_SIZE, MATRIX_SIZE)) # for GUI representation 
        self.S = 0
        self.gen = 0
        self.amount_healthy = self.N
        self.sickness_list = [] #num of sick in each generation, for plotting
        
        # initialize N creatures on random points on the board
        points = random.sample([(x, y) for x in range(MATRIX_SIZE) for y in range(MATRIX_SIZE)], self.N)
        for id in range(1, self.N + 1):
            location = points[id-1]
            sickness = False
            is_fast = raffle(self.R) # quickly moving creatures
            # decide which of the N creatures are sick or helthy with initial_sickness propabilty
            if raffle(self.D):
                sickness = True
                self.matrix[location] = CONTAGIOUS
                self.S += 1
            else:
                self.matrix[location] = HEALTHY
            creature = Creature(id, location, sickness, is_fast) # initilize 
            if sickness:
                creature.sick_gen_counter += 1
            self.creatures[id] = creature
        self.sickness_list.append(self.S)
        self.amount_healthy -= self.S
        
       
        
    # get the right probility to catch the virus according to the amount of active sick creatures
    def get_prob_to_get_sick(self):
        F = self.S / self.N # fraction of sick creatures in the population
        
        if F >= self.T: # high amount of sick creatures >> more carful >> it is less likely to be infected, however there are more sick creatures to get infected from
            ratio = self.T/F # indication of how much T is smaller than F, higher F --> smaller ratio
            return (1-F) * ratio * self.low_prob # use 1-F to get larger probability when F is smaller
        else: # low amount of sick >> less carful >> higher probability to get sick
            return (1-F) * self.high_prob # use 1-F to get larger probability when F is smaller

        
    # keep a matrix of all creature objects according to their location and sickness status
    def update_matrix_and_creatures(self):
        self.matrix = np.zeros((MATRIX_SIZE, MATRIX_SIZE))
        for creature in self.creatures.values(): # each creature object
            new_loc = creature.next_location
            creature.update_location() # keep new location instead previous 
            # sick
            if creature.sickness:
                creature.sick_gen_counter += 1
                if creature.is_contagious():
                    self.matrix[new_loc] = CONTAGIOUS
                else:
                    self.matrix[new_loc] = NOT_CONTAGIOUS
            # healthy
            else:
                self.matrix[new_loc] = HEALTHY
         
    def try_to_move_creature(self, creature, temp_locations):
        while True:
            try:
                new_temp_location = creature.move_on_board(set() ,temp_locations, self.creatures)
                return new_temp_location
            except:
                pass
                
    
    # creates a new generation - generates a new sickness status 
    # and movment to a distinct location for all creatures
    def step(self):
        self.new_sick_only = 0
        new_S = 0
        temp_locations = {} # new dictionary
        prob = self.get_prob_to_get_sick()
        # init new matrix 
        for x in range(MATRIX_SIZE):
            for y in range(MATRIX_SIZE):
                temp_locations[(x,y)] = EMPTY
        # refill matrix according to each creature's current sickness status and new location
        for creature in self.creatures.values():
            ### current sickness status - check if contagious 
            if not creature.sickness:
                is_infected = creature.get_infected(prob, self.matrix)
                if (is_infected):
                    new_S += 1
                    self.new_sick_only += 1
                    self.amount_healthy -= 1
            elif creature.is_contagious():
                new_S += 1
                
            ### generate movment to a new distinct location
            temp_locations = self.try_to_move_creature(creature, temp_locations)
            
        self.update_matrix_and_creatures() # updates the matrix and the creatures' locations
        self.gen += 1 # increasing generation
        self.S = new_S # new value of sick creatures
        self.sickness_list.append(self.S) # adding this value to the sickness list over all generations
        
# ############################  DELETE AFER CHECKING ALL GRAPHS
# b = Board()    
# while b.S > 0 and b.gen < 700:
#     #print(b.amount_healthy)
#     old_s = b.S
#     b.step()
#     print(b.get_prob_to_get_sick(), b.S, b.new_sick_only, b.amount_healthy)


# # create plot
# import matplotlib.pyplot as plt
# from creature import X

# plt.plot(b.sickness_list)
# plt.xlabel('generation')
# plt.ylabel('amount of sick')
# plt.title("N=" + str(b.N) + " D=" + str(b.D) + " R=" + str(b.R) + " X=" + str(X) + " T=" + str(b.T) + " high P=" + str(b.high_prob) + " low P=" + str(b.low_prob))
# plt.show()





