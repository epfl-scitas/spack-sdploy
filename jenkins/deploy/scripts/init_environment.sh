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
spack --env ${environment} write-spack-yaml -s ${STACK_RELEASE}

echo "Installing packages configuration for ${environment}"
spack --env ${environment} write-packages-yaml -s ${STACK_RELEASE}
spack --env ${environment} config blame packages

echo "Installing modules configuration for ${environment}"
spack --env ${environment} write-modules-yaml -s ${STACK_RELEASE}
spack --env ${environment} config blame modules

echo "Installing config.yaml for ${environment}"
spack --env ${environment} write-config-yaml -s ${STACK_RELEASE}
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

if [ -d ${SPACK_SDPLOY_INSTALL_PATH}/stacks/${STACK}/data/templates ]; then
    echo "Installing templates files"
    cp -r ${SPACK_SDPLOY_INSTALL_PATH}/stacks/${STACK}/data/templates ${SPACK_SYSTEM_CONFIG_PATH}
fi

echo "Creating symlink for users to be able to do an upstream"
mkdir -p ${STACK_PREFIX}/${STACK_RELEASE_VER}/var/spack/environments
cd ${STACK_PREFIX}/${STACK_RELEASE_VER}/var/spack/environments
ln -sf ${SPACK_SYSTEM_CONFIG_PATH} ${environment}

echo "List environment directory contents"
ls -l ${SPACK_SYSTEM_CONFIG_PATH}
