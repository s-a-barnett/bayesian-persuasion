#!/bin/bash
# Purpose: Read Comma Separated CSV File
# ------------------------------------------
for number in $(seq 0.025 0.05 1.025)
do
echo $number
webppl see_judgescore.wppl --require ../shared --require webppl-csv -- --stick $number
done
