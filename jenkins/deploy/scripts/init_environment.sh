#!/bin/bash -l
# set -euo pipefail

environment=$(echo $NODE_LABELS | cut -d '-' -f 1)
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
spack env list |head


# spack_env_path=$(spack location -e ${environment})
# echo "spack_env_path: ${spack_env_path}"

 # if [ -d $(spack_env_path) ]; then
 #     echo "Environment ${environment} already exists"
 # else
 #     echo "Creating environment ${environment}"
 #     spack env create ${environment}
 # fi


#echo "Initialize environment: ${environment}"
#if [[ -z $(spack env list | grep $environment) && $? -eq 1 ]] ; then
#    echo "Creating environment $environment"
#    # spack env create ${environment}
#else
#    echo "Found environment $environment"
#fi
#
#echo "List spack environments"
#spack env list
#
