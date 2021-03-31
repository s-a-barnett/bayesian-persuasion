import numpy as np
import pandas as pd
from sklearn.neighbors import KernelDensity
import matplotlib.pyplot as plt

# df_pp = pd.read_csv("results/cluster/results/rsa-pp-params-posterior.csv")
df_pp = pd.read_csv("results/cluster/results/mas-pp-params-posterior.csv")

gameids = list(df_pp.columns)[:-1]

x_test = np.linspace(0, 1, 100)[:, np.newaxis]
map_predicts = []
for ind in range(len(gameids)):
    gameid = gameids[ind]
    test = df_pp[[gameid, 'prob']].groupby(gameid).sum().reset_index().to_numpy()
    kde = KernelDensity(bandwidth=0.05).fit(np.expand_dims(test[:, 0], axis=1), sample_weight=test[:, 1])
    dens = kde.score_samples(x_test)
    map_predicts.append(x_test[np.argmax(dens)][0])
    if (ind % 50 == 0):
        print(f"iteration {ind} done")

df = pd.DataFrame(
    {
        "gameid": gameids,
        "belief": map_predicts
    }
)

df.to_csv("mas_pp_map_beliefs.csv", index=False)
