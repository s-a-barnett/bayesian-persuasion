import numpy as np
import pandas as pd
import argparse

def MAP_params_from_query(d, num_obs):
    # filter out other params
    num_unique = len(d.param.unique())
    num_params = num_unique - num_obs
    d_map = pd.concat([d.iloc[i*num_unique +num_obs:i*num_unique +num_obs+num_params] for i in range(len(d) // num_unique)])

    # add up probs
    d_map = d_map.groupby(['param', 'val']).sum().reset_index()

    # return MAPs
    idx = d_map.groupby(['param'])['prob'].transform(max) == d_map['prob']

    return d_map[idx]

def main(args):
    query = pd.read_csv(args.input + "rsa-het-speakers-params-posterior.csv")
    df_map = MAP_params_from_query(query, args.num_obs).iloc[:3, :]

    levels = ["J0", "J1", "J1"]
    params = ["nSticks", "agentBias", "nSticks"]
    vals   = df_map["val"]
    probs   = df_map["prob"]

    df = pd.DataFrame(
        {
            "level": levels,
            "param": params,
            "val": vals,
            "prob": probs
        }
    ).reset_index()

    df.to_csv(args.output + "map-params.csv")

    return 0

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("-i", "--input", type=str, default="./results/", help="location of input file")
    parser.add_argument("-n", "--num_obs", type=int, default=725, help="number of experiment participants")
    parser.add_argument("-o", "--output", type=str, default="./", help="location of output table")
    args = parser.parse_args()
    main(args)
