#!/bin/bash -l
# set -euo pipefail

environment=$(echo $NODE_LABELS | cut -d '-' -f 1)

# Activating Spack
. $JENKINS/activate_spack.sh

echo "Installing stack configuration: ${environment}"
spack --env ${environment} write-spack-yaml -s ${STACK_RELEASE} -p ${environment}

echo "Installing packages configuration: ${environment}"
spack write-packages-yaml -v -s ${STACK_RELEASE} -p ${environment} -d

echo "Installing modules configuration: ${environment}"
spack write-modules-yaml -v -s ${STACK_RELEASE} -p ${environment} -d

echo "Installing mirrors configuration: ${environment}"
spack write-mirrors-yaml -v-s ${STACK_RELEASE} -p ${environment} -d
