import os
from itertools import product
import numpy as np
import pandas as pd

# Create folder in working directory to store text files
if os.path.isdir('parameters') is False:
    os.mkdir('parameters')

# Write out lists of hyperparameters
nSticks         = [3, 4, 5]
agent0stick     = [round(0.525+0.05*i, 3) for i in range(10)]
agent1stick     = [round(0.475-0.05*i, 3) for i in range(10)]
fixedBiasAgent0 = [10.]
fixedBiasAgent1 = [10.]

# Create iterator to loop through
iterator = product(nSticks, agent0stick, agent1stick, fixedBiasAgent0, fixedBiasAgent1)

num_max = 5

ind = 0
for x in iterator:
    # Create pandas dataframe with results, append to results csv
    settings = {'nSticks': [x[0]],
                'agent0stick': [x[1]],
                'agent1stick': [x[2]],
                'fixedBiasAgent0': [x[3]],
                'fixedBiasAgent1': [x[4]]}

    df = pd.DataFrame.from_dict(settings)
    exp_name = 'exp' + str(ind).zfill(num_max)
    df.to_csv(os.getcwd() + '/parameters/' + exp_name + '.csv', header=False, index=False)

    ind += 1
