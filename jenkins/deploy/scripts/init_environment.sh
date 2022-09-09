#!/bin/bash -l
set -euo pipefail

# Activating Spack
. $JENKINS/activate_spack.sh

echo "Who is Spack:"
spack location -r

echo "Processing environment: ${environment}"
if [ ! -e ${SPACK_INSTALL_PATH}/var/spack/environments/${environment}/spack.yaml ]; then
    echo "$environment: creating..."
    spack env create ${environment}
else
    echo "$environment: found"
fi

_env_path=$(spack location --env ${environment} || true)

if [ ! -z ${_env_path} ]; then
    export SPACK_SYSTEM_CONFIG_PATH=${_env_path}
fi

echo "Deploying manifest for ${environment}"
spack --env ${environment} -d write-spack-yaml -s ${STACK_RELEASE}

echo "Installing packages configuration for ${environment}"
spack --env ${environment} -d write-packages-yaml -s ${STACK_RELEASE}
spack --env ${environment} config blame packages

echo "Installing modules configuration for ${environment}"
spack --env ${environment} -d write-modules-yaml -s ${STACK_RELEASE}
spack --env ${environment} config blame modules

echo "Installing config.yaml for ${environment}"
spack --env ${environment} -d write-config-yaml -s ${STACK_RELEASE}
spack --env ${environment} config blame config

echo "Installing external repos for ${environment}"
spack --env ${environment} write-repos-yaml -s ${STACK_RELEASE}
spack --env ${environment} config blame repos

echo "Installing mirrors configuration for ${environment}"
spack --env ${environment} write-mirrors-yaml -s ${STACK_RELEASE}
spack --env ${environment} config blame mirrors

echo "Installing concretizer configuration for ${environment}"
spack --env ${environment} write-concretizer-yaml -s ${STACK_RELEASE}
spack --env ${environment} config blame concretizer

echo "List environment directory contents"
ls -l ${SPACK_SYSTEM_CONFIG_PATH}
