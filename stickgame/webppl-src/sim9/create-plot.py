import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
plt.close('all')

df = pd.read_csv('results-summary.csv')

g = sns.FacetGrid(df, col="stick1", row="judge", hue="recencyBias")
g.map(plt.plot, "stick2", "p_isLong_2")
g.set_axis_labels("agent 2 stick length", "absolute belief");
g.add_legend();
for ax in g.axes.flat:
    ax.plot((0.0, 0.5), (0.5, 0.5), c=".2", ls="--")

g.savefig('absolute-plot.png')
