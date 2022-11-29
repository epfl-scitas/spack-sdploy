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

if [ ! -d $HOME/.spack-${STACK} ]; then
    mkdir -p $HOME/.spack-${STACK}
fi

export SPACK_USER_CACHE_PATH=$HOME/.spack-${STACK}
export SPACK_USER_CONFIG_PATH=$HOME/.spack-${STACK}


echo 'Source Spack and show version'
. $SPACK_INSTALL_PATH/share/spack/setup-env.sh

spack --version

echo "Add system compiler:"
spack compiler find --scope site /usr

echo "============= COMPILERS DEBUG INFO ============="
echo "spack config blame compilers"
spack config blame compilers

echo "spack compilers"
spack compilers


