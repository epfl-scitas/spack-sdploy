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

JENKINS_SCRIPTS_PATH=jenkins/deploy/scripts
PYTHON_VIRTUALENV_PATH=/home/scitasbuildpr/syrah/py3-env
SPACK_INSTALL_PATH=/home/scitasbuildpr/syrah/spack.v1

# 'Load variables'
#. ${JENKINS_SCRIPTS_PATH}/config.sh

# 'Activating Python virtual environment'
. ${PYTHON_VIRTUALENV_PATH}/bin/activate

export TEST_SPACK_ROOT=`yareed -file stacks/common.yaml -keys spack_root`

# 'Source Spack'
. $SPACK_INSTALL_PATH/share/spack/setup-env.sh

$@
