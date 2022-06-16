import pandas as pd
import seaborn as sns
import numpy as np
import matplotlib.pyplot as plt
from itertools import product

d = pd.read_csv('../output/rsa-het-speakers-posterior-replication.csv', index_col=0)
d_weights = d[d.param.str.startswith('g')]
d_pos = d[d.param.isin(['J1-agentBias', 'offset'])]
convert_dict = {'val': float, 'prob': float}
d_weights = d_weights.astype(convert_dict)
d_pos = d_pos.astype(convert_dict)

d_weights[['category', 'level', 'strength']] = d_weights['param'].str.split('-', expand=True)
level_dict = {'J0': 'L0', 'J1': 'L1'}
stick_dict = dict(zip(['less', '0.8', '0.9'], range(1, 4)))
d_weights['level'] = d_weights['level'].map(lambda x: level_dict[x])
d_weights['strength'] = d_weights['strength'].map(lambda x: stick_dict[x])
d_weights = d_weights.astype(convert_dict)

fig, axs = plt.subplots(1, 2, figsize=(12,6))

sns.kdeplot(ax=axs[0], data=d_pos[d_pos['param']=='J1-agentBias'], x='val', weights='prob')
sns.kdeplot(ax=axs[1], data=d_pos[d_pos['param']=='offset'], x='val', weights='prob')
axs[0].set_title('$L_1$ $\\beta$')
axs[1].set_title('offset')
for i in range(2):
    axs[i].set_xlabel('Value')
    axs[i].set_ylabel('Posterior Density')
    axs[i].grid()

fig.savefig('../output/posterior_plots.pdf', backend='pdf')

plt.clf()

g = sns.FacetGrid(d_weights, col='strength', hue='level')
g.map_dataframe(sns.kdeplot, x='val', weights='prob', fill=True, alpha=.5, linewidth=0)
g.add_legend()
g.set_axis_labels(x_var='Value')
g.savefig('../output/level_prior_plots.pdf', backend='pdf')

plt.clf()
