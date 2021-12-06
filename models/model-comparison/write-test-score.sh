#!/bin/bash

while getopts m:f:i:t:x: option
do
  case "${option}"
    in
    m) MODEL=${OPTARG};;
    f) FOLD=${OPTARG};;
    i) INPUT=${OPTARG};;
    t) TESTSAMPLES=${OPTARG};;
    x) MAXSCORE=${OPTARG};;
  esac
done

mleString=$(python mle_params.py -m $MODEL -f $FOLD -i $INPUT)
score=$(webppl $MODEL.wppl --require ../shared --require webppl-csv \
  -- --test true --mleString $mleString --fold $FOLD --testSamples $TESTSAMPLES --maxScore $MAXSCORE \
  | head -n 1)

echo $MODEL,$FOLD,$score >> cv-scores.csv
