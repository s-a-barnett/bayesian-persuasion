import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
plt.close('all')

df = pd.read_csv('results-summary.csv')

df2 = df[(df['stick1'] != 0.525) & (df['stick1'] != 0.975)]

g = sns.FacetGrid(df2, col="stick1", row="judge", hue="agentBias")
g.map(plt.plot, "stick2", "delta")
g.set_axis_labels("agent 2 stick length", "absolute change in belief");
g.add_legend();
for ax in g.axes.flat:
    ax.plot((0.0, 0.5), (0, 0), c=".2", ls="--")

g.savefig('delta-plots.png')
