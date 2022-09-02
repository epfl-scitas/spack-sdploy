#!/bin/bash -l
set -euo pipefail

environment=$(echo $NODE_LABELS | cut -d '-' -f 1)
echo "ENVIRONMENT ${environment}"

echo 'Activating Spack'
. $JENKINS/activate_spack.sh

echo "Initialize environment: ${environment}"
spack env create ${environment}
