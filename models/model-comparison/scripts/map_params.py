import numpy as np
import pandas as pd
import argparse
from pathlib import Path
import os

def main(args):
    models = [
        'rsa-het-speakers',
    ]
    for model in models:
        test_path = Path(os.path.join(args.input, f'{model}-params-posterior_c0fundefinedreplication.csv'))
        if test_path.is_file():
            print(f'{model = }')
            for experiment in ['replication']:
                posterior_ = [
                    f'{args.input}/{model}-params-posterior_c{i}fundefined{experiment}.csv' for i in range(4)
                ]

                df = pd.concat([pd.read_csv(posterior_[i], delimiter=' ') for i in range(4)])
                d1 = df[list(df.columns)[0]].str.rsplit(pat=',', n=1, expand=True)
                d2 = d1[0].str.split(pat=',', n=1, expand=True)

                d_pos = pd.DataFrame({'param': d2[0], 'val': d2[1], 'prob': d1[1]})

                # remove irrelevant rows
                d_pos = d_pos[~d_pos['param'].isin(['score', 'params'])]
                d_pos = d_pos[~d_pos.param.str.startswith('p')]

                # rescale probabilities
                d_pos['prob'] = pd.to_numeric(d_pos['prob']) / 4
                
                # add up probs
                d_pos = d_pos.groupby(['param', 'val']).sum().reset_index()

                # return MAPs
                idx = d_pos.groupby(['param'])['prob'].transform(max) == d_pos['prob']

                d_map = d_pos[idx]    

                d_map.to_csv(os.path.join(args.output, f'{model}-{experiment}-map-params.csv'), index=False)

    return 0

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", type=str, default="/scratch/gpfs/samuelab/bper/waic/", help="location of input files")
    parser.add_argument("--output", type=str, default="./output/", help="location of output table")
    args = parser.parse_args()
    main(args)
