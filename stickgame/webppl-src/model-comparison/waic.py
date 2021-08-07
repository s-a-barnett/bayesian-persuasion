import numpy as np
import pandas as pd
import argparse
from scipy.special import logsumexp

def compute_pwaic2(d):
    return d[['gameid', 'score']].groupby(['gameid']).var().sum().score

def compute_lppd(d):
    score = d[['gameid', 'score']].groupby(['gameid']).aggregate(logsumexp).sum().score
    num_obs = len(d.gameid.unique()); S = len(d) // num_obs
    return score - (num_obs * np.log(S))

def compute_elppd_waic(d):
    lppd = compute_lppd(d)
    pwaic2 = compute_pwaic2(d)
    return -2 * (lppd - pwaic2)

def main(args):

    models = np.loadtxt("./model-list.csv", dtype=str, delimiter=",")

    if args.verbose:
        print("importing data...")
    # dfs = [pd.read_csv(args.input + model + "-pointScores.csv") for model in models]
    dfs = [pd.concat([pd.read_csv(args.input + model + "-pointScores_c{}ftrue.csv".format(i)) for i in range(4)]) for model in models]

    if args.verbose:
        print("computing lppds...")
    lppds = list(map(compute_lppd, dfs))
    if args.verbose:
        print("computing pwaic2s...")
    pwaic2s = list(map(compute_pwaic2, dfs))

    df_waic = pd.DataFrame(
        {
            "model": models,
            "lppd": lppds,
            "pwaic2": pwaic2s,
            "elppd-waic": -2 * (np.asarray(lppds) - np.asarray(pwaic2s))
        }
    )

    df_waic.to_csv(args.output + "waic-scores.csv")

    if args.verbose:
        print("computation complete \n \n")
        print(df_waic)

    return 0

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("-i", "--input", type=str, default="./results/", help="location of input files")
    parser.add_argument("-o", "--output", type=str, default="./", help="location of output table")
    parser.add_argument("-v", "--verbose", action="store_true", default=True)
    args = parser.parse_args()
    main(args)
