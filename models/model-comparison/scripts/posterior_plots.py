import pandas as pd
import seaborn as sns
import numpy as np
import matplotlib.pyplot as plt
from itertools import product
from scipy.stats import gaussian_kde
from scipy.optimize import minimize

d = pd.read_csv('../output/rsa-het-speakers-posterior-replication.csv', index_col=0)
d_weights = d[d.param.str.startswith('g')]
d_pos = d[d.param.isin(['J1-agentBias', 'offset'])]
convert_dict = {'val': float, 'prob': float}
d_weights = d_weights.astype(convert_dict)
d_pos = d_pos.astype(convert_dict)

data = d_pos[d_pos['param'] == 'J1-agentBias']['val'].to_numpy()
weights = d_pos[d_pos['param'] == 'J1-agentBias']['prob'].to_numpy()

kern = gaussian_kde(data, weights=weights)

print('J1 agent bias MAP param\n')
print(minimize(lambda x: -kern.logpdf(x), 1.0))

data = d_pos[d_pos['param'] == 'offset']['val'].to_numpy()
weights = d_pos[d_pos['param'] == 'offset']['prob'].to_numpy()

kern = gaussian_kde(data, weights=weights)

print('J1 offset MAP param\n')
print(minimize(lambda x: -kern.logpdf(x), 1.0))

d_weights[['category', 'level', 'strength']] = d_weights['param'].str.split('-', expand=True)
level_dict = {'J0': 'L0', 'J1': 'L1'}
stick_dict = dict(zip(['less', '0.8', '0.9'], ['less strong evidence first', 'less strong evidence first', 'strongest evidence first']))
d_weights['level'] = d_weights['level'].map(lambda x: level_dict[x])
d_weights['strength'] = d_weights['strength'].map(lambda x: stick_dict[x])
d_weights = d_weights.astype(convert_dict)
d_weights = d_weights[d_weights['level'] == 'L1']
d_weights = d_weights.rename(columns={'strength': 'speaker trial'})

data = d_weights[d_weights['speaker trial'] == 'less strong evidence first']['val'].to_numpy()
weights = d_weights[d_weights['speaker trial'] == 'less strong evidence first']['prob'].to_numpy()

kern = gaussian_kde(data, weights=weights)

print('less strong evidence first J1 prior density\n')
print(minimize(lambda x: -kern.logpdf(x), 0.1))

data = d_weights[d_weights['speaker trial'] == 'strongest evidence first']['val'].to_numpy()
weights = d_weights[d_weights['speaker trial'] == 'strongest evidence first']['prob'].to_numpy()

kern = gaussian_kde(data, weights=weights)

print('strongest evidence first J1 prior density\n')
print(minimize(lambda x: -kern.logpdf(x), 1.0))

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

sns.kdeplot(data=d_weights, hue='speaker trial', x='val', weights='prob')
plt.xlabel('Value')
plt.ylabel('Prior Density Over $L_1$')
plt.savefig('../output/level_prior_plots.pdf', backend='pdf')

plt.clf()
