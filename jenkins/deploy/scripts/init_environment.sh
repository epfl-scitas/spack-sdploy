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

# echo "Processing environment: ${environment}"
# if [[ -z $(spack env list | grep $environment) && $? -eq 1 ]] ; then
#     echo "$environment: creating..."
#     spack env create ${environment}
# else
#     echo "$environment: found"
# fi
