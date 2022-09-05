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

echo "============= COMPILERS DEBUG INFO ============="

echo "SPACK_SYSTEM_CONFIG_PATH: ${SPACK_SYSTEM_CONFIG_PATH}"

echo "spack config blame compilers"
spack config blame compilers

echo "spack compilers"
spack compilers

echo "cat ${SPACK_SYSTEM_CONFIG_PATH}/compilers.yaml:"
cat ${SPACK_SYSTEM_CONFIG_PATH}/compilers.yaml
