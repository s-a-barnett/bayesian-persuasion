#!/bin/bash
# Purpose: Run a selection of experiments in sequence
numStart=$1
numEnd=$2
for number in $(seq $numStart $numEnd)
do
printf -v numExp "%05d" $number
bash run_sim.sh $numExp
done

exit 0
