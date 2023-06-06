#!/bin/bash -l
set -euo pipefail

# Activating Spack
. $JENKINS/activate_spack.sh

echo "Installing packages for environment ${environment}"
spack --env ${environment} install --log-format junit --log-file install_stack.xml --only-concrete

# Modules are now created in next step 
#echo "Creating modules for environment ${environment}"
#spack --env ${environment} module lmod refresh -y
