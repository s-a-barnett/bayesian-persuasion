#!/bin/bash
#SBATCH --job-name=job_array_%a
#SBATCH --output=output/job_%a.out
#SBATCH --error=output/job_%a.err
#SBATCH -N 1
#SBATCH -n 1
#SBATCH --array=0-63
#SBATCH -t 05:59:59

# Change to current directory
cd /home/samuelab/bayesian-persuasion/stickgame/webppl-src/sim2/

# Execute script
printf -v numExp "%05d" ${SLURM_ARRAY_TASK_ID}
srun sh run_sim.sh $numExp
