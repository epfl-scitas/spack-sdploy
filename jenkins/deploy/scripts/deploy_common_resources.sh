#!/bin/bash -l
set -euo pipefail

# Activating Spack
. $JENKINS/activate_spack.sh

# This is a workaround, we must specify an existing
# platform, because SpackFile will do stuff, even if
# not needed for the following two commands.

echo "Installing external repos for:"
spack write-repos-yaml -s ${STACK_RELEASE} -p ph02_avx
spack config blame repos

echo "Installing mirrors configuration"
spack write-mirrors-yaml -s ${STACK_RELEASE} -p -p ph02_avx
spack config blame repos
