#!/bin/bash
while getopts s:b:v: option
do
  case "${option}"
    in
    s) SAMPLES=${OPTARG};;
    b) BURN=${OPTARG};;
    v) VERBOSE=${OPTARG};;
  esac
done

webppl rsa-hom.wppl --require ../shared-simple --require webppl-csv \
  -- --samples $SAMPLES --burn $BURN --verbose $VERBOSE 
