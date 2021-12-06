import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

df = pd.read_csv('judge-heatmap.csv')
df['stickLength'] = df['stick'] * 10
df['stickLength'] = df['stickLength'].astype(int)
df['weeStrength'] = np.maximum(-(df['belief'] - 0.5), 0)
df = df[df['stickLength'] >= 5]

grid_kws = {'width_ratios': [1,1,1,0.08]}
fig, axs = plt.subplots(1, 4, figsize=(20, 6), gridspec_kw=grid_kws)
nSticks = [3, 4, 5]
axs[0].get_shared_y_axes().join(axs[1], axs[2])
for i in range(3):
  cbar_ax = None if i < 2 else axs[3]
  df_pivot = df[df['nSticks'] == nSticks[i]].pivot('stickLength', 'agentBias', 'weeStrength')
  sns.heatmap(ax=axs[i], data=df_pivot, vmin=0, vmax=0.5, cbar=(i == 2),
              cbar_ax=cbar_ax, center=0)
  axs[i].invert_yaxis();
  axs[i].set_title(f'nSticks = {nSticks[i]}');
  if i != 0:
    axs[i].set_ylabel('');
    axs[i].set_yticks([]);
  else:
    axs[i].set_ylabel('stick length (inches)');
  if i != 1:
    axs[i].set_xlabel('');
  else:
    axs[i].set_xlabel('agent bias');
  plt.suptitle('Strength of Weak Evidence Effect under the RSA Model')

plt.savefig('wee-heatmap.png')
plt.close()
