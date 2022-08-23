#!/bin/bash -l
set -euo pipefail

# Activating Spack
. $JENKINS/activate_spack.sh

echo "Creating mirror for environment ${environment}"
spack --env ${environment} add-mirror create -D -a -s ${STACK_RELEASE} -p ${environment}
