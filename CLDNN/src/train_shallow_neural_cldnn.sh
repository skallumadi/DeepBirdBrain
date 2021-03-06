#!/bin/sh

# Directives
#PBS -N CLDNN_PR_SHALLOW
#PBS -W group_list=yetistats
#PBS -l walltime=72:00:00,mem=7gb
#PBS -M sl3368@columbia.edu
#PBS -m a
#PBS -V

# Set output and error directories
#PBS -o localhost:/vega/stats/users/sl3368/CLDNN/logs/neural/
#PBS -e localhost:/vega/stats/users/sl3368/CLDNN/logs/neural/

module load anaconda/2.7.8
module load cuda/6.5

python neural_shallow_cldnn.py $REGION $HELDOUT


#END OF SCRIPT
