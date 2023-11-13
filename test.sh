#!/bin/sh
#SBATCH -N 1
#SBATCH -n 1
#SBATCH --mem 200
#SBATCH -t 0-10:00
#SBATCH -o slurm.%j.out
#SBATCH -e slurm.%j.err
module load gcc/6.4.0
module load python/3.6.4
module load numpy/1.16.3-python-3.6.4
module load scipy/1.3.0-python-3.6.4
module load matplotlib/2.2.2-python-3.6.4

python3 Seerday1p1cri.py
