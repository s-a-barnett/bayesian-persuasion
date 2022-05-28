import tqdm
import numpy as np
import pandas as pd
import argparse
from pathlib import Path
import os
from scipy.stats import bootstrap

def bs(x):
    res = bootstrap((x, ), np.mean)
    ci_low = res.confidence_interval.low
    ci_high = res.confidence_interval.high
    ci_se = res.standard_error
    return '_'.join([str(ci_low), str(ci_high), str(ci_se)])

def get_cv_summary_stats(d):
    d_new = d.groupby('model')['score'].apply(bs).str.split('_', expand=True).reset_index()
    d_new.rename(columns=dict(zip(range(3), ['ci_low', 'ci_high', 'standard_error'])), inplace=True)
    d_sum = d.groupby('model')['score'].mean().reset_index().merge(d_new)
    return d_sum

