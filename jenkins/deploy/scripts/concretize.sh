#!/bin/bash -l
set -euo pipefail

echo 'Activating Spack'
. $JENKINS/activate_spack.sh

echo "Concretizing environment ${environment}"
spack --env ${environment} concretize
