#!/bin/sh
#SBATCH -N 1
#SBATCH -n 1
#SBATCH --mem 30000
#SBATCH -t 0-24:00
#SBATCH -o slurm.%j.out
#SBATCH -e slurm.%j.err
module load gcc/9.2.0 openmpi/4.0.2
module load python/3.7.4
module load numpy/1.19.2-python-3.7.4
module load scipy/1.6.0-python-3.7.4
module load pandas/1.0.5-python-3.7.4
module load matplotlib/3.2.1-python-3.7.4

python3 QLD0227forecastECGauto.py