# Model comparisons

## Instructions

The easiest way to run the full model comparison is to use the
provided shell script to run different chains in parallel:

```
> parallel --bar --colsep ',' "sh ./slurm/run_waic.sh {1} {2} {3} {4} {5} {6} {7}" :::: ../input/hyperparameters.csv
```

## Dependencies

1. install [`webppl`](https://github.com/probmods/webppl):

```
> npm install -g webppl
```

2. install the `shared` webppl package:

```
> cd ../shared/
> npm install
```

3. install the `webppl-csv` webppl package:

```
mkdir -p ~/.webppl
npm install --prefix ~/.webppl webppl-csv
```

# Guide to files

* `models/*.wppl`: implementations of the different models we consider.
* `train.sh`: The main entry-point for running MCMC chains. Produces a `params-posterior.csv` with posterior samples.
* `scripts/model-criterion.py`: computes the WAIC and AIC scores of each model using output
* `scripts/map_params.py`, `scripts/mle_params.py`: computes MAP and MLE parameters from posterior csv files.
* `scripts/posterior_plots.py`: creates visualizations of param posteriors and computes MAP estimates

## Slurm scripts

We also included a slurm script (for bigger jobs), but note that
because of the more complex server-side setup, it will be necessary to manually change paths to match your system.

* `run-waic.slurm`: used to run experiments to get model criterion of each model.
