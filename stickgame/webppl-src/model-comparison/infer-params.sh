#!/bin/bash
while getopts m:s:b:v:l:o:c: option
do
  case "${option}"
    in
    m) MODEL=${OPTARG};;
    s) SAMPLES=${OPTARG};;
    b) BURN=${OPTARG};;
    v) VERBOSE=${OPTARG};;
    l) LAG=${OPTARG};;
    o) OUT=${OPTARG};;
    c) CHAIN=${OPTARG};;
  esac
done

webppl $MODEL.wppl --require ../shared-simple --require webppl-csv \
  -- --samples $SAMPLES --burn $BURN --verbose $VERBOSE --lag $LAG --out $OUT \
  --chain $CHAIN
