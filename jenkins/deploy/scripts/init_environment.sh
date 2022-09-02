#!/bin/bash -l
set -euo pipefail

environment=$(echo $NODE_LABELS | cut -d '-' -f 1)
echo "ENVIRONMENT ${environment}"

echo 'Activating Spack'
. $JENKINS/activate_spack.sh

echo "Initialize environment: ${environment}"
if [[ -z $(spack env list | grep $environment) ]] && $?; then
   echo "Found environment $environment"
else
   echo "Creating environment $environment"
   spack env create ${environment}
fi
