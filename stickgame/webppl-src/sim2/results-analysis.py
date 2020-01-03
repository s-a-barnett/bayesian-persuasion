import numpy as np
import pandas as pd
import os

# Initialise lists
numExp_vals        = []
agentBias_vals     = []
biasPrior_vals     = []
sampleMean_vals    = []
MAP_stick1_S1_vals = []
MAP_stick2_S1_vals = []
MAP_stick1_S2_vals = []
MAP_stick2_S2_vals = []
optProb_S1_vals    = []
optProb_S2_vals    = []
isOptMAP_S1_vals   = []
isOptMAP_S2_vals   = []

def getMAPsticks(df):
    MAP_sticks = df.iloc[df.idxmax()['prob']]
    return MAP_sticks[0], MAP_sticks[1]

def isOptMAP(stick1, stick2, sticks):
    ordered_sticks = sticks[np.argsort(sticks)]
    if np.isclose(stick1, ordered_sticks[-1]) & np.isclose(stick2, ordered_sticks[-2]):
        return True
    else:
        return False

def getOptProb(df, sticks):
    ordered_sticks = sticks[np.argsort(sticks)]
    optEntry = df[np.isclose(df['0'], ordered_sticks[-1]) & np.isclose(df['1'], ordered_sticks[-2])]
    if optEntry.empty:
        return 0.
    else:
        return float(optEntry['prob'])

for numExp in range(len(next(os.walk('parameters/'))[2])):
    exists = os.path.isfile('results/exp' + str(numExp) + '_sticks.csv')
    if exists:
        # Read params
        df_params = pd.read_csv('parameters/exp' + str(numExp).zfill(5) + '.csv', header=None)
        # Read raw data
        df_sticks = pd.read_csv('results/exp' + str(numExp) + '_sticks.csv', header =None)
        df_S1     = pd.read_csv('results/exp' + str(numExp) + '_S1.csv')
        df_S2     = pd.read_csv('results/exp' + str(numExp) + '_S2.csv')

        sticks = np.asarray(df_sticks)[0]

        nSticks    = int(df_params[0])
        agentBias  = float(df_params[1])
        biasPrior  = np.asarray(df_params[2])[0]
        sampleMean = np.mean(sticks)

        # Record MAP value for first two choices for S1
        MAP_stick1_S1, MAP_stick2_S1 = getMAPsticks(df_S1)
        MAP_stick1_S2, MAP_stick2_S2 = getMAPsticks(df_S2)

        # Record probability of choosing sticks in descending order
        optProb_S1 = getOptProb(df_S1, sticks)
        optProb_S2 = getOptProb(df_S2, sticks)

        # Record whether the optimal strategy is the MAP strategy
        isOptMAP_S1 = isOptMAP(MAP_stick1_S1, MAP_stick2_S1, sticks)
        isOptMAP_S2 = isOptMAP(MAP_stick1_S2, MAP_stick2_S2, sticks)

        numExp_vals.append(numExp)
        agentBias_vals.append(agentBias)
        biasPrior_vals.append(biasPrior)
        sampleMean_vals.append(sampleMean)
        MAP_stick1_S1_vals.append(MAP_stick1_S1)
        MAP_stick2_S1_vals.append(MAP_stick2_S1)
        MAP_stick1_S2_vals.append(MAP_stick1_S2)
        MAP_stick2_S2_vals.append(MAP_stick2_S2)
        optProb_S1_vals.append(optProb_S1)
        optProb_S2_vals.append(optProb_S2)
        isOptMAP_S1_vals.append(isOptMAP_S1)
        isOptMAP_S2_vals.append(isOptMAP_S2)

results_dict = {'numExp': numExp_vals,
                'agentBias': agentBias_vals,
                'biasPrior': biasPrior_vals,
                'sampleMean': sampleMean_vals,
                'MAP_stick1_S1': MAP_stick1_S1_vals,
                'MAP_stick2_S1': MAP_stick2_S1_vals,
                'MAP_stick1_S2': MAP_stick1_S2_vals,
                'MAP_stick2_S2': MAP_stick2_S2_vals,
                'optProb_S1': optProb_S1_vals,
                'optProb_S2': optProb_S2_vals,
                'isOptMAP_S1': isOptMAP_S1_vals,
                'isOptMAP_S2': isOptMAP_S2_vals}

df = pd.DataFrame(results_dict).set_index('numExp')
df.to_csv('results_summary.csv')
