import numpy as np
import pandas as pd
from scipy.stats import chi2_contingency
import argparse

def MAP_levels_from_query(d, num_obs):
    # filter out other params
    num_unique = len(d.param.unique())
    num_params = num_unique - num_obs
    d_map = pd.concat([d.iloc[i*num_unique :i*num_unique +num_obs] for i in range(len(d) // num_unique)])

    # add up probs
    d_map = d_map.groupby(['param', 'val']).sum().reset_index()

    # return MAPs
    idx = d_map.groupby(['param'])['prob'].transform(max) == d_map['prob']

    return d_map[idx]


def main(args):
    query = pd.concat([pd.read_csv(args.input + args.model + "-params-posterior_{}.csv".format(i)) for i in range(4)])
    d_map_levels = MAP_levels_from_query(query, args.num_obs)
    d_map_levels['judgeLevel'] = d_map_levels.val.str[:-2]
    d_map_levels['speakerLevel'] = d_map_levels.val.str[-2:]

    d_js = d_map_levels[['judgeLevel', 'speakerLevel']].value_counts().to_frame().reset_index()
    d_js['freq'] = d_js[0]
    d_contingency = d_js.pivot(index='judgeLevel', columns='speakerLevel', values='freq').fillna(0)

    d_contingency.to_csv(args.output + args.model + "contingency.csv")
    print(chi2_contingency(d_contingency))

    return 0

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("-i", "--input", type=str, default="./results/", help="location of input file")
    parser.add_argument("-n", "--num_obs", type=int, default=725, help="number of experiment participants")
    parser.add_argument("-o", "--output", type=str, default="./", help="location of output table")
    parser.add_argument("-m", "--model", type=str, default="rsa-het-indep", help="name of model")
    args = parser.parse_args()
    main(args)
