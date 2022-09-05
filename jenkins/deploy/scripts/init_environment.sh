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

echo "List spack environments:"
spack env list

echo "Deploying manifest"
spack --env ${environment} -d write-spack-yaml -s ${STACK_RELEASE}

echo "Installing packages configuration"
spack --env ${environment} -d write-packages-yaml -s ${STACK_RELEASE}
spack --env ${environment} config blame packages

echo "Installing modules configuration"
spack --env ${environment} -d write-modules-yaml -s ${STACK_RELEASE}
spack --env ${environment} config blame modules

echo "Installing config.yaml configuration: ${environment}"
spack --env ${environment} -d write-config-yaml -s ${STACK_RELEASE}
spack --env ${environment} config blame config

echo "Installing external repos for:"
spack --env ${environment} write-repos-yaml -s ${STACK_RELEASE}
spack --env ${environment} config blame repos

echo "Installing mirrors configuration"
spack --env ${environment} write-mirrors-yaml -s ${STACK_RELEASE}
spack --env ${environment} config blame mirrors

echo "List environment directory contents"
ls -l ${SPACK_SYSTEM_CONFIG_PATH}



# echo "Processing environment: ${environment}"
# if [[ -z $(spack env list | grep $environment) && $? -eq 1 ]] ; then
#     echo "$environment: creating..."
#     spack env create ${environment}
# else
#     echo "$environment: found"
# fi
