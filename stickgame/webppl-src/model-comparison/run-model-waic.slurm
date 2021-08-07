#!/bin/bash
#SBATCH --job-name=all-models-waic
#SBATCH --output=slurm-%A.%a.out # STDOUT file
#SBATCH --error=slurm-%A.%a.err  # STDERR file
#SBATCH --nodes=1
#SBATCH --ntasks=1
#SBATCH --cpus-per-task=1
#SBATCH --mem-per-cpu=4G
#SBATCH --time=71:59:59
#SBATCH --array=0-31
#SBATCH --mail-type=begin        # send email when job begins
#SBATCH --mail-type=end          # send email when job ends
#SBATCH --mail-user=samuelab@princeton.edu

# Change to current directory
cd /home/samuelab/bayesian-persuasion/stickgame/webppl-src/model-comparison/

# Create scratch and tigress directories to record results
mkdir -p /tigress/samuelab/bper/model-comparison/waic/results/

# 4 chains, 8 models
num_model=$(($SLURM_ARRAY_TASK_ID/4))
num_chain=$(($SLURM_ARRAY_TASK_ID%4))
# model numbering from 1 to 8, zero-indexing elsewhere
(( num_model++ ))

while IFS="," read -r model
do
    srun sh infer-params.sh -m $model -s 2500 -b 20000 -l 1999 -v false -o /tigress/samuelab/bper/model-comparison/waic/ -c $num_chain
done < <(cut -d "," -f$num_model model-list.csv)
