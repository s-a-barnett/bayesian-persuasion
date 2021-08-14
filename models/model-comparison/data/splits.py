import numpy as np
import pandas as pd
import os
from sklearn.model_selection import StratifiedKFold

dirpath = os.path.dirname(os.path.abspath(__file__))
df = pd.read_csv(dirpath + '/rsa-het-data.csv')

skf = StratifiedKFold(n_splits=10, shuffle=True, random_state=0)

# stratify using the speaker stick choice as a target label
splits = skf.split(np.zeros(len(df)), (10 * df.to_numpy()[:, 3]).astype(int))

fold = 0
for train_index, test_index in splits:
    df.iloc[train_index].to_csv(dirpath + f'/data_train_{fold}.csv', index=False)
    df.iloc[test_index].to_csv(dirpath + f'/data_test_{fold}.csv', index=False)
    fold += 1
