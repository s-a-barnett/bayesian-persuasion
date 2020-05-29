import numpy as np
import pandas as pd
import os

# Initialise lists
numExp_vals        = []
stick1_vals        = []
stick2_vals        = []
agentBias_vals     = []
p_isLong_1_L0_vals = []
p_isLong_2_L0_vals = []
p_isLong_1_L1_vals = []
p_isLong_2_L1_vals = []
delta_L0_vals      = []
delta_L1_vals      = []

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


        numExp_vals.append(numExp)
        stick1_vals.append(stick1)
        stick2_vals.append(stick2)
        agentBias_vals.append(agentBias)
        p_isLong_1_L0_vals.append(p_isLong_1_L0)
        p_isLong_2_L0_vals.append(p_isLong_2_L0)
        p_isLong_1_L1_vals.append(p_isLong_1_L1)
        p_isLong_2_L1_vals.append(p_isLong_2_L1)
        delta_L0_vals.append(delta_L0)
        delta_L1_vals.append(delta_L1)

results_dict = {'numExp': numExp_vals,
                'stick1': stick1_vals,
                'stick2': stick2_vals,
                'agentBias': agentBias_vals,
                'p_isLong_1_J0': p_isLong_1_L0_vals,
                'p_isLong_2_J0': p_isLong_2_L0_vals,
                'p_isLong_1_J1': p_isLong_1_L1_vals,
                'p_isLong_2_J1': p_isLong_2_L1_vals,
                'delta_J0': delta_L0_vals,
                'delta_J1': delta_L1_vals}

df = pd.DataFrame(results_dict).set_index('numExp')
df.to_csv('results-summary.csv')
