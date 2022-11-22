#!/bin/bash -l
set -euo pipefail

# Activate Spack
. $JENKINS/activate_spack.sh

echo "Activate packages"
spack write-activate_list -s ${STACK_RELEASE} -p ${environment}

echo "Loop through all packages"
packages_to_activate=$(cat packages_to_activate)

for package in ${packages_to_activate}
do
    echo activating package ${package}
    spack activate ${package}
done
