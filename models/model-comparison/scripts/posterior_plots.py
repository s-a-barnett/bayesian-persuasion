import pandas as pd
import seaborn as sns
import numpy as np
import matplotlib.pyplot as plt
from itertools import product

d = pd.read_csv('rsa-het-speakers-replication-posterior-full.csv', index_col=False)
d_groups = d[d.param.str.startswith('p')]
d_weights = d[d.param.str.startswith('g')]
d_pos = d[d.param.str.startswith('J') | d.param.str.startswith('l')]
convert_dict = {'val': float, 'prob': float}
d_weights = d_weights.astype(convert_dict)
d_pos = d_pos.astype(convert_dict)
d_pos = pd.concat([d_pos, pd.DataFrame({'param': ['J1nSticks'], 'val': [3.0], 'prob': [0.0]})])

d_weights[['category', 'level', 'strength']] = d_weights['param'].str.split('-', expand=True)
level_dict = {'noise': 'noise', 'J0': 'L0', 'J1': 'L1'}
stick_dict = dict(zip(['0.2', '0.4', '0.7', '0.8', '0.9'], range(1, 6)))
d_weights['level'] = d_weights['level'].map(lambda x: level_dict[x])
d_weights['strength'] = d_weights['strength'].map(lambda x: stick_dict[x])
d_weights = d_weights.astype(convert_dict)

print(d_groups.groupby('val')['prob'].mean())

fig, axs = plt.subplots(2, 2, figsize=(12,10))

sns.barplot(ax=axs[0][0], data=d_pos[d_pos['param']=='J0nSticks'], x='val', y='prob')
axs[0][0].set_xticks([0,1,2], [3,4,5])
axs[0][0].set_yticks(0.2*np.arange(6))
axs[0][0].set_title('$L_0$ $\hat{N}$')
sns.barplot(ax=axs[0][1], data=d_pos[d_pos['param']=='J1nSticks'], x='val', y='prob')
axs[0][1].set_xticks([0,1,2], [3,4,5])
axs[0][0].set_yticks(0.2*np.arange(6))
axs[0][1].set_title('$L_1$ $\hat{N}$')
sns.kdeplot(ax=axs[1][0], data=d_pos[d_pos['param']=='J1agentBias'], x='val', weights='prob')
sns.kdeplot(ax=axs[1][1], data=d_pos[d_pos['param']=='logitSigma'], x='val', weights='prob')
axs[1][0].set_title('$L_1$ $\\beta$')
axs[1][1].set_title('$\sigma$')
for i, j in product(range(2), range(2)):
    axs[i][j].set_xlabel('Value')
    axs[0][j].set_ylabel('Posterior Probability')
    axs[1][j].set_ylabel('Posterior Density')
    
fig.savefig('../output/posterior_plots.pdf', backend='pdf')

plt.clf()

g = sns.FacetGrid(d_weights, col='strength', hue='level', col_wrap=3)
g.map_dataframe(sns.kdeplot, x='val', weights='prob', fill=True, alpha=.5, linewidth=0)
g.add_legend(loc=(0.8, 0.2))
g.set_axis_labels(x_var='Value')
g.savefig('../output/level_prior_plots.pdf', backend='pdf')

plt.clf()
