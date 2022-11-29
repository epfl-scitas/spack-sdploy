#!/bin/bash -l
set -euo pipefail

source $HOME/.profile

echo 'Activating Python virtual environment'
if [ -e ${PYTHON_VIRTUALENV_PATH}/bin/activate ]; then
    . ${PYTHON_VIRTUALENV_PATH}/bin/activate
fi

echo 'Active Spack'
if [ -e $SPACK_INSTALL_PATH/share/spack/setup-env.sh ]; then
    . $SPACK_INSTALL_PATH/share/spack/setup-env.sh
    spack --version

    environment=$(echo $NODE_LABELS | cut -d '-' -f 1)
    echo "ENVIRONMENT ${environment}"

    _env_path=$(spack location --env ${environment} || true)

    export SPACK_USER_CACHE_PATH=$HOME/.spack-${STACK}
    export SPACK_USER_CONFIG_PATH=$HOME/.spack-${STACK}

    if [ ! -z ${_env_path} ]; then
        export SPACK_SYSTEM_CONFIG_PATH=${_env_path}
        echo "Setting SPACK_SYSTEM_CONFIG_PATH to: ${SPACK_SYSTEM_CONFIG_PATH}"
    fi
fi
