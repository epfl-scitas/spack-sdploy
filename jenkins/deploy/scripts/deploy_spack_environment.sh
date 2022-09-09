#!/bin/bash -l
set -euo pipefail
set -x

# Activating Spack
. $JENKINS/activate_spack.sh

echo "Deploying manifest"
spack --env ${environment} -d write-spack-yaml -s ${STACK_RELEASE} -p ${environment}

echo "Installing packages configuration"
spack --env ${environment} -d write-packages-yaml -s ${STACK_RELEASE} -p ${environment}
spack --env ${environment} config blame packages

echo "Installing modules configuration"
spack --env ${environment} -d write-modules-yaml -s ${STACK_RELEASE} -p ${environment}
spack --env ${environment} config blame modules

echo "Installing config.yaml configuration: ${environment}"
spack --env ${environment} -d write-config-yaml -s ${STACK_RELEASE} -p ${environment}
spack --env ${environment} config blame config

echo "Installing external repos for:"
spack --env ${environment} write-repos-yaml -s ${STACK_RELEASE} -p ${environment}
spack --env ${environment} config blame repos

echo "Installing mirrors configuration"
spack --env ${environment} write-mirrors-yaml -s ${STACK_RELEASE} -p ${environment}
spack --env ${environment} config blame mirrors

echo "List environment directory contents"
ls -l ${SPACK_SYSTEM_CONFIG_PATH}

