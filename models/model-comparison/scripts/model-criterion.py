import tqdm
import numpy as np
import pandas as pd
import argparse
from scipy.special import logsumexp
from pathlib import Path
import os
import psis
import math

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

    models = [
        'aa-hom',
        'mas-hom',
        'mas-het',
        'rsa-hom', 
        'rsa-het',
        'rsa-het-speakers',
        'rsa-het-speakers-hi',
    ]
    for model in models:
        test_path = Path(os.path.join(args.input, f'{model}-params-posterior_c0replication.csv'))
        print(f'{model}-params-posterior_c0replication.csv', test_path.is_file())
        if test_path.is_file():
            print(f'model = {model}')
            for experiment in ['replication']:
                num_chains = 6
                dfs = pd.concat([pd.read_csv(os.path.join(args.input, f'{model}-params-posterior_c{i}{experiment}.csv'),
                                             on_bad_lines = 'skip') for i in range(num_chains)])
                mle = np.amax(pd.to_numeric(dfs[dfs.param.str.fullmatch("likelihood")]['val'].to_numpy()))

                # Pull out pointwise scores & predictions
                dfs = dfs[dfs.param.str.count("-") == 5].reset_index()
                dfs[['param', 'gameid']] = dfs['param'].str.split('_', expand=True)
                dfs['counts'] = (dfs.prob * 1000).round()
                print(dfs)
                dfs = (dfs.loc[dfs.index.repeat(dfs.counts)]
                       .query('param == "pointscore"')
                       .drop(['param', 'prob','index','counts'], axis=1)
                       .rename(columns={
                           "val" : "score"
                       }))
                dfs['score'] = pd.to_numeric(dfs['score'])
                stats = compute_mc_stats(dfs)
                stats.update({'model': model, 'experiment': experiment, 'mle': mle})
                df_waic = df_waic.append(stats, ignore_index=True)

    df_waic.to_csv(os.path.join(args.output, "model-criterion-scores.csv"), index=False)

    return 0

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", type=str, default="/scratch/gpfs/samuelab/bper/waic/", help="location of input files")
    parser.add_argument("--output", type=str, default="./output/", help="location of output table")
    args = parser.parse_args()
    main(args)
