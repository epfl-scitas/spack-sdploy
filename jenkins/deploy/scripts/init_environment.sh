#!/bin/bash -l
# set -euo pipefail

environment=$(echo $NODE_LABELS | cut -d '-' -f 1)
echo "NODE_LABEL: $NODE_LABELS"
echo "ENVIRONMENT ${environment}"

# Activating Spack
. $JENKINS/activate_spack.sh

echo "Who is Spack:"
spack location -r

echo "Processing environment: ${environment}"
if [[ -z $(spack env list | grep $environment) && $? -eq 1 ]] ; then
    echo "$environment: creating environment"
    # spack env create ${environment}
else
    echo "$environment: found environment"
fi

echo "List spack environments:"
spack env list
