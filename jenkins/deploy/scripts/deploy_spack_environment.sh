#!/bin/bash -l
# set -euo pipefail

environment=$(echo $NODE_LABELS | cut -d '-' -f 1)
echo "NODE_LABEL: $NODE_LABELS"
echo "ENVIRONMENT: $environment"

# Activating Spack
. $JENKINS/activate_spack.sh

# When doing this, all the files writen to the previous
# location do not take effect anymore. To use the extension
# we must copy the files over ot the new directory.
cp ${SPACK_SYSTEM_CONFIG_PATH}/* $(spack location -e $environment)
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

echo "Reporting spack.yaml:"
cat $(spack location -e $environment)/spack.yaml

