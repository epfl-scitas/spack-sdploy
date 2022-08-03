#!/bin/bash -l
set -euo pipefail

# This script assumes that the following variables are set in the environment:
#
# PYTHON_VIRTUALENV_PATH: path where to setup the Python virtual environment
# SPACK_INSTALL_PATH
#

echo 'Activating Python virtual environment'
. ${PYTHON_VIRTUALENV_PATH}/bin/activate

echo 'Load variables'
. $JENKINS_SCRIPTS_PATH/config.sh

echo JENKINS_SCRIPTS_PATH: $JENKINS_SCRIPTS_PATH
echo STACK_RELEASE: $STACK_RELEASE

export SPACK_SDPLOY_INSTALL_PATH=${STACK_PREFIX}/${SPACK_SDPLOY_PATH}.${VERSION}
echo SPACK_SDPLOY_INSTALL_PATH: $SPACK_SDPLOY_INSTALL_PATH

git clone https://github.com/epfl-scitas/spack-sdploy ${SPACK_SDPLOY_INSTALL_PATH}
