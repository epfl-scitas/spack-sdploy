#!/bin/bash -l
set -euo pipefail

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
spack install-compilers -s ${STACK_RELEASE} -p ${environment}

echo "Adding stack compilers"
spack --env ${environment} add-compilers find -s ${STACK_RELEASE} --scope system

echo "Adding system compiler"
spack --env ${environment} compilers find --scope system

sed -i 's/intel@19.1.3.304/intel@20.0.4/' ${SPACK_SYSTEM_CONFIG_PATH}/compilers.yaml
