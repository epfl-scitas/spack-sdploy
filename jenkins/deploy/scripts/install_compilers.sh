#!/bin/bash -l
set -euo pipefail

echo 'Activating Spack'
. $JENKINS_SCRIPTS_PATH/activate_spack.sh

spack install-compilers --templates stacks/syrah-lite/templates

env
