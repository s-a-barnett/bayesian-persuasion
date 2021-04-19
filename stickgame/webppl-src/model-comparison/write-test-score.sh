#!/bin/bash

while getopts m:f:i: option
do
  case "${option}"
    in
    m) MODEL=${OPTARG};;
    f) FOLD=${OPTARG};;
    i) INPUT=${OPTARG};;
  esac
done

mleString=$(python mle_params.py -m $MODEL -f $FOLD -i $INPUT)
score=$(webppl $MODEL.wppl --require ../shared-simple --require webppl-csv \
  -- --test true --mleString $mleString --fold $FOLD | head -n 1)

echo $MODEL,$FOLD,$score >> cv-scores.csv
