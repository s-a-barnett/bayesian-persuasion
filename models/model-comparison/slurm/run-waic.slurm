#!/bin/bash
#SBATCH --job-name=all-models-waic
#SBATCH --output=outputs/slurm-%A.%a.out # STDOUT file
#SBATCH --error=outputs/slurm-%A.%a.err  # STDERR file
#SBATCH --nodes=1
#SBATCH --ntasks=1
#SBATCH --cpus-per-task=1
#SBATCH --mem-per-cpu=4G
#SBATCH --time=23:59:59
#SBATCH --array=0-289
#SBATCH --mail-type=begin        # send email when job begins
#SBATCH --mail-type=end          # send email when job ends
#SBATCH --mail-user=samuelab@princeton.edu

# Change to current directory
cd /home/samuelab/Repos/bayesian-persuasion/models/model-comparison

# Create scratch and tigress directories to record output
out=/scratch/gpfs/samuelab/bper/waic/
mkdir -p $out

ITERS_PER_JOB=1
START=$(( $SLURM_ARRAY_TASK_ID * $ITERS_PER_JOB ))
END=$(( $START + $(($ITERS_PER_JOB - 1)) ))
for i in $(seq $START $END)
do
    srun python train.py hyperparameters/hyperparameters_waic.csv $i $out
done
