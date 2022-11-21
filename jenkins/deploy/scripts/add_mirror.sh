#!/bin/bash -l
set -euo pipefail

# Activating Spack
. $JENKINS/activate_spack.sh

spack list-mirrors -s ${STACK_RELEASE} | grep local | tee mirrors.list
SPACK_MIRROR=$(cat mirrors.list | cut -d ' ' -f 2)

echo "Looping through all environments:"
for environment in $(spack env list); do
    echo "Creating mirror for environment ${environment}"
    # Setting SPACK_SYSTEM_CONFIG_PATH here bacause the job jenkins running this script
    # is not environment aware and therefor it fails doing so in activate_spack.sh.
    export SPACK_SYSTEM_CONFIG_PATH=$(spack location --env ${environment} || true)
    spack --env ${environment} mirror -n create -D -d ${SPACK_MIRROR} -a || /usr//bin/true
done
