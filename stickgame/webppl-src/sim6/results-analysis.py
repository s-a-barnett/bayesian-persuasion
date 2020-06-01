import numpy as np
import pandas as pd
import os

# Initialise lists
numExp_vals     = []
stick1_vals     = []
stick2_vals     = []
agentBias_vals  = []
judge_vals      = []
p_isLong_1_vals = []
p_isLong_2_vals = []
delta_vals      = []

for numExp in range(len(next(os.walk('parameters/'))[2])):
    exists = os.path.isfile('results/exp' + str(numExp) + '.csv')
    if exists:
        # Read params
        df_params = pd.read_csv('parameters/exp' + str(numExp).zfill(5) + '.csv', header=None)
        # Read raw data
        df_results = pd.read_csv('results/exp' + str(numExp) + '.csv')

        stick1  = float(df_params[0])
        stick2  = float(df_params[1])
        agentBias = float(df_params[2])
        p_isLong_1_L0 = float(np.exp(df_results['firstJ0']))
        p_isLong_2_L0 = float(np.exp(df_results['secondJ0']))
        p_isLong_1_L1 = float(np.exp(df_results['firstJ1']))
        p_isLong_2_L1 = float(np.exp(df_results['secondJ1']))

        delta_L0 = p_isLong_2_L0 - p_isLong_1_L0
        delta_L1 = p_isLong_2_L1 - p_isLong_1_L1

        numExp_vals += 2 * [numExp]
        stick1_vals += 2 * [stick1]
        stick2_vals += 2 * [stick2]
        agentBias_vals += 2 * [agentBias]
        judge_vals += ['J0', 'J1']
        p_isLong_1_vals += [p_isLong_1_L0, p_isLong_1_L1]
        p_isLong_2_vals += [p_isLong_2_L0, p_isLong_2_L1]
        delta_vals += [delta_L0, delta_L1]


results_dict = {'numExp': numExp_vals,
                'stick1': stick1_vals,
                'stick2': stick2_vals,
                'judge': judge_vals,
                'agentBias': agentBias_vals,
                'p_isLong_1': p_isLong_1_vals,
                'p_isLong_2': p_isLong_2_vals,
                'delta': delta_vals}

df = pd.DataFrame(results_dict)
df.to_csv('results-summary.csv')
