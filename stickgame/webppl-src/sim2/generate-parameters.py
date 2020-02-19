import os
from itertools import product
import numpy as np
import pandas as pd

# Create folder in working directory to store text files
if os.path.isdir('parameters') is False:
    os.mkdir('parameters')

# Write out lists of hyperparameters
nSticks = [5] * 500
agentBias = [10.]
biasPrior = ['flat', 'v']
scale = [1]

# Create iterator to loop through
iterator = product(nSticks, agentBias, biasPrior, scale)

num_max = 5

ind = 0
for x in iterator:
    # Create pandas dataframe with results, append to results csv
    settings = {'nSticks': [x[0]],
                'agentBias': [x[1]],
                'biasPrior': [x[2]],
                'scale': [x[3]]}

    df = pd.DataFrame.from_dict(settings)
    exp_name = 'exp' + str(ind).zfill(num_max)
    df.to_csv(os.getcwd() + '/parameters/' + exp_name + '.csv', header=False, index=False)

    ind += 1
