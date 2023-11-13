#!/bin/sh
#SBATCH -N 1
#SBATCH -n 1
#SBATCH --mem 200
#SBATCH -t 0-24:00
#SBATCH -o slurm.%j.out
#SBATCH -e slurm.%j.err
module load gcc/6.4.0
module load python/3.6.4


pip3 install biosppy



