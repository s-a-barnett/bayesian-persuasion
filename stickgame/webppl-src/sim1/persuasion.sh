#!/bin/bash
# Purpose: Read Comma Separated CSV File
# ------------------------------------------
INPUT=data/se_parameters.csv
OLDIFS=$IFS
IFS=','
[ ! -f $INPUT ] && { echo "$INPUT file not found"; exit 99; }
while read nSticks agent0stick agent1stick
do
	webppl persuasion.wppl --require webppl-csv -- --nSticks $nSticks --agent0stick $agent0stick --agent1stick $agent1stick
done < $INPUT
IFS=$OLDIFS
