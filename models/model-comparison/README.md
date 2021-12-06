# Model comparisons

## Instructions

Run `data/splits.py` to produce different folds of the data for cross-validation.

NB: it will be necessary to change the directory references within these files
so that they are specific to your file storage structure.


# Guide to files

* `*.wppl`: fits model parameters to passed-in data via WebPPL's MCMC. Produces a `pointScores.csv` file giving the score of each sample generated in the chain, and a `params-posterior.csv` file giving the posterior over the parameters.
* `waic.py`, `aic.py`: computes the WAIC and AIC scores of each model using the `pointScores.csv` files.
* `mas_opt.py`: fits different MAS models to data by directly optimizing.
* `indep_analysis.py`: creates contingency table of different MAP assignments.
* `model-list.csv`: list of models used for analyses.
* `map_params.py`, `mle_params.py`: computes MAP and MLE parameters from posterior csv files.
* `infer-params.sh`: main driver for running MCMC chains.
* `write-test-scores.sh`: use MLE parameters to compute scores on a held-out test set.
* `run-model-cv.slurm`, `run-rsa-hom-cv.slurm`: used to run experiments to get cross-validation scores. 
* `run-*-pp.slurm`: used to get posterior predictive runs for best RSA and MAS models.
* `run-rsa-het-indep.slurm`: used to run independence analysis for contigency tables.
* `run-model-waic.slurm`: used to run experiments to get WAIC scores of each model.
