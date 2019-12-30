#!/bin/bash
# Purpose: Run a selection of experiments in sequence
for number in {0..299}
do
printf -v numExp "%05d" $number
echo 'running experiment' $numExp'...'
bash persuasion.sh $numExp
done

python results-analysis.py
exit 0
