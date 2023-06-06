#!/bin/bash -l
set -euo pipefail

. ${JENKINS}/setenv.sh

if [ -e ${SPACK_INSTALL_PATH} ]; then
    echo 'Previous installation of Spack detected...'
    cd ${SPACK_INSTALL_PATH}
    git fetch origin
    git checkout $SPACK_RELEASE
    cd -
else
    echo 'Spack not detected...'
    git clone -b $SPACK_RELEASE https://github.com/spack/spack ${SPACK_INSTALL_PATH}
fi

if [ ! -d $HOME/.spack-${STACK} ]; then
    mkdir -p $HOME/.spack-${STACK}
fi

echo 'Activating Python virtual environment'
pwd
. ${JENKINS}/activate_spack.sh

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


