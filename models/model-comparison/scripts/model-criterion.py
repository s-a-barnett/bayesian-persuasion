import tqdm
import numpy as np
import pandas as pd
import argparse
from scipy.special import logsumexp
from pathlib import Path
import os
import psis

def compute_mc_stats(d):
    num_obs = len(d.gameid.unique())
    S = len(d) // num_obs

    d_numpy = np.stack(d.groupby('gameid')['score'].apply(np.asarray).to_numpy(), axis=1)
    loo, loos, _ = psis.psisloo(d_numpy)
    se_loo = np.sqrt(num_obs * np.var(loos))

    lppd_i = d.groupby('gameid').aggregate(logsumexp).to_numpy() - np.log(S)
    pwaic2_i = d.groupby('gameid').var().to_numpy()
    elppd_waic_i = lppd_i - pwaic2_i

    lppd = np.sum(lppd_i)
    pwaic2 = np.sum(pwaic2_i)
    elppd_waic = -2 * (lppd - pwaic2)
    se_elppd_waic = np.sqrt(num_obs * np.var(elppd_waic_i))

    out = {
        'loo': -loo,
        'se_loo': se_loo,
        'lppd': lppd,
        'pwaic2': pwaic2,
        'elppd_waic': elppd_waic,
        'se_elppd_waic': se_elppd_waic,
    }

    return out

def main(args):

    df_waic = pd.DataFrame(columns=['model', 'experiment', 'lppd', 'pwaic2', 'elppd_waic', 'se_elppd_waic', 'loo', 'se_loo'])

    # models = list(pd.read_csv('./hyperparameters/hyperparameters_waic.csv').model.unique())
    # TODO: base this off of .wppl files
    models = [
        'aa-hom',
        'aa-hom-adding',
        'mas-het-simple',
        'mas-het-simple-adding',
        'mas-het-speakers',
        'mas-het-speakers-adding',
        'mas-hom',
        'mas-hom-adding',
        'rsa-hom', 
        'rsa-het-simple',
        'rsa-het-speakers',
        'rsa-het-speakers-hi',
    ]
    for model in models:
        test_path = Path(os.path.join(args.input, f'{model}-pointScores_c0fundefinedoriginal.csv'))
        if test_path.is_file():
            print(f'{model = }')
            for experiment in ['original', 'replication']:
                num_chains = 100 if model == 'rsa-hom' else 4
                dfs = pd.concat([pd.read_csv(os.path.join(args.input, f'{model}-pointScores_c{i}fundefined{experiment}.csv')) for i in range(num_chains)])
                stats = compute_mc_stats(dfs)
                stats.update({'model': model, 'experiment': experiment})

                df_waic = df_waic.append(stats, ignore_index=True)

    df_waic.to_csv(os.path.join(args.output, "model-criterion-scores.csv"), index=False)

    return 0

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", type=str, default="/scratch/gpfs/samuelab/bper/waic/", help="location of input files")
    parser.add_argument("--output", type=str, default="./output/", help="location of output table")
    args = parser.parse_args()
    main(args)
