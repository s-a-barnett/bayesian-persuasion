import numpy as np
import pandas as pd
import os

# Initialise lists
numExp_vals         = []
nSticks_vals        = []
stick1_vals         = []
stick2_vals         = []
p_isLong_1_L0_vals  = []
p_isLong_2_L0_vals  = []
p_isLong_1_L1_vals  = []
p_isLong_2_L1_vals  = []
is_WEE_vals         = []
dBias_weak_1_vals   = []
dBias_strong_1_vals = []
dBias_weak_2_vals   = []
dBias_strong_2_vals = []

# TODO - Auto-count number of results
for numExp in range(27):
    exists = os.path.isfile('results/exp' + str(numExp) + 'priorL0.csv')
    if exists:
        # Read params
        df_params = pd.read_csv('parameters/exp' + str(numExp).zfill(5) + '.csv', header=None)
        # Read raw data
        df_priorL0 = pd.read_csv('results/exp' + str(numExp) + 'priorL0.csv')
        df_weakL0  = pd.read_csv('results/exp' + str(numExp) + 'weakL0.csv')
        df_priorL1 = pd.read_csv('results/exp' + str(numExp) + 'priorL1.csv')
        df_weakL1  = pd.read_csv('results/exp' + str(numExp) + 'weakL1.csv')

        nSticks = int(df_params[0])
        stick1  = float(df_params[1])
        stick2  = float(df_params[2])
        p_isLong_1_L0 = df_priorL0[df_priorL0.isLong == True].sum()['prob']
        p_isLong_2_L0 = df_weakL0[df_weakL0.isLong == True].sum()['prob']
        p_isLong_1_L1 = df_priorL1[df_priorL1.isLong == True].sum()['prob']
        p_isLong_2_L1 = df_weakL1[df_weakL1.isLong == True].sum()['prob']

        # Weak Evidence Effect if the second stick increases the probability that
        # the sample is long for the pragmatic judge, but not the literal judge.
        is_WEE = (p_isLong_1_L0 >= p_isLong_2_L0) & (p_isLong_2_L1 >= p_isLong_1_L1)

        # Change in belief that Player i is biased
        # Note: prior probability that weakly (resp. strongly) biased in correct direction is 0.2 (resp. 0.25)
        # Naming issue: 'weak' is referring either to WEE or to a bias of 1.0
        dBias_weak_1   = df_priorL1[df_priorL1.bias0 == 1.].sum()['prob'] - 0.2
        dBias_strong_1 = df_priorL1[df_priorL1.bias0 == 5.].sum()['prob'] - 0.25
        dBias_weak_2   = df_weakL1[df_weakL1.bias1   == -1.].sum()['prob'] - 0.2
        dBias_strong_2 = df_weakL1[df_weakL1.bias1   == -5.].sum()['prob'] - 0.25

        numExp_vals.append(numExp)
        nSticks_vals.append(nSticks)
        stick1_vals.append(stick1)
        stick2_vals.append(stick2)
        p_isLong_1_L0_vals.append(p_isLong_1_L0)
        p_isLong_2_L0_vals.append(p_isLong_2_L0)
        p_isLong_1_L1_vals.append(p_isLong_1_L1)
        p_isLong_2_L1_vals.append(p_isLong_2_L1)
        is_WEE_vals.append(is_WEE)
        dBias_weak_1_vals.append(dBias_weak_1)
        dBias_strong_1_vals.append(dBias_strong_1)
        dBias_weak_2_vals.append(dBias_weak_2)
        dBias_strong_2_vals.append(dBias_strong_2)

results_dict = {'numExp': numExp_vals,
                'nSticks': nSticks_vals,
                'stick1': stick1_vals,
                'stick2': stick2_vals,
                'p_isLong_1_L0': p_isLong_1_L0_vals,
                'p_isLong_2_L0': p_isLong_2_L0_vals,
                'p_isLong_1_L1': p_isLong_1_L1_vals,
                'p_isLong_2_L1': p_isLong_2_L1_vals,
                'is_WEE': is_WEE_vals,
                'dBias_weak_1': dBias_weak_1_vals,
                'dBias_strong_1': dBias_strong_1_vals,
                'dBias_weak_2': dBias_weak_2_vals,
                'dBias_strong_2': dBias_strong_2_vals}

df = pd.DataFrame(results_dict).set_index('numExp')
df.to_csv('results_summary.csv')
