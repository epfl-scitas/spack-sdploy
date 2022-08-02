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
echo SPACK_RELEASE: $SPACK_RELEASE

export SPACK_INSTALL_PATH=${STACK_PREFIX}/spack.${VERSION}
echo SPACK_INSTALL_PATH: $SPACK_INSTALL_PATH

git clone git@github.com:spack/spack ${SPACK_INSTALL_PATH}
cd ${SPACK_INSTALL_PATH}
git checkout $SPACK_RELEASE
