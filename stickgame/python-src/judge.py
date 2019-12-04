from stickgame.irwinhall import IrwinHall
import numpy as np
from itertools import product
from math import factorial
from scipy.special import comb

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
        self.sumlengths = float(sum(self.agent1obs+self.agent2obs))
        self.threshold  = max(0.5*self.numsticks - self.sumlengths, 0.0)

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

# Useful default prior for joint bias distribution
unifjointprior = (1.0/7.0)*np.ones((3,3))
unifjointprior[0,0] = 0.0; unifjointprior[2,2] = 0.0

class Judge:
    def __init__(self, numsticks, jointbiasprior=unifjointprior):
        self.numsticks = numsticks
        self.jointbiasprior = jointbiasprior

        self.agent1obs  = []  # List of moves made by agent 1
        self.agent2obs  = []  # and agent 2

    def _biases2indices(self, biases):
        indices = []
        for bias in biases:
            if bias == 's':
                indices.append(0)
            elif bias == 'n':
                indices.append(1)
            elif bias == 'l':
                indices.append(2)
            else:
                return ValueError
        return indices

    # Deals with case where biases = ['s', 'n'], ['l', 'n'] or reverse
    # Uses the hypergeometric distribution
    def _likelihood_onebias(self, biases):
        # Rename variables for convenience
        N = self.numsticks; N_1 = len(self.agent1obs); N_2 = len(self.agent2obs)

        jointobs = [self.agent1obs, self.agent2obs]

        prob_unordered = (factorial(N-N_1)*factorial(N-N_2)) / (factorial(N-N_1-N_2)*factorial(N))

        # Yield the size of the neutrally sampled observations
        # Will equal either N_1, or N_2
        N_neutral = len(jointobs[biases.index('n')])
        return prob_unordered / factorial(N_neutral)

    # Deals with cases where biases = ['n', 'n']
    def _likelihood_nobias(self):
        # Rename variables for convenience
        N = self.numsticks; N_1 = len(self.agent1obs); N_2 = len(self.agent2obs)

        # Compute \sum_{K=N_2}^{N-N_1} p(S_1, S_2 ordered | S_1) p(S_1)
        sum = 0.0
        for K in range(N_2, N-N_1+1):
            sum += (comb(N-K-1, N_1-1)*comb(K, N_2))

        # Multiply by factor of 2 as order can be in either direction
        prob_ordered = 2 * sum / (comb(N, N_1) * comb(N-N_1, N_2))

        # Take into account specific ordering of samples
        prob_ordered /= (factorial(N_1)*factorial(N_2))
        return prob_ordered

    # Note: these calculations assume len(self.agent1obs + self.agent2obs) < numsticks
    # TODO: Find better way of storing and updating agent observations
    def _obslikelihood(self, biases):
        jointobs = [self.agent1obs, self.agent2obs]

        # Returns 1.0 if no observations to consider
        if jointobs == [[], []]:
            return 1.0

        # Returns 0.0 if observation order not consistent with agent bias
        for ii in range(2):
            if biases[ii] == 's' and not np.allclose(jointobs[ii], np.sort(jointobs[ii])):
                return 0.0
            elif biases[ii] == 'l' and not np.allclose(jointobs[ii], np.sort(jointobs[ii])[::-1]):
                return 0.0
            else:
                pass

        # Handles case with one empty, one non-empty
        if sorted(list(map(bool, jointobs))) == [False, True]:
            if biases[jointobs.index([])] == 'n':
                N_neutral = len(jointobs[biases.index('n')])
                N = self.numsticks
                return factorial(N-N_neutral) / factorial(N)
            else:
                return 1.0

        # Returns 0.0 if samples are 'interleaved' but agent bias not neutral
        # Must have non-empty observations for both
        if self.agent1obs and self.agent2obs:
            if ((np.min(self.agent1obs) < np.min(self.agent2obs) < np.min(self.agent1obs)) \
                or (np.min(self.agent2obs) < np.min(self.agent1obs) < np.min(self.agent2obs))) \
                and biases != ['n', 'n']:
                return 0.0

        # Returns 0.0 if bias not consistent with other agent's observations
        for ii in range(2):
            if (biases[ii] == 's') and (biases[1-ii] == 'l') and \
                (np.max(jointobs[ii]) > np.min(jointobs[1-ii])):
                return 0.0

        # Returns 1.0 if observations are appropriately ordered and separated
        # with both agents biased
        if sorted(self._biases2indices(biases)) == [0, 2]:
            return 1.0

        if sorted(self._biases2indices(biases)) == [0,1] or sorted(self._biases2indices(biases)) == [1,2]:
            return self._likelihood_onebias(biases)

        if biases == ['n', 'n']:
            return self._likelihood_nobias()

    def compute_p_long(self):
        numerator = 0.0; denominator = 0.0
        for biases in product(['s', 'n', 'l'], repeat=2):
            if biases == ['s', 's'] or biases == ['l', 'l']:
                pass
            else:
                biases = list(biases)
                fjudge = FixedJudge(self.numsticks, biases[0], biases[1])
                fjudge.agent1obs = self.agent1obs; fjudge.agent2obs = self.agent2obs

                # Avoid computing this twice
                obs_likelihood = self._obslikelihood(biases)

                numerator += fjudge.compute_p_long() * obs_likelihood * self.jointbiasprior(tuple(self._biases2indices(biases)))
                denominator += obs_likelihood

        return numerator / denominator
