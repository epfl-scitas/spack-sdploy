#!/bin/bash -l
set -euo pipefail

# Activate spack
. $JENKINS/activate_spack.sh

echo 'Installing Intel license'
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

echo "Looping through all environments:"
for environment in $(yareed -file stacks/common.yaml -key environments); do
    echo "Working on environment ${enviroment}"
    spack readc -s ${STACK_RELEASE} -p ${environment}
    compilers=$(cat compilers-inline.${environment})
    echo "Found compilers ${compilers}"
    spack install ${compilers}
done

echo "Configuring compilers"
while read -r line
do
    spec_path=$(spack location -i ${line})
    spack compiler find --scope system ${spec_path}
done <<< $(cat compilers-perline.${environment})
