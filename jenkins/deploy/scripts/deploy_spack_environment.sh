#!/bin/bash -l
# set -euo pipefail

environment=$(echo $NODE_LABELS | cut -d '-' -f 1)
echo "NODE_LABEL: $NODE_LABELS"
echo "ENVIRONMENT: $environment"

# Activating Spack
. $JENKINS/activate_spack.sh

SPACK_SYSTEM_CONFIG_PATH=$(spack location -e $environment)

echo "Installing stack configuration: ${environment}"
spack --env ${environment} write-spack-yaml -s ${STACK_RELEASE} -p ${environment}

echo "Installing packages configuration: ${environment}"
spack --env ${environment} write-packages-yaml -s ${STACK_RELEASE} -p ${environment} -d

echo "Installing modules configuration: ${environment}"
spack --env ${environment} write-modules-yaml -s ${STACK_RELEASE} -p ${environment} -d

echo "Installing mirrors configuration: ${environment}"
spack --env ${environment} write-mirrors-yaml -s ${STACK_RELEASE} -p ${environment} -d

echo "Installing config.yaml configuration: ${environment}"
spack --env ${environment} write-config-yaml -s ${STACK_RELEASE} -p ${environment} -d
