#!/bin/bash -l
set -euo pipefail

echo 'Activating Python virtual environment'
. ${PYTHON_VIRTUALENV_PATH}/bin/activate

if [ -e ${SPACK_INSTALL_PATH} ]; then
    echo 'Previous installation of Spack detected...'
    cd ${SPACK_INSTALL_PATH}
    git fetch origin
    git checkout $SPACK_RELEASE
else
    echo 'Spack not detected...'
    git clone -b $SPACK_RELEASE https://github.com/spack/spack ${SPACK_INSTALL_PATH}
fi

echo 'Source Spack and show version'
. $SPACK_INSTALL_PATH/share/spack/setup-env.sh
spack --version

echo "Check if there is a previous SPACK_SYSTEM_CONFIG_PATH directory and remove it:"
if [ -e ${SPACK_SYSTEM_CONFIG_PATH} ]; then
    echo 'Previous system config directory found, removing it...'
    rm -r ${SPACK_SYSTEM_CONFIG_PATH}
fi

echo "SPACK_SYSTEM_CONFIG_PATH: ${SPACK_SYSTEM_CONFIG_PATH}"

echo "Add system compiler:"
spack compiler find --scope system

echo "Dsiplay known compilers:"
spack config blame compilers

echo 'Installing Intel license'
# If directory already exists, remove it
# This is done here beacuse it must be done only once !
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
