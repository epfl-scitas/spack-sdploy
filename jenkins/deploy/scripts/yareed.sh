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

# 'Activating Python virtual environment'
echo "PYTHON_VIRTUALENV_PATH: ${PYTHON_VIRTUALENV_PATH}"
. ${PYTHON_VIRTUALENV_PATH}/bin/activate

$@
