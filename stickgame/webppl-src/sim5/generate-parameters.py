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
nSticks   = [3]
statistic = ['mean']
liarAlpha = [10., 50., 100., 500.]
alpha     = [10., 50., 100., 500.]

# Create iterator to loop through
iterator = product(nSticks, statistic, liarAlpha, alpha)

num_max = 5

ind = 0
for x in iterator:
    # Create pandas dataframe with results, append to results csv
    settings = {'nSticks': [x[0]],
                'statistic': [x[1]],
                'liarAlpha': [x[2]],
                'alpha': [x[3]]}

    df = pd.DataFrame.from_dict(settings)
    exp_name = 'exp' + str(ind).zfill(num_max)
    df.to_csv(os.getcwd() + '/parameters/' + exp_name + '.csv', header=False, index=False)

    ind += 1
