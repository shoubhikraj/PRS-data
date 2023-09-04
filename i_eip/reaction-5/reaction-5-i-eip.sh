#!/bin/bash
#$ -cwd
#$ -pe smp 4
#$ -l s_rt=360:00:00
export OMP_NUM_THREADS=1
module load openmpi4.1.1
conda activate ade
/u/fd/shug7486/miniconda/envs/ade/bin/python reaction-5-i-eip.py 
