#!/bin/bash
#SBATCH --job-name=rsa-hom-csv
#SBATCH --output=slurm-%A.%a.out # STDOUT file
#SBATCH --error=slurm-%A.%a.err  # STDERR file
#SBATCH --nodes=1
#SBATCH --ntasks=1
#SBATCH --cpus-per-task=1
#SBATCH --mem-per-cpu=4G
#SBATCH --time=71:59:59
#SBATCH --array=0-39
#SBATCH --mail-type=begin        # send email when job begins
#SBATCH --mail-type=end          # send email when job ends
#SBATCH --mail-user=samuelab@princeton.edu

# Load Python
module load anaconda3

# Change to current directory
cd /home/samuelab/bayesian-persuasion/stickgame/webppl-src/model-comparison/

# Create scratch and tigress directories to record results
mkdir -p /tigress/samuelab/bper/model-comparison/cv/results/

# 4 chains, 10 folds
num_fold=$(($SLURM_ARRAY_TASK_ID%10))
num_chain=$(($SLURM_ARRAY_TASK_ID/10))
model=rsa-hom

srun sh infer-params.sh -m $model -s 1000 -b 20000 -l 1999 -v false -o /tigress/samuelab/bper/model-comparison/cv/ -c $num_chain -f $num_fold

# if all the chains have run, compute likelihood of test data
if [[ -f /tigress/samuelab/bper/model-comparison/cv/results/$model-params-posterior_c0f$num_fold.csv && \
      -f /tigress/samuelab/bper/model-comparison/cv/results/$model-params-posterior_c1f$num_fold.csv && \
      -f /tigress/samuelab/bper/model-comparison/cv/results/$model-params-posterior_c2f$num_fold.csv && \
      -f /tigress/samuelab/bper/model-comparison/cv/results/$model-params-posterior_c3f$num_fold.csv ]]; then
      srun sh write-test-score.sh -m $model -f $num_fold -i /tigress/samuelab/bper/model-comparison/cv/results/
fi
