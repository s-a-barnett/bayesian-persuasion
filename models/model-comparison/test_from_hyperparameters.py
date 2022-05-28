import os
import sys
import pandas as pd
from pathlib import Path
import numpy as np

hyp_file = sys.argv[1]
idx = int(sys.argv[2])
out = sys.argv[3]
df = pd.read_csv(hyp_file)
if idx < len(df):
    # check params-posterior file exists for all four chains
    hyperparameters = df.iloc[idx]
    model = hyperparameters['model']
    fold = hyperparameters['fold']
    experiment = hyperparameters['experiment']
    num_chains = 40 if model == 'rsa-hom' else 4

    paths = [
        os.path.join(out, f'{model}-params-posterior_c{i}f{fold}{experiment}.csv') for i in range(num_chains)
    ]

    all_paths_exist = np.all([Path(path).is_file() for path in paths])

    if all_paths_exist:
        script = f'sh test.sh '
        script += f'-m {model} '
        script += f'-f {fold} '
        script += f'-e {experiment} '
        script += f'-i {out}'
        
        os.system(script) 
