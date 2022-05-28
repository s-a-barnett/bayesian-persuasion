import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

for experiment in ['original', 'replication']:
    df = pd.read_csv(f'judge-beliefs-{experiment}.csv')
    df['stick'] = df['stick'] * 10

    plt.xticks(np.linspace(start=1, stop=10, num=10))
    plt.yticks(np.linspace(start=0, stop=1.1, num=12))
    plt.plot([0, 10], [0.5, 0.5], ls='--', color="white")
    sns.lineplot(x='stick', y='belief', data=df, hue='level', err_style="bars", ci=95);
    plt.savefig(f'mle-beliefs-{experiment}.png')
