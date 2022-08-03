#!/bin/bash -l
set -euo pipefail

echo 'Activating Python virtual environment'
. ${PYTHON_VIRTUALENV_PATH}/bin/activate

echo 'Load variables'
. $JENKINS_SCRIPTS_PATH/config.sh

echo JENKINS_SCRIPTS_PATH: $JENKINS_SCRIPTS_PATH
echo STACK_RELEASE: $STACK_RELEASE

export SPACK_SDPLOY_INSTALL_PATH=${STACK_PREFIX}/${SPACK_SDPLOY_PATH}.${VERSION}
echo SPACK_SDPLOY_INSTALL_PATH: $SPACK_SDPLOY_INSTALL_PATH

if [ -e ${SPACK_SDPLOY_INSTALL_PATH} ]; then
    echo 'Previous installation of spack-sdploy detected, removing...'
    rm -rf ${SPACK_SDPLOY_INSTALL_PATH}
fi

git clone https://github.com/epfl-scitas/spack-sdploy ${SPACK_SDPLOY_INSTALL_PATH}
