import numpy as np
import pandas as pd
import os

output_file = 'hyperparameters_pp.csv'
real_path = os.path.realpath(__file__)
dir_path = os.path.dirname(real_path)

hyp_dict = {
    'model': [
        # 'aa-hom-adding',
        # 'aa-hom',
        # 'mas-het-simple-adding',
        # 'mas-het-simple',
        # 'mas-het-speakers-adding',
        # 'mas-het-speakers',
        # 'mas-hom-adding',
        # 'mas-hom',
        # 'rsa-het-simple',
        # 'rsa-het-speakers-hi',
        # 'rsa-het-speakers',
        # 'rsa-hom',
        'rsa-pp',
        'mas-pp-het-simple',
        'mas-pp-hom',
        # 'mas-pp',
        # 'mas-pp-adding',
    ],
    'samples': [
        # 100, # rsa-hom cv or waic
        1000, # cross-validation and posterior predictive
        # 250, # rsa-hom waic
        # 2500, # waic and psis-loo
    ],
    'burn': [7500],
    'lag': [100],
    'verbose': ['false'],
    'chain': list(range(4)), # 40 for rsa-hom cv, 100 for rsa-hom waic, 4 otherwise
    # 'fold': list(range(10)), # cross-validation only
    'experiment': [
        # 'original', 
        'replication',
    ],
}

index = pd.MultiIndex.from_product(hyp_dict.values(), names=hyp_dict.keys())
df = pd.DataFrame(index = index).reset_index()
print(f'number of unique hyperparameter settings: {len(df)}')
df.to_csv(os.path.join(dir_path, output_file), index=False)
