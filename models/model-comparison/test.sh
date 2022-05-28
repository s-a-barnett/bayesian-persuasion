#!/bin/bash

while getopts m:f:i:t:x:e: option
do
  case "${option}"
    in
    m) MODEL=${OPTARG};;
    f) FOLD=${OPTARG};;
    i) INPUT=${OPTARG};;
    t) TESTSAMPLES=${OPTARG};;
    x) MAXSCORE=${OPTARG};;
    e) EXPERIMENT=${OPTARG};;
  esac
done

mleString=$(python scripts/mle_params.py -m $MODEL -f $FOLD -i $INPUT -e $EXPERIMENT)
score=$(webppl models/$MODEL.wppl --require ../shared --require webppl-csv \
  -- --test true --experiment $EXPERIMENT --mleString $mleString --fold $FOLD --testSamples $TESTSAMPLES --maxScore $MAXSCORE \
  | head -n 1)

echo $MODEL,$FOLD,$score >> $INPUT/$EXPERIMENT-cv-scores.csv
