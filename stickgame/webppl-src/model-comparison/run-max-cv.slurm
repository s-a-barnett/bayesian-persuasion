#!/bin/bash
#SBATCH --job-name=all-models-mc-max
#SBATCH --output=slurm-%A.%a.out # STDOUT file
#SBATCH --error=slurm-%A.%a.err  # STDERR file
#SBATCH --nodes=1
#SBATCH --ntasks=1
#SBATCH --cpus-per-task=1
#SBATCH --mem-per-cpu=4G
#SBATCH --time=01:02:00
#SBATCH --array=0-49
#SBATCH --mail-type=begin        # send email when job begins
#SBATCH --mail-type=end          # send email when job ends
#SBATCH --mail-user=samuelab@princeton.edu

# Load Python
module load anaconda3

# Change to current directory
cd /home/samuelab/bayesian-persuasion/stickgame/webppl-src/model-comparison/

# Create scratch and tigress directories to record results
mkdir -p /tigress/samuelab/bper/model-comparison/cv/results/

# 5 models, 10 folds
num_model=$(($SLURM_ARRAY_TASK_ID/10))
num_fold=$(($SLURM_ARRAY_TASK_ID%10))
# model numbering from 1 to 9, zero-indexing elsewhere
(( num_model++ ))

while IFS="," read -r model
do
    srun sh write-test-score.sh -m $model -f $num_fold -i /tigress/samuelab/bper/model-comparison/cv/results/ 
done < <(cut -d "," -f$num_model het-model-list.csv)
