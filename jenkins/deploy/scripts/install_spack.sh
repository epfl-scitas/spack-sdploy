#!/bin/bash -l
set -euo pipefail

echo 'Activating Python virtual environment'
. ${PYTHON_VIRTUALENV_PATH}/bin/activate

echo 'Load variables'
. $JENKINS_SCRIPTS_PATH/config.sh

#export SPACK_INSTALL_PATH=${STACK_PREFIX}/spack.${VERSION}
#echo SPACK_INSTALL_PATH: $SPACK_INSTALL_PATH

if [ -e ${SPACK_INSTALL_PATH} ]; then
    echo 'Previous installation of Spack detected, removing...'
    rm -rf ${SPACK_INSTALL_PATH}
fi

git clone -b $SPACK_RELEASE --single-branch https://github.com/spack/spack ${SPACK_INSTALL_PATH}
