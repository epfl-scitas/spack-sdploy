#!/bin/bash -l
set -euo pipefail

environment=$(echo $NODE_LABELS | cut -d '-' -f 1)
echo "NODE LABELS: $NODE_LABELS"
echo "ENVIRONMENT: $environment"

# Activating Spack
. $JENKINS/activate_spack.sh

echo "Installing packages configuration: ${environment}"
spack -v write-packages-yaml -s ${STACK_RELEASE} -p ${environment} -d

echo "Installing modules configuration: ${environment}"
spack -v write-modules-yaml -s ${STACK_RELEASE} -p ${environment} -d

echo "Installing mirrors configuration: ${environment}"
spack -v write-mirrors-yaml -s ${STACK_RELEASE} -p ${environment} -d
