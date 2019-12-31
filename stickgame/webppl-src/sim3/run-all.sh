#!/bin/bash
# Purpose: Run a selection of experiments in sequence
for number in {0..150}
do
printf -v numExp "%05d" $number
bash run_sim.sh $numExp
done

python results-analysis.py
exit 0
