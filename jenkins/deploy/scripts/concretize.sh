#!/bin/bash -l
set -euo pipefail

# Activating Spack
. $JENKINS/activate_spack.sh

timestamp=`date +%y%m%d.%k%m%M`

echo "Concretizing environment ${environment}"
spack --env ${environment} concretize --force > concretize.${timestamp}.log
