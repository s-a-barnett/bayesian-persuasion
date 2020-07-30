#!/bin/bash
# Purpose: Read Comma Separated CSV File
# ------------------------------------------
INPUT=parameters/exp$1.csv
OLDIFS=$IFS
IFS=','
[ ! -f $INPUT ] && { echo "$INPUT file not found"; exit 99; }
while read biasPrior statistic biasPenalty
do
	webppl see-judgescore.wppl --require webppl-csv --require ../shared \
	-- --biasPrior $biasPrior --statistic $statistic \
	--numExp $1 --biasPenalty $biasPenalty
done < $INPUT
IFS=$OLDIFS
