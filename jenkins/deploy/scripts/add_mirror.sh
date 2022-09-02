#!/bin/bash -l
set -euo pipefail

# Activating Spack
. $JENKINS/activate_spack.sh

SPACK_MIRROR=$(yareed -file stacks/common.yaml -keys mirrors local)
SPACK_MIRROR=${WORK_DIR}/${SPACK_MIRROR}
echo "SPACK_MIRROR: ${SPACK_MIRROR}"

echo "Looping through all environments:"
for environment in $(yareed -file stacks/common.yaml -key environments); do
    echo "Creating mirror for environment ${environment}"
    spack --env ${environment} mirror create -D -d ${SPACK_MIRROR} -a
done

