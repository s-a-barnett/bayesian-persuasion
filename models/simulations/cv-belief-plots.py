import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
%matplotlib inline

df = pd.read_csv('judge-beliefs.csv')
df['stick'] = df['stick'] * 10

plt.xticks(np.linspace(start=0, stop=11, num=12))
plt.yticks(np.linspace(start=0, stop=1.1, num=12))
plt.plot([0, 10], [0.5, 0.5], ls='--', color="white")
sns.lineplot(x='stick', y='belief', data=df, hue='level', err_style="bars", ci=95);
plt.savefig('mle-beliefs.png')
