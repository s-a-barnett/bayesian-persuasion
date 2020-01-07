#!/bin/bash
# Purpose: Read Comma Separated CSV File
# ------------------------------------------
INPUT=parameters/exp$1.csv
OLDIFS=$IFS
IFS=','
[ ! -f $INPUT ] && { echo "$INPUT file not found"; exit 99; }
while read nSticks stick biasPrior
do
	webppl see_judge.wppl --require webppl-csv --require ../shared \
	-- --nSticks $nSticks --stick $stick --biasPrior $biasPrior --numExp $1
done < $INPUT
IFS=$OLDIFS
