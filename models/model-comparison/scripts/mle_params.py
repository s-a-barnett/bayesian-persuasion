import pandas as pd
import argparse

def main(args):
    posterior_ = [f'{args.input}/{args.model}-params-posterior_c{i}f{args.fold}.csv' for i in range(4)]

    df = pd.concat([pd.read_csv(posterior_[i], delimiter=' ') for i in range(4)])
    d1 = df[list(df.columns)[0]].str.rsplit(pat=',', n=1, expand=True)
    d2 = d1[0].str.split(pat=',', n=1, expand=True)

    scores = d2[d2[0]=='score'][1].astype(float)

    params_json = d2.iloc[scores.idxmax()+1].values[1]

    print(params_json)

    return 0

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("-m", "--model", type=str, help="name of model")
    parser.add_argument("-f", "--fold", type=int, help="fold number")
    parser.add_argument("-i", "--input", type=str, default="./output/", help="location of input files")
    args = parser.parse_args()
    main(args)
