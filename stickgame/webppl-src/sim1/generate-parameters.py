import os
from itertools import product
import numpy as np
import pandas as pd

# Create folder in working directory to store text files
if os.path.isdir('parameters') is False:
    os.mkdir('parameters')

# Create folder in working directory to store results
if os.path.isdir('results') is False:
    os.mkdir('results')

# Write out lists of hyperparameters
nSticks        = [3, 4, 5]
agent0stick    = [round(0.025+0.05*i, 3) for i in range(20)]
agent1stick    = agent0stick
fixedBiasAgent = [2., 5., 10.]

# Create iterator to loop through
iterator = product(nSticks, agent0stick, agent1stick, fixedBiasAgent)

num_max = 5

ind = 0
for x in iterator:
    # Create pandas dataframe with results, append to results csv
    settings = {'nSticks': [x[0]],
                'agent0stick': [x[1]],
                'agent1stick': [x[2]],
                'fixedBiasAgent': [x[3]]}

    df = pd.DataFrame.from_dict(settings)
    exp_name = 'exp' + str(ind).zfill(num_max)
    df.to_csv(os.getcwd() + '/parameters/' + exp_name + '.csv', header=False, index=False)

    ind += 1
