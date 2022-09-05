#!/bin/bash -l
set -euo pipefail

# Activating Spack
. $JENKINS/activate_spack.sh

spack list-mirrors -s ${STACK_RELEASE} | grep local | tee mirrors.list
SPACK_MIRROR=$(cat mirrors.list | cut -d ' ' -f 2)

echo "Looping through all environments:"
for environment in $(spack env list); do
    echo "Creating mirror for environment ${environment}"
    spack --env ${environment} mirror create -D -d ${SPACK_MIRROR} -a
done

