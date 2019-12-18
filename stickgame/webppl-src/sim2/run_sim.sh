#!/bin/bash
# Purpose: Read Comma Separated CSV File
# ------------------------------------------
INPUT=parameters/exp$1.csv
OLDIFS=$IFS
IFS=','
[ ! -f $INPUT ] && { echo "$INPUT file not found"; exit 99; }
while read nSticks agentBias
do
	webppl see_speaker.wppl --require webppl-csv -- --nSticks $nSticks --agentBias $agentBias --numExp $1
done < $INPUT
IFS=$OLDIFS
