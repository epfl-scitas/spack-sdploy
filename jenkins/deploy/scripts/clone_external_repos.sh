#!/bin/bash -l

echo 'Activating Python virtual environment'
. ${PYTHON_VIRTUALENV_PATH}/bin/activate

echo 'Source Spack'
. $SPACK_INSTALL_PATH/share/spack/setup-env.sh

spack repos-yaml -s ${STACK_RELEASE}
