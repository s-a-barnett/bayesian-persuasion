import pandas as pd
import argparse
import json

def get_mle_table(loc, model, experiment, num_folds=10):
    d = pd.concat([
        pd.json_normalize(json.loads(get_params_json(loc, model, i, experiment))) \
        for i in range(num_folds)
    ])

    return d

def get_params_json(loc, model, fold, experiment):
    if fold is None:
        fold = 'undefined'
    else:
        fold = fold

    num_chains = 40 if model == 'rsa-hom' else 4
    posterior_ = [
        f'{loc}/{model}-params-posterior_c{i}f{fold}{experiment}.csv' for i in range(num_chains)
    ]

    df = pd.concat([pd.read_csv(posterior_[i], delimiter=' ') for i in range(num_chains)])
    d1 = df[list(df.columns)[0]].str.rsplit(pat=',', n=1, expand=True)
    d2 = d1[0].str.split(pat=',', n=1, expand=True)

    scores = d2[d2[0]=='score'][1].astype(float)

    params_json = d2.iloc[scores.idxmax()+1].values[1]

    return params_json

def main(args):

    params_json = get_params_json(args.input, args.model, args.fold, args.experiment)
    print(params_json)

    return 0

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("-m", "--model", type=str, help="name of model")
    parser.add_argument("-f", "--fold", type=int, help="fold number")
    parser.add_argument("-i", "--input", type=str, default="./output/", help="location of input files")
    parser.add_argument("-e", "--experiment", type=str, default="original", help="original or replication")
    args = parser.parse_args()
    main(args)
