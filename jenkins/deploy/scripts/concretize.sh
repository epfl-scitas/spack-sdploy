#!/bin/bash -l
set -euo pipefail

# Activating Spack
. $JENKINS/activate_spack.sh

echo "Concretizing environment ${environment}"
spack -c config:build_jobs:32 --env ${environment} concretize --force
