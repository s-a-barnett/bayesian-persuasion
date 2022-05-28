#!/bin/bash
MODEL=rsa-het-speakers
INPUT=/scratch/gpfs/samuelab/bper/cv/
for FOLD in {0..9}
do
    for EXPERIMENT in original replication
    do
        echo $FOLD
        mleString=$(python ../model-comparison/scripts/mle_params.py -m $MODEL -f $FOLD -i $INPUT -e $EXPERIMENT)
        webppl judge.wppl --require ../shared -- --mleString $mleString | head -n 18 >> judge-beliefs-$EXPERIMENT.csv
    done
done
exit 0
