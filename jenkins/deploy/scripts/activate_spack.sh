#!/bin/bash -l
set -euo pipefail

echo 'Activating Python virtual environment'
. ${PYTHON_VIRTUALENV_PATH}/bin/activate

echo 'Active Spack'
. $SPACK_INSTALL_PATH/share/spack/setup-env.sh

spack --version

environment=$(echo $NODE_LABELS | cut -d '-' -f 1)
echo "ENVIRONMENT ${environment}"

SPACK_SYSTEM_CONFIG_PATH=$(spack location --env ${environment})
