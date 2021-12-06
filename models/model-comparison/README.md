# Model comparisons

## Instructions

Run `data/splits.py` to produce different folds of the data for cross-validation.

Run `train.sh` to fit model on train split:

```
sh train.sh -m rsa-het-speakers -s 1000 -b 1000 -l 1 -v false -c 1 -f 1 -o ./
```

Run `test.sh` to test performance on test split:

```
sh test.sh -m rsa-het-speakers -f 1 -i ./output/
```

# Guide to files

* `infer-params.sh`: The main entry-point for running MCMC chains. Produces a `pointScores.csv` file giving the score of each sample generated in the chain, and a `params-posterior.csv` file giving the posterior over the parameters.
* `models/*.wppl`: implement the different models we consider in the model comparison.
* `model-criterion.py`: computes the WAIC and AIC scores of each model using the `pointScores.csv` files.
* `indep_analysis.py`: creates contingency table of different MAP assignments.
* `model-list.csv`: list of models used for analyses.
* `map_params.py`, `mle_params.py`: computes MAP and MLE parameters from posterior csv files.
* `write-test-scores.sh`: use MLE parameters to compute scores on a held-out test set.
* `mas_opt.py`: produces Appendix Fig. S1 showing fits of different directly optimized MAS models 

## Slurm scripts

While it is possible to manually run chains for different models using direct calls to `infer-params.sh`, we implemented a series of scripts to run all folds for all models in parallel. Note that because of the more complex server setup, however, it will be necessary to manually change paths to match your system.

* `run-model-cv.slurm`: used to run experiments to get cross-validation scores. 
* `run-*-pp.slurm`: used to get posterior predictive runs for best RSA and MAS models.
* `run-rsa-het-indep.slurm`: used to run independence analysis for contigency tables.
* `run-model-waic.slurm`: used to run experiments to get WAIC scores of each model.
