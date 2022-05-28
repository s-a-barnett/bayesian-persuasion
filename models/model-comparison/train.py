import os
import sys
import pandas as pd

hyp_file = sys.argv[1]
idx = int(sys.argv[2])
out = sys.argv[3]
df = pd.read_csv(hyp_file)
if idx < len(df):
    hyperparameters = df.iloc[idx]
    model = hyperparameters['model']
    script = f'webppl models/{model}.wppl --random-seed {hyperparameters["chain"]} --require ../shared --require webppl-csv -- '
    script += ' '.join([f'--{key} {hyperparameters[key]}' for key in df.columns if key != 'model'])
    script += f' --out {out}'
    
    os.system(script) 
