#!/bin/bash -l

echo 'Activating Python virtual environment'
. ${PYTHON_VIRTUALENV_PATH}/bin/activate

echo 'Load variables'
#. $JENKINS_SCRIPTS_PATH/config.sh

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
