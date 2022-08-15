#!/bin/bash -l

# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
#                                                                             #
# SCITAS STACK DEPLOYMENT 2022, EPFL                                          #
#                                                                             #
# This is a conveinience script that loads importante environment variables,  #
# activates the Python environment and sets up Spack. In the end, it will     #
# just run the command that it was given to as parameter.                     #
#                                                                             #
#                                                                             #
#                                                                             #
#                                                                             #
#                                                                             #
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

PYTHON_VIRTUALENV_PATH=/home/scitasbuildpr/syrah/py3-venv
SPACK_INSTALL_PATH=/home/scitasbuildpr/syrah/spack.v1

# 'Activating Python virtual environment'
. ${PYTHON_VIRTUALENV_PATH}/bin/activate

# 'Source Spack'
. $SPACK_INSTALL_PATH/share/spack/setup-env.sh

$@
