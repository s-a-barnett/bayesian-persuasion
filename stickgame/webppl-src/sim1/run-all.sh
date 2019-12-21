#!/bin/bash
for number in {0..107}
do
printf -v numExp "%05d" $number
echo 'running experiment' $numExp'...'
bash persuasion.sh $numExp
done

python results-analysis.py
exit 0
