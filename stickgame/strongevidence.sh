#!/bin/bash
# Purpose: Read Comma Separated CSV File
# ------------------------------------------
INPUT=data/test_parameters.csv
OLDIFS=$IFS
IFS=','
[ ! -f $INPUT ] && { echo "$INPUT file not found"; exit 99; }
while read nSticks agentBiased
do
	webppl persuasion.wppl --require webppl-csv -- --nSticks $nSticks --agentBiased $agentBiased
done < $INPUT
IFS=$OLDIFS
