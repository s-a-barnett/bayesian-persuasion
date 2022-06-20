#!/bin/bash#
# parallel --bar --colsep ',' "sh ./run_waic.sh {1} {2} {3} {4} {5} {6} {7}" :::: ../input/hyperparameters.csv
webppl ./models/$1.wppl --random-seed $6 --require ../shared --require webppl-csv -- --samples $2 --burn $3 --lag $4 --verbose $5 --chain $6 --experiment $7 --out ./output/

