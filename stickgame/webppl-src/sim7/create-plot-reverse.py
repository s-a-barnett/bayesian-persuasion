import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

plt.close();

df0 = pd.read_csv('results/posterior-bias0-reverse.csv')
df2 = pd.read_csv('results/posterior-bias2-reverse.csv')
df5 = pd.read_csv('results/posterior-bias5-reverse.csv')
df10 = pd.read_csv('results/posterior-bias10-reverse.csv')
df = pd.concat([df0, df2, df5, df10])

df['stick3'] = 3*df['stat'] - 1

df_pos = df[df['prob'] != 0.]

ax = sns.lineplot(x="stick3", y="prob", hue="bias0", data=df_pos, legend='full');
plt.ylabel('p(stick3 | stick1, stick2)');
plt.yticks([]);
plt.title('Posterior Belief over Length of Third Stick');
plt.plot([0.175, 0.175], [0, 0.09], 'k-', lw=1, dashes=[2,2]);
plt.plot([0.825, 0.825], [0, 0.09], 'k-', lw=1, dashes=[2,2]);
fig = ax.get_figure();
fig.savefig('posterior-plot-reverse.png');
