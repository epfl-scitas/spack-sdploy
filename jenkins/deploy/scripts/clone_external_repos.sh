#!/bin/bash -l

echo 'Activating Python virtual environment'
. ${PYTHON_VIRTUALENV_PATH}/bin/activate

echo 'Source Spack'
. $SPACK_INSTALL_PATH/share/spack/setup-env.sh

repo=`yareed -file ${SPACK_SDPLOY_INSTALL_PATH}/stacks/${STACK_RELEASE}/common.yaml -keys extra_repos scitas-external repo`

echo repo

# if [ -e ${SPACK_SDPLOY_INSTALL_PATH} ]; then
#     echo 'Previous installation of spack-sdploy detected, removing...'
#     rm -rf ${SPACK_SDPLOY_INSTALL_PATH}
# fi
# 
# git clone --branch debug https://github.com/epfl-scitas/spack-sdploy ${SPACK_SDPLOY_INSTALL_PATH}
