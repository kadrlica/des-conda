#!/bin/bash

# Wrapper around `conda install` to work with cvmfs version control.
# This script should be sourced, otherwise cvmfs will complain about running
# processes when the script tries to publish.
#
# Usage:
# source conda_install.sh [options] packages
#
# For help try:
# conda install --help
#
# @author: Alex Drlica-Wagner <kadrlica@fnal.gov>

if [[ "${BASH_SOURCE[0]}" == "${0}" ]]; then
    echo "ERROR: $(basename ${BASH_SOURCE[0]}) must be sourced";
    exit 1
fi

CONDA_DIR=/cvmfs/des.opensciencegrid.org/fnal/anaconda2
export PATH=$CONDA_DIR/bin:$PATH
export CONDA_ENVS_PATH=$CONDA_DIR/envs

# Start the cvmfs transaction
cvmfs_server transaction des.opensciencegrid.org

# Activate the default environment (note: not root)
source activate default

# Perform the installation
conda install $@

# Remove positional parameters for deactivate
set --; source deactivate

# Publishing can take a while due to anaconda's hardlinks
#cd; cvmfs_server publish des.opensciencegrid.org
cd; screen -S publish -dm cvmfs_server publish des.opensciencegrid.org
echo "cvmfs publishing dispatched to screen session..."
sleep 1
screen -ls

echo "Done."