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
biasPrior = ['flat', 'v']
statistic = ['mean', 'median']
biasPenalty = [0., 1., 3., 10.]

# Create iterator to loop through
iterator = product(biasPrior, statistic, biasPenalty)

num_max = 5

ind = 0
for x in iterator:
    # Create pandas dataframe with results, append to results csv
    settings = {'biasPrior': [x[0]],
                'statistic': [x[1]],
                'biasPenalty': [x[2]]}

    df = pd.DataFrame.from_dict(settings)
    exp_name = 'exp' + str(ind).zfill(num_max)
    df.to_csv(os.getcwd() + '/parameters/' + exp_name + '.csv', header=False, index=False)

    ind += 1
