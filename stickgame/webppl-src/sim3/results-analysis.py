import numpy as np
import pandas as pd
import os

# Initialise lists
numExp_vals    = []
stick_vals     = []
biasPrior_vals = []
biasVal_vals   = []
biasProb_vals  = []

def getBiasProb(df, bias):
    return df[df.bias0==bias].sum()['prob']

for numExp in range(len(next(os.walk('parameters/'))[2])):
    exists = os.path.isfile('results/exp' + str(numExp) + 'posterior.csv')
    if exists:
        # Read params
        df_params = pd.read_csv('parameters/exp' + str(numExp).zfill(5) + '.csv', header=None)
        # Read raw data
        df_posterior     = pd.read_csv('results/exp' + str(numExp) + 'posterior.csv')

        stick = float(df_params[1])
        biasPrior = np.asarray(df_params[2])[0]

        for biasVal in [0, 2, 5, 10]:
            numExp_vals.append(numExp)
            stick_vals.append(stick)
            biasPrior_vals.append(biasPrior)
            biasVal_vals.append(biasVal)
            biasProb_vals.append( getBiasProb(df_posterior, biasVal) )

results_dict = {'numExp': numExp_vals,
                'biasPrior': biasPrior_vals,
                'stick': stick_vals,
                'biasVal': biasVal_vals,
                'biasProb': biasProb_vals}

df = pd.DataFrame(results_dict)
df.to_csv('results_summary.csv')
