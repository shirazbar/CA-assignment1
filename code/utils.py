import random

MATRIX_SIZE = 200

EMPTY = 0
HEALTHY = 1
CONTAGIOUS = 2
NOT_CONTAGIOUS = 3

# bool checks if random is smaller then the probability given
def raffle(probability):
    return random.random() < probability