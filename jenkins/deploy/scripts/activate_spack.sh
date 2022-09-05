#!/bin/bash -l
set -euo pipefail
set -x

echo 'Activating Python virtual environment'
. ${PYTHON_VIRTUALENV_PATH}/bin/activate

echo 'Active Spack'
. $SPACK_INSTALL_PATH/share/spack/setup-env.sh

spack --version

environment=$(echo $NODE_LABELS | cut -d '-' -f 1)
echo "ENVIRONMENT ${environment}"

_env_path=$(spack location --env ${environment} || true)

if [ ! -z ${_env_path} ]; then
    export SPACK_SYSTEM_CONFIG_PATH=${_env_path}
fi
