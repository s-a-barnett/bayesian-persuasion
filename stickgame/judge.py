from stickgame.irwinhall import IrwinHall

class Judge:
    def __init__(self, numsticks):
        self.numsticks = numsticks # Total number of sticks in sample
        self.sumlengths = 0.0 # Tracks current sum of stick lengths
