#!/bin/bash -l
set -euo pipefail

# Activating Spack
. $JENKINS/activate_spack.sh

echo "SPACK_SYSTEM_CONFIG_PATH=${SPACK_SYSTEM_CONFIG_PATH}"
spack config blame repos

echo "Installing packages for environment ${environment}"
spack --env ${environment} install --log-format junit --log-file install_stack.xml

echo "Creating modules for environment ${environment}"
spack --env ${environment} module lmod refresh -y
