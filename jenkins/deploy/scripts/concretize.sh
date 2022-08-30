#!/bin/bash -l
set -euo pipefail

environment=$(echo $NODE_LABELS | cut -d '-' -f 1)

# Activating Spack
. $JENKINS/activate_spack.sh

echo "Concretizing environment ${environment}"
spack --env ${environment} concretize
