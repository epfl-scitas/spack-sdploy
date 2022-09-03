#!/bin/bash -l
set -euo pipefail

echo 'Activating Python virtual environment'
. ${PYTHON_VIRTUALENV_PATH}/bin/activate

echo 'Active Spack'
. $SPACK_INSTALL_PATH/share/spack/setup-env.sh

spack --version
