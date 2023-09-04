#!/bin/bash
#$ -cwd
#$ -pe smp 8
#$ -l s_rt=360:00:00
#
export ORIG=$PWD
export SCR=$TMPDIR
export NBOEXE=/usr/local/nbo7/bin/nbo7.i4.exe
module load openmpi4.1.1
cp *.xyz *.hess $SCR
cp reaction4-IEIP_ts_guess_scan_5-4_orca.inp $SCR
cd $SCR
/usr/local/orca_5_0_4/orca reaction4-IEIP_ts_guess_scan_5-4_orca.inp > $ORIG/reaction4-IEIP_ts_guess_scan_5-4_orca.out
rm -f *.tmp
cp -R * $ORIG
rm *.sh.*
