#!/bin/bash -l
set -euo pipefail

# Activating Spack
. $JENKINS/activate_spack.sh

echo "Who is Spack:"
spack location -r

echo "List spack environments:"
spack env list

# <!> DIRECTORY OVERWRITTEN <!>
# export SPACK_SYSTEM_CONFIG_PATH=${SYSTEM_CONFIG_PREFIX}/${environment}
# echo "Grep SPACK_SYSTEM_CONFIG_PATH from shell environment"
# env|grep SPACK_SYSTEM_CONFIG_PATH
# echo "SPACK_SYSTEM_CONFIG_PATH: ${SPACK_SYSTEM_CONFIG_PATH}"
# mkdir -p ${SPACK_SYSTEM_CONFIG_PATH}
# echo "Created SPACK_SYSTEM_CONFIG_PATH in ${SPACK_SYSTEM_CONFIG_PATH}"

# if [ -d $(spack location -e ${environment}) ]; then
#     echo "Environment ${environment} already exists"
# else
#     echo "Creating environment ${environment}"
#     spack env create ${environment}
# fi

echo "Deploying manifest"
spack --env ${environment} write-spack-yaml -s ${STACK_RELEASE} -p ${environment}

echo "Installing packages configuration"
spack --env ${environment} write-packages-yaml -s ${STACK_RELEASE} -p ${environment}
spack --env ${environment} config blame packages

echo "Installing modules configuration"
spack --env ${environment} write-modules-yaml -s ${STACK_RELEASE} -p ${environment}
spack --env ${environment} config blame modules

echo "Installing config.yaml configuration: ${environment}"
spack --env ${environment} write-config-yaml -s ${STACK_RELEASE} -p ${environment}
spack --env ${environment} config blame config

echo "Installing external repos for:"
spack --env ${environment} write-repos-yaml -s ${STACK_RELEASE} -p ${environment}
spack --env ${environment} config blame repos

echo "Installing mirrors configuration"
spack --env ${environment} write-mirrors-yaml -s ${STACK_RELEASE} -p ${environment}
spack --env ${environment} config blame mirrors

echo "List environment directory contents"
ls -l ${SPACK_SYSTEM_CONFIG_PATH}

