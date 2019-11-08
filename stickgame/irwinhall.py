from scipy.special import comb
from math import factorial

class IrwinHall:
    def __init__(self, numvars, lower=0.0, upper=1.0):
        self.numvars = numvars # Number of uniformly drawn r.v.s
        self.lower   = lower   # Each r.v. drawn from U[lower, upper]
        self.upper   = upper

    # If X ~ IH(numvars), then cdf(x) = p(lower \le X \le x)
    def cdf(self, x):
        if x < self.numvars*self.lower:
            return 0.0
        elif x > self.numvars*self.upper:
            return 1.0
        else:
            x_transform = (x - self.numvars*self.lower) / (self.upper - self.lower)
            sum = 0.0
            for ii in range(int(x_transform)+1):
                sum += ((-1)**ii) * comb(self.numvars, ii) * ((x_transform - ii)**self.numvars)
            return (1 / factorial(self.numvars)) * sum
