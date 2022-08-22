#!/bin/bash -l
set -euo pipefail

echo 'Activating Python virtual environment'
. ${PYTHON_VIRTUALENV_PATH}/bin/activate

echo 'Source Spack'
. $SPACK_INSTALL_PATH/share/spack/setup-env.sh

echo "Installing external repos for:"
echo "STACK: ${STACK_RELEASE}"

spack write-repos-yaml -s ${STACK_RELEASE}

