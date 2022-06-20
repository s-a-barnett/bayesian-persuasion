import numpy as np
import pandas as pd
import os

output_file = 'hyperparameters.csv'
real_path = os.path.realpath(__file__)
dir_path = os.path.dirname(real_path)

hyp_dict = {
    'model': [
        'aa-hom',
        'mas-hom',
        'mas-het',
        'rsa-hom',
        'rsa-het',
        'rsa-het-speakers',
        'rsa-het-speakers-hi',
    ],
    'samples': [1000],
    'burn': [7500],
    'lag': [100],
    'verbose': ['false'],
    'chain': list(range(6)),
    'experiment': ['replication']
}

index = pd.MultiIndex.from_product(hyp_dict.values(), names=hyp_dict.keys())
df = pd.DataFrame(index = index).reset_index()
print(f'number of unique hyperparameter settings: {len(df)}')
df.to_csv(os.path.join(dir_path, output_file), index=False)
