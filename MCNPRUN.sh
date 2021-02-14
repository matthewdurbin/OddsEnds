#!/bin/bash
#PBS -l nodes=1:ppn=1
#PBS -j oe
#PBS -N artest.mpi
#PBS -A open
#PBS -r n
#PBS -l walltime=5:00

THIS_HOST=$(hostname --short)
DATE=$(date)

# This job's working directory
echo Job ID: $PBS_JOBID
echo Working directory is $PBS_O_WORKDIR

echo Running on host ${THIS_HOST}
echo Time is ${DATE}
echo Directory is $(pwd)
# echo This job runs on the following processors:
# echo $(cat $PBS_NODEFILE)
cat /proc/cpuinfo | grep 'name'

#Define number of processors
NPROCS=$(wc -l < $PBS_NODEFILE)
echo This job has allocated $NPROCS processors.

# How many nodes?
NHOSTS=$(( ${NPROCS} / ${PPN} ))
echo This job has allocated ${NHOSTS} nodes.

#####################################
# For an individual MCNP run
#####################################
# MCNP data path
#export DATAPATH="/path/to/MCNP_DATA"

# Set the full (or relative) path to your executable
#MYPROG="/path/to/executable"

# load modules
#module load "gcc"

# Run the parallel MPI executable "cpi" using mpiexec
# MYPROG_CMD="${MYPROG} i=INPUT.txt o=OUTPUT tasks 20"

# echo "Done"

#####################################
# For an AutoMateCNP run
#####################################
# load modules
module purge
module load python/3.6.3-anaconda5.0.1
module load "gcc"

cd $PBS_O_WORKDIR

python AutoMateCNP.py

echo "Done"
