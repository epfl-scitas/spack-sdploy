#!/bin/bash -l
set -euo pipefail

# Activating Spack
. $JENKINS/activate_spack.sh

_env_path=$(spack location --env ${environment} || true)

if [ ! -z ${_env_path} ]; then
    export SPACK_SYSTEM_CONFIG_PATH=${_env_path}
else
    echo "Cannot locate environment, aborting"
    return
fi

echo "spack compilers before:"
spack compilers

spack load 
