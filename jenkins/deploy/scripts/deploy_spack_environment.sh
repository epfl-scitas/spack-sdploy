#!/bin/bash -l

echo 'Activating Spack'
. $JENKINS/activate_spack.sh

echo "Remove existing spack.yaml"
rm /home/scitasbuildpr/syrah-lite/spack.v1/var/spack/environments/ph02-avx/spack.yaml

echo "Installing stack configuration: ${environment}"
spack --env ${environment} write-spack-yaml -s ${STACK_RELEASE} -p ${environment} -d

echo "Installing packages configuration: ${environment}"
spack write-packages-yaml -s ${STACK_RELEASE} -p ${environment} -d

echo "Installing modules configuration: ${environment}"
spack write-modules-yaml -s ${STACK_RELEASE} -p ${environment} -d
