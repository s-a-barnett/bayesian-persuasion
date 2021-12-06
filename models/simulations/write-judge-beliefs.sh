#!/bin/bash
MODEL=rsa-het-speakers-hi
INPUT=/tigress/samuelab/bper/model-comparison/cv/results/
for FOLD in {0..9}
do
	echo $FOLD
	mleString=$(python ../model-comparison/mle_params.py -m $MODEL -f $FOLD -i $INPUT)
	webppl judge.wppl --require ../shared -- --mleString $mleString | head -n 33 >> judge-beliefs.csv
done
exit 0
