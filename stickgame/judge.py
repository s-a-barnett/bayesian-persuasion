from stickgame.irwinhall import IrwinHall

class FixedJudge:
    def __init__(self, numsticks, agent1bias='s', agent2bias='l'):
        self.numsticks  = numsticks # Total number of sticks in sample
        self.sumlengths = 0.0 # Tracks current sum of stick lengths

        self.agent1obs  = []  # List of moves made by agent 1
        self.agent2obs  = []  # and agent 2

        self._recompute_sum_and_threshold()
        self.agent1bias = agent1bias # Determines strategy for agent 1
        self.agent2bias = agent2bias # and agent 2

        self.upper = 1.0
        self.lower = 0.0

    # Keeps track of the total stick length needed for the sample to be 'long'
    def _recompute_sum_and_threshold(self):
        self.sumlengths = sum(self.agent1obs+self.agent2obs)
        self.threshold = max(0.5*self.numsticks - self.sumlengths, 0.0)

    # Keeps track of the range of possible future stick lengths
    def _compute_upper_and_lower(self):
        for agent in [[self.agent1obs, self.agent1bias], [self.agent2obs, self.agent2bias]]:
            if agent[0]:
                if agent[1] == 'l':
                    self.upper = min(agent[0])
                elif agent[1] == 's':
                    self.lower = max(agent[0])
                elif agent[1] != 'n':
                    raise ValueError

    def compute_p_long(self):
        self._recompute_sum_and_threshold()
        self._compute_upper_and_lower()

        num_unseen = self.numsticks - len(self.agent1obs+self.agent2obs)

        ih = IrwinHall(num_unseen, lower=self.lower, upper=self.upper)

        return 1 - ih.cdf(self.threshold)
