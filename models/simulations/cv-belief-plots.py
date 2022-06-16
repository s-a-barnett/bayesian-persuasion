import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

for experiment in ['replication']:
    df = pd.read_csv(f'judge-beliefs-{experiment}.csv')
    df['stick'] = df['stick'] * 10

    plt.xticks(np.linspace(start=1, stop=10, num=10))
    plt.yticks(np.linspace(start=0, stop=1.1, num=12))
    plt.xlim(0.5, 9.5)
    plt.xlabel('stick length $u$')
    plt.ylabel('listener beliefs')
    plt.plot([0, 10], [0.5, 0.5], ls='--', color="black")
    sns.lineplot(x='stick', y='belief', data=df, hue='level', err_style="bars", ci=95);
    plt.savefig(f'mle-beliefs-{experiment}.pdf', backend='pdf')
    plt.clf();
