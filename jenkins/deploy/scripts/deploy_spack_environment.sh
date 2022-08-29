#!/bin/bash -l
# set -euo pipefail

environment=$(echo $NODE_LABELS | cut -d '-' -f 1)
echo "NODE_LABEL: $NODE_LABELS"
echo "ENVIRONMENT: $environment"

# Activating Spack
. $JENKINS/activate_spack.sh

echo "Installing stack configuration: ${environment}"
spack --env ${environment} write-spack-yaml -s ${STACK_RELEASE} -p ${environment}

echo "Installing packages configuration: ${environment}"
spack -v --env ${environment} write-packages-yaml -s ${STACK_RELEASE} -p ${environment} -d

echo "Installing modules configuration: ${environment}"
spack -v --env ${environment} write-modules-yaml -s ${STACK_RELEASE} -p ${environment} -d

echo "Installing mirrors configuration: ${environment}"
spack -v --env ${environment} write-mirrors-yaml -s ${STACK_RELEASE} -p ${environment} -d
