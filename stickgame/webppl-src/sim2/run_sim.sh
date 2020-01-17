#!/bin/bash
# Purpose: Read Comma Separated CSV File
# ------------------------------------------
INPUT=parameters/exp$1.csv
OLDIFS=$IFS
IFS=','
[ ! -f $INPUT ] && { echo "$INPUT file not found"; exit 99; }
while read nSticks agentBias biasPrior
do
	webppl see_speaker.wppl --require webppl-csv --require ../shared \
	-- --nSticks $nSticks --agentBias $agentBias --biasPrior $biasPrior --numExp $1
done < $INPUT
IFS=$OLDIFS
