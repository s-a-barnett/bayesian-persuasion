import numpy as np
import pandas as pd
import os

array  = np.stack([np.asarray(pd.read_csv('results/scores_{}.csv'.format(1000*round(0.025+0.05*ii, 3)), header =None))[0] for ii in range(20)])
stick_vals = [round(0.025 + 0.05*ii, 3) for ii in range(20)]

df = pd.DataFrame(array, index=stick_vals, columns=stick_vals)
df.to_csv('results_summary.csv')
