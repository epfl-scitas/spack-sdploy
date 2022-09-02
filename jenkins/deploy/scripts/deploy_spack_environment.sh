#!/bin/bash -l
# set -euo pipefail

environment=$(echo $NODE_LABELS | cut -d '-' -f 1)
echo "NODE_LABEL: $NODE_LABELS"
echo "ENVIRONMENT: $environment"

# Activating Spack
. $JENKINS/activate_spack.sh

SPACK_SYSTEM_CONFIG_PATH=${SYSTEM_CONFIG_PREFIX}/${environment}
echo "SPACK_SYSTEM_CONFIG_PATH: ${SPACK_SYSTEM_CONFIG_PATH}"
mkdir -p ${SPACK_SYSTEM_CONFIG_PATH}
echo "Created SPACK_SYSTEM_CONFIG_PATH in ${SPACK_SYSTEM_CONFIG_PATH}"

#echo "Creating spack environemnt: ${environment}"
# We test if the environment directory already exists ans create it otherwise
# env_dir=$(spack location -e ${environment})

if ! [ -e $(spack location -e ${environment} ]; then
    echo "Environment ${environment} already exists"
else
    echo "Creating environment ${environment}"
    spack env create ${environment}
fi

echo "Deploying manifest"
spack --env ${environment} write-spack-yaml -s ${STACK_RELEASE} -p ${environment}

echo "Installing packages configuration"
spack --env ${environment} write-packages-yaml -s ${STACK_RELEASE} -p ${environment} -d
spack --env ${environment} config blame packages

echo "Installing modules configuration"
spack --env ${environment} write-modules-yaml -s ${STACK_RELEASE} -p ${environment} -d
spack --env ${environment} config blame modules

echo "Installing config.yaml configuration: ${environment}"
spack --env ${environment} write-config-yaml -s ${STACK_RELEASE} -p ${environment} -d
spack --env ${environment} config blame config


