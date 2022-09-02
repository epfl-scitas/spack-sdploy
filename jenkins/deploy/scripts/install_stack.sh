#!/bin/bash -l
set -euo pipefail

environment=$(echo $NODE_LABELS | cut -d '-' -f 1)
echo "NODE_LABEL: $NODE_LABELS"
echo "ENVIRONMENT: $environment"

# Activating Spack
. $JENKINS/activate_spack.sh

echo "Installing packages for environment ${environment}"
spack --env ${environment} install

echo "Creating modules for environment ${environment}"
spack --env ${environment} module lmod refresh -y
