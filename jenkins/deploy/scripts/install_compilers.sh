#!/bin/bash -l

echo 'Activating Spack'
. $JENKINS/activate_spack.sh

echo 'Installing License'
# If diectory already exists, do nothing
SOURCE_PATH=${SPACK_SDPLOY_INSTALL_PATH}/external/licenses/intel
LICENSE_PATH=${SPACK_INSTALL_PATH}/etc/spack/licenses/intel
if [ ! -d ${LICENSE_PATH} ]; then
    mkdir -p ${LICENSE_PATH}
    cp ${SOURCE_PATH}/USE_SERVER.lic ${LICENSE_PATH}/license.lic
fi

echo "Installing compilers in environment: ${environment}"
spack --env ${environment} install-compilers -s stacks/${STACK_RELEASE}/${STACK_RELEASE}.yaml
