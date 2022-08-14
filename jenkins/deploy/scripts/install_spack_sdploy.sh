#!/bin/bash -l

echo 'Activating Python virtual environment'
. ${PYTHON_VIRTUALENV_PATH}/bin/activate

echo 'Load variables'
# . $JENKINS_SCRIPTS_PATH/config.sh

if [ -e ${SPACK_SDPLOY_INSTALL_PATH} ]; then
    echo 'Previous installation of spack-sdploy detected, removing...'
    rm -rf ${SPACK_SDPLOY_INSTALL_PATH}
fi

git clone --branch debug https://github.com/epfl-scitas/spack-sdploy ${SPACK_SDPLOY_INSTALL_PATH}
