#!/bin/bash
# Purpose: Read Comma Separated CSV File
# ------------------------------------------
INPUT=parameters/exp$1.csv
OLDIFS=$IFS
IFS=','
[ ! -f $INPUT ] && { echo "$INPUT file not found"; exit 99; }
while read nSticks statistic liarAlpha alpha
do
	webppl see-s2dist.wppl --require webppl-csv --require ../shared-deceptive \
	-- --liarAlpha $liarAlpha --statistic $statistic \
	--numExp $1 --nSticks $nSticks --alpha $alpha
done < $INPUT
IFS=$OLDIFS
