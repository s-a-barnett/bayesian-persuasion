#!/bin/bash
# Purpose: Read Comma Separated CSV File
# ------------------------------------------
INPUT=parameters/exp$1.csv
OLDIFS=$IFS
IFS=','
[ ! -f $INPUT ] && { echo "$INPUT file not found"; exit 99; }
while read agent0stick fixedBiasAgent nSticks
do
	webppl wee-plots.wppl --require webppl-csv --require ../shared \
	-- --agent0stick $agent0stick \
	--numExp $1 --fixedBiasAgent $fixedBiasAgent --nSticks $nSticks
done < $INPUT
IFS=$OLDIFS
