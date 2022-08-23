#!/bin/bash -l
set -euo pipefail

# Activating Spack
. $JENKINS/activate_spack.sh

echo "Concretizing environment ${environment}"
spack -d --env ${environment} concretize
