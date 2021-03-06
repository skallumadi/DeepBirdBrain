#!/bin/sh

# Directives
#PBS -N LSTM_PR_500
#PBS -W group_list=yetistats
#PBS -l walltime=192:00:00,mem=7gb
#PBS -M sl3368@columbia.edu
#PBS -m a
#PBS -V
#PBS -q long2 

# Set output and error directories
#PBS -o localhost:/vega/stats/users/sl3368/rnn_code/logs/neural/
#PBS -e localhost:/vega/stats/users/sl3368/rnn_code/logs/neural/

module load anaconda/2.7.8
module load cuda/6.5

python neural_1_layer_script.py $REGION $HELDOUT


#END OF SCRIPT
