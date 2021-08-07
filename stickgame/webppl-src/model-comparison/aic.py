import numpy as np
import pandas as pd
import argparse

def compute_nparams(d):
    if 'shiftMatrix' in d.columns:
        return 401
    if 'param' in d.columns:
        nparams = d.param.unique().size
    else:
        nparams = len(d.columns) -1
    return nparams

def compute_mlescore(d):
    return d.groupby(d.index // 725).sum().max().to_numpy()[0]

def compute_elpd_aic(d_scores, d_params):
    mlescore = compute_mlescore(d_scores)
    nparams  = compute_nparams(d_params)
    return -2 * (mlescore - nparams)

def main(args):

    models = np.loadtxt("./model-list.csv", dtype=str, delimiter=",")

    if args.verbose:
        print("importing data...")
    dfs_params = [pd.read_csv(args.input + model + "-params-posterior_1.csv") for model in models]
    dfs_scores = [pd.concat([pd.read_csv(args.input + model + "-pointScores_{}.csv".format(i)) for i in range(4)]) for model in models]

    if args.verbose:
        print("computing mlescores...")
    mlescores = list(map(compute_mlescore, dfs_scores))
    if args.verbose:
        print("computing nparams...")
    nparamss = list(map(compute_nparams, dfs_params))

    df_aic = pd.DataFrame(
        {
            "model": models,
            "mlescore": mlescores,
            "nparams": nparamss,
            "elpd-aic": -2 * (np.asarray(mlescores) - np.asarray(nparamss))
        }
    )

    df_aic.to_csv(args.output + "aic-scores.csv")

    if args.verbose:
        print("computation complete \n \n")
        print(df_aic)

    return 0

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("-i", "--input", type=str, default="./results/", help="location of input files")
    parser.add_argument("-o", "--output", type=str, default="./", help="location of output table")
    parser.add_argument("-v", "--verbose", action="store_true", default=True)
    args = parser.parse_args()
    main(args)
