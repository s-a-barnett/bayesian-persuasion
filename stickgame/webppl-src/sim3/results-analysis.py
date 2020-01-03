import numpy as np
import pandas as pd
import os

# Initialise lists
numExp_vals            = []
stick_vals            = []
probBiasedLong_vals = []
probNeutral_vals    = []

def getBiasProb(df, bias):
    return df[df.bias0==bias].sum()['prob']

for numExp in range(len(next(os.walk('parameters/'))[2])):
    exists = os.path.isfile('results/exp' + str(numExp) + '_moves.csv')
    if exists:
        # Read params
        df_params = pd.read_csv('parameters/exp' + str(numExp).zfill(5) + '.csv', header=None)
        # Read raw data
        df_sticks = pd.read_csv('results/exp' + str(numExp) + '_moves.csv', header=None)
        df_m0     = pd.read_csv('results/exp' + str(numExp) + '_move0.csv')
        df_m1     = pd.read_csv('results/exp' + str(numExp) + '_move1.csv')

        sticks = np.asarray(df_sticks)[0, 1:]

        # Record probability that agents have bias = 5.0
        probBiasedLong_m0 = getBiasProb(df_m0, 5)
        probBiasedLong_m1 = getBiasProb(df_m1, 5)

        # Record probability that agents have bias = 0.0
        probNeutral_m0 = getBiasProb(df_m0, 0)
        probNeutral_m1 = getBiasProb(df_m1, 0)

        numExp_vals.append(numExp)
        stick_vals += list(sticks)
        probBiasedLong_vals.append(probBiasedLong_m0)
        probBiasedLong_vals.append(probBiasedLong_m1)
        probNeutral_vals.append(probNeutral_m0)
        probNeutral_vals.append(probNeutral_m1)

move_vals   = [0,1]*len(numExp_vals)
numExp_vals = sorted(numExp_vals*2)

results_dict = {'numExp': numExp_vals,
                'move': move_vals,
                'stick': stick_vals,
                'probBiasedLong': probBiasedLong_vals,
                'probNeutral': probNeutral_vals}

df = pd.DataFrame(results_dict).set_index('numExp')
df.to_csv('results_summary.csv')
