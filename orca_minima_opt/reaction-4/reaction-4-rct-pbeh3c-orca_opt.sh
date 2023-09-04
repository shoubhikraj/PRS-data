#!/bin/bash
#$ -cwd
#$ -pe smp 4
#$ -l s_rt=360:00:00
#
export ORIG=$PWD
export SCR=$TMPDIR
export NBOEXE=/usr/local/nbo7/bin/nbo7.i4.exe
module load openmpi4.1.1
cp *.xyz *.hess $SCR
cp reaction-4-rct-pbeh3c-orca_opt.inp $SCR
cd $SCR
/usr/local/orca_5_0_4/orca reaction-4-rct-pbeh3c-orca_opt.inp > $ORIG/reaction-4-rct-pbeh3c-orca_opt.out
rm -f *.tmp
cp -R * $ORIG
rm *.sh.*
