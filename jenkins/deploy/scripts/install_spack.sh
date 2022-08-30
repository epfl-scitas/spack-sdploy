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

if [ -e ${SPACK_SYSTEM_CONFIG_PATH} ]; then
    echo 'Previous system config directory...'
    rm -r ${SPACK_SYSTEM_CONFIG_PATH}
fi

echo "spack compiler find --scope system:"
spack compiler find --scope system

echo "spack config blame compiler:"
spack config blame compilers
