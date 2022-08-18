#!/bin/bash -l

echo 'Activating Spack'
. $JENKINS/activate_spack.sh

echo "Installing stack configuration: ${environment}"
spack --env ${environment} write-spack-yaml -s ${STACK_RELEASE} -p ${environment}

echo "Installing modules configuration: ${environment}"
spack --env ${environment} write-modules-yaml -s ${STACK_RELEASE} -p ${environment}

echo "Installing packages configuration: ${environment}"
spack --env ${environment} write-packages-yaml -s ${STACK_RELEASE} -p ${environment}
