import numpy as np
import pandas as pd
import os

# Initialise lists
numExp_vals      = []
agentBias_vals   = []
biasPrior_vals   = []
sampleMean_vals  = []
sampleMax_vals   = []
sampleUQ_vals    = []
MAP_S1_vals      = []
MAP_S2_vals      = []
idx_MAP_S1_vals  = []
idx_MAP_S2_vals  = []
max_S1_vals      = []
max_S2_vals      = []
logMaxRatio_vals = []

# Return index (1-indexing) and probability of MAP stick
def getMAPsticks(df):
    prob_MAP = df.max()[1]
    idx_MAP = int(df.idxmax()[1])
    return prob_MAP, idx_MAP+1

for numExp in range(len(next(os.walk('parameters/'))[2])):
    exists = os.path.isfile('results/exp' + str(numExp) + '_sticks.csv')
    if exists:
        # Read params
        df_params = pd.read_csv('parameters/exp' + str(numExp).zfill(5) + '.csv', header=None)
        # Read raw data
        df_sticks = pd.read_csv('results/exp' + str(numExp) + '_sticks.csv', header=None)
        df_S1     = pd.read_csv('results/exp' + str(numExp) + '_S1.csv', header=None)
        df_S2     = pd.read_csv('results/exp' + str(numExp) + '_S2.csv', header=None)

        sticks = np.asarray(df_sticks)[0]

        nSticks    = int(df_params[0])
        agentBias  = float(df_params[1]) * float(10 ** df_params[3])
        biasPrior  = np.asarray(df_params[2])[0]
        sampleMean = np.mean(sticks)
        sampleMax  = np.max(sticks)
        sampleUQ   = np.percentile(sticks, 75)

        # Record MAP value and idx for first choice for S1
        MAP_S1, idx_MAP_S1 = getMAPsticks(df_S1)
        MAP_S2, idx_MAP_S2 = getMAPsticks(df_S2)

        # Record probability mass of highest stick
        max_S1 = np.asarray(df_S1)[0,1]
        max_S2 = np.asarray(df_S2)[0,1]
        logMaxRatio = np.log(max_S1) - np.log(max_S2)

        numExp_vals.append(numExp)
        agentBias_vals.append(agentBias)
        biasPrior_vals.append(biasPrior)
        sampleMean_vals.append(sampleMean)
        sampleMax_vals.append(sampleMax)
        sampleUQ_vals.append(sampleUQ)
        MAP_S1_vals.append(MAP_S1)
        idx_MAP_S1_vals.append(idx_MAP_S1)
        MAP_S2_vals.append(MAP_S2)
        idx_MAP_S2_vals.append(idx_MAP_S2)
        max_S1_vals.append(max_S1)
        max_S2_vals.append(max_S2)
        logMaxRatio_vals.append(logMaxRatio)

results_dict = {'numExp': numExp_vals,
                'agentBias': agentBias_vals,
                'biasPrior': biasPrior_vals,
                'sampleMean': sampleMean_vals,
                'sampleMax': sampleMax_vals,
                'sampleUQ': sampleUQ_vals,
                'MAP_S1': MAP_S1_vals,
                'idx_MAP_S1': idx_MAP_S1_vals,
                'MAP_S2': MAP_S2_vals,
                'idx_MAP_S2': idx_MAP_S2_vals,
                'max_S1': max_S1_vals,
                'max_S2': max_S2_vals,
                'logMaxRatio': logMaxRatio_vals}

df = pd.DataFrame(results_dict).set_index('numExp')
df.to_csv('results_summary.csv')
