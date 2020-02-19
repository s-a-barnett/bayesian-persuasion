#!/bin/bash
#SBATCH --job-name=job_array_%a
#SBATCH --output=output/job_%a.out
#SBATCH --error=output/job_%a.err
#SBATCH -N 1
#SBATCH -n 1
#SBATCH --array=0-49
#SBATCH -t 1:00:01
#SBATCH --mail-type=begin        # send email when job begins
#SBATCH --mail-type=end          # send email when job ends
#SBATCH --mail-user=samuelab@princeton.edu

# Change to current directory
cd /home/samuelab/bayesian-persuasion/stickgame/webppl-src/sim2/
module load anaconda3

numStart=$((20 * ${SLURM_ARRAY_TASK_ID}))
numEnd=$(($numStart + 19))

# Execute script
srun sh run-all.sh $numStart $numEnd

srun python results-analysis.py
