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
agent0stick    = [round(0.025+0.05*i, 3) for i in range(20)]
agent1stick    = agent0stick
fixedBiasAgent = [2., 5., 10.]

# Create iterator to loop through
iterator = product(agent0stick, agent1stick, fixedBiasAgent)

num_max = 5

ind = 0
for x in iterator:
    # Create pandas dataframe with results, append to results csv
    if (x[0] >= 0.5) and (x[1] <= 0.5):
        settings = {'agent0stick': [x[0]],
                    'agent1stick': [x[1]],
                    'fixedBiasAgent': [x[2]]}

        df = pd.DataFrame.from_dict(settings)
        exp_name = 'exp' + str(ind).zfill(num_max)
        df.to_csv(os.getcwd() + '/parameters/' + exp_name + '.csv', header=False, index=False)

        ind += 1
