#!/bin/bash
while getopts s:b:v:l:o: option
do
  case "${option}"
    in
    s) SAMPLES=${OPTARG};;
    b) BURN=${OPTARG};;
    v) VERBOSE=${OPTARG};;
    l) LAG=${OPTARG};;
    o) OUT=${OPTARG};;
  esac
done

webppl rsa-het.wppl --require ../shared-simple --require webppl-csv \
  -- --samples $SAMPLES --burn $BURN --verbose $VERBOSE --lag $LAG --out $OUT
