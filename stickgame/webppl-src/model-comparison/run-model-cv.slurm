#!/bin/bash
#SBATCH --job-name=all-models-mc
#SBATCH --output=slurm-%A.%a.out # STDOUT file
#SBATCH --error=slurm-%A.%a.err  # STDERR file
#SBATCH --nodes=1
#SBATCH --ntasks=1
#SBATCH --cpus-per-task=1
#SBATCH --mem-per-cpu=4G
#SBATCH --time=23:59:59
#SBATCH --array=0-269
#SBATCH --mail-type=begin        # send email when job begins
#SBATCH --mail-type=end          # send email when job ends
#SBATCH --mail-user=samuelab@princeton.edu

# Change to current directory
cd /home/samuelab/bayesian-persuasion/stickgame/webppl-src/model-comparison/

# Create scratch and tigress directories to record results
mkdir -p /tigress/samuelab/bper/model-comparison/results/

# 9 models, 3 chains, 10 folds
num_fold=$(($SLURM_ARRAY_TASK_ID%10))
num_chain=$(((((($SLURM_ARRAY_TASK_ID - $num_fold)) / 10))%3))
num_model=$(($SLURM_ARRAY_TASK_ID/30))
# model numbering from 1 to 9, zero-indexing elsewhere
(( num_model++ ))

while IFS="," read -r model
do
    srun sh infer-params.sh -m $model -s 2500 -b 20000 -l 1999 -v false -o /tigress/samuelab/bper/model-comparison/ -c $num_chain

    # if all the chains have run, compute likelihood of test data
    if [[ -f /tigress/samuelab/bper/model-comparison/results/$model-params-posterior_0.csv && \
          -f /tigress/samuelab/bper/model-comparison/results/$model-params-posterior_1.csv &&  \
          -f /tigress/samuelab/bper/model-comparison/results/$model-params-posterior_2.csv ]]; then
          bash write-test-score.sh -m $model -f $num_fold -i /tigress/samuelab/bper/model-comparison/results/
    fi
done < <(cut -d "," -f$num_model model-list.csv)
