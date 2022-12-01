#!/bin/bash -l
set -euo pipefail

. ${JENKINS}/configure_proxies.sh
. ${JENKINS}/setenv.sh


echo 'Activating Python virtual environment' 1>&2
if [ -e ${PYTHON_VIRTUALENV_PATH}/bin/activate ]; then
    . ${PYTHON_VIRTUALENV_PATH}/bin/activate
fi

echo 'Active Spack' 1>&2
if [ -e $SPACK_INSTALL_PATH/share/spack/setup-env.sh ]; then
    . $SPACK_INSTALL_PATH/share/spack/setup-env.sh
    spack --version

    export SPACK_USER_CACHE_PATH=$HOME/.spack-${STACK}
    export SPACK_USER_CONFIG_PATH=$HOME/.spack-${STACK}

    environment=$(echo $NODE_LABELS | cut -d '-' -f 1)
    set +e
    echo $NODE_LABELS | grep -q login
    res=$?
    set -e
    if [ $res -eq 0 ]; then
        echo "Running on a login node" 1>&2
        break
    fi

    echo "ENVIRONMENT ${environment}" 1>&2

    _env_path=$(spack location --env ${environment} || true)


    if [ ! -z ${_env_path} ]; then
        export SPACK_SYSTEM_CONFIG_PATH=${_env_path}
        echo "Setting SPACK_SYSTEM_CONFIG_PATH to: ${SPACK_SYSTEM_CONFIG_PATH}" 1>&2
    fi
fi
