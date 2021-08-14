# Reproducing model simulations and comparison fits

## Model comparisons
Use the `.slurm` files in `model-comparison/` for producing model comparisons
and fits to data: refer to the README within the folder for descriptions of
each file. Run `model-comparison/data/splits.py` to produce the folds of the
data for cross-validation scores.

NB: it will be necessary to change the directory references within these files
so that they are specific to your file storage structure.

## Model simulations
For the visualizations of the RSA model, use the `.py` scripts in `judge-beliefs/`
and `basic-model/`. Refer to the READMEs in these folders for further details.
