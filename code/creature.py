import random
from utils import raffle, CONTAGIOUS, MATRIX_SIZE

#X = 4

#------------------------------------------------------------------------------#
# Creature class represents a creature in the Covid19 Cell Automat             #
#------------------------------------------------------------------------------#
class Creature:
    def __init__(self, id, location, sickness, is_fast, X):
        self.id = id # distinct
        self.location = location
        self.next_location = None
        self.sickness = sickness # bool
        self.sick_gen_counter = 0
        self.is_fast = is_fast # bool
        self.X = X

        
    # checks whether a creature currently contagious 
    def is_contagious(self):
        return self.sick_gen_counter <= self.X
    
    
    # checks where can a creature move to 
    def get_options_to_move(self):
        if self.is_fast: # R creature
            possible_range = list(range(-10,11)) # can move up to 10 spots at once in all direction
        else: # regular speed creature
            possible_range = [-1, 0, 1] # can move 1 spot in all direction
        # get all options creature can move to from current location
        x,y = self.location
        options = [] 
        for i in possible_range:
            for j in possible_range:     
                options.append(((x+i)%(MATRIX_SIZE), (y+j)%(MATRIX_SIZE))) #keeps wrap around model
        return options
    
    
    # check whether creature can get infected by his current neighbors
    def get_infected(self, prob_to_get_sick, matrix):        
        (x,y) = self.location
        # wrap arround model
        up = (y + 1) % MATRIX_SIZE
        down = (y - 1) % MATRIX_SIZE
        left = (x - 1) % MATRIX_SIZE
        right = (x + 1) % MATRIX_SIZE
        # go throgh all creatures neighbors
        neighbors = [(left,down), (x,down), (right,down), (right,y), (right,up), (x,up), (left,up), (left,y)]
        for neighbor_loc in neighbors: 
            if matrix[neighbor_loc] == CONTAGIOUS: 
                # there a neighbor who can inffect current creture in a certain probabiltiy
                self.sickness = raffle(prob_to_get_sick)
                if self.sickness: # got sick

                    return True
                    
        return False # not sick
  
    #################################################################################
    # Generate for each creature a new distinct location in a uniform probability.  #
    # No creture has priority over someone else. Checks recursivly on each creature.#
    #################################################################################
    def move_on_board(self, forbidden_locations, temp_locations, creatures): 
        all_options = self.get_options_to_move() # get a list of all allowed locations
        new_location_opt = list(set(all_options).difference(set(forbidden_locations))) # eliminating locations where the creature already lost in the fight
        if len(new_location_opt) == 0: # if creature lost in all of his possible locations, than he does'nt have a choice but trying again everything
            new_location_opt = list(all_options)
        new_loc = new_location_opt[random.randrange(0, len(new_location_opt))] # new location idx
        if temp_locations[new_loc] == 0:      # new possition in empty, no collision
            temp_locations[new_loc] = self.id # locate create in new position
            self.next_location = new_loc      # update creatures location
        else: 
            # collision between creatures
            # get probability to give up the new location and try a diffrent one
            give_up = raffle(0.5) 
            if give_up:
                forbidden_locations.add(new_loc) # now this location is forbidden as well
                temp_locations = self.move_on_board(forbidden_locations, temp_locations, creatures) # creature tries again in other locations                    
            else: # didnt give up, gets the new location, rival has to choose a diffrent location to move to
                rival = creatures[temp_locations[new_loc]] # the creatre creates the collision with the same new position    
                temp_locations[new_loc] = self.id          # locate create in new position
                self.next_location = new_loc               # update creatures location
                temp_locations = rival.move_on_board(set([new_loc, ()]), temp_locations, creatures) # rival tries again another location since he lost
        return temp_locations
       #################################################################################
    
   # update cretures location after movement, called from board only when all creatures have a bew valid location
    def update_location(self):
        self.location = self.next_location
        self.next_location = None
        
        
        
        
        
        