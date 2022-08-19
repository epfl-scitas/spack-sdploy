#!/bin/bash -l

echo 'Activating Spack'
. $JENKINS/activate_spack.sh

echo 'Installing License'
# If directory already exists, remove it
SOURCE_PATH=${SPACK_SDPLOY_INSTALL_PATH}/external/licenses/intel
LICENSE_PATH=${SPACK_INSTALL_PATH}/etc/spack/licenses/intel
if [ ! -d ${LICENSE_PATH} ]; then
    mkdir -p ${LICENSE_PATH}
    cp ${SOURCE_PATH}/USE_SERVER.lic ${LICENSE_PATH}/license.lic
else
    rm -r ${LICENSE_PATH}
    mkdir -p ${LICENSE_PATH}
    cp ${SOURCE_PATH}/USE_SERVER.lic ${LICENSE_PATH}/license.lic
fi

echo "Installing compilers in environment: ${environment}"
spack --env ${environment} install-compilers -s ${STACK_RELEASE} -p ${environment}

echo 'Create modules for newly installed compilers'
spack --env ${environment} module lmod refresh -y ${SPACK_SYSTEM_CONFIG_PATH}/compilers.list

echo "Add newly installed compilers in environment: ${environment}"
spack --env ${environment} compiler find
