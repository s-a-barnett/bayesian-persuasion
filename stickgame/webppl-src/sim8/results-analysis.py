import numpy as np
import pandas as pd
import os

# Initialise lists
numExp_vals     = []
stick1_vals     = []
agentBias_vals  = []
nSticks_vals    = []
judge_vals      = []
p_isLong_1_vals = []
p_isLong_2_vals = []

for numExp in range(len(next(os.walk('parameters/'))[2])):
    exists = os.path.isfile('results/exp' + str(numExp) + '.csv')
    if exists:
        # Read params
        df_params = pd.read_csv('parameters/exp' + str(numExp).zfill(5) + '.csv', header=None)
        # Read raw data
        df_results = pd.read_csv('results/exp' + str(numExp) + '.csv')

        stick1  = float(df_params[0])
        agentBias = float(df_params[1])
        nSticks = float(df_params[2])
        p_isLong_1_L0 = float(np.exp(df_results['firstJ0']))
        p_isLong_1_L1 = float(np.exp(df_results['firstJ1']))

        numExp_vals += 2 * [numExp]
        stick1_vals += 2 * [stick1]
        agentBias_vals += 2 * [agentBias]
        nSticks_vals += 2 * [nSticks]
        judge_vals += ['J0', 'J1']
        p_isLong_1_vals += [p_isLong_1_L0, p_isLong_1_L1]


results_dict = {'numExp': numExp_vals,
                'stick1': stick1_vals,
                'judge': judge_vals,
                'agentBias': agentBias_vals,
                'nSticks': nSticks_vals,
                'p_isLong_1': p_isLong_1_vals}

df = pd.DataFrame(results_dict)
df.to_csv('results-summary.csv')
