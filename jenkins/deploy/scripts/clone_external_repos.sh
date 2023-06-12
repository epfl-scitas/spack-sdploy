#!/bin/bash -l
set -euo pipefail

# Activating Spack
. $JENKINS/activate_spack.sh

echo "Installing external repos for:"
echo "STACK: ${STACK_RELEASE}"

# This is a workaround, we must specify an existing
# platform, because SpackFile will do stuff, even if
# not needed for this command.
spack clone-external-repos -s ${STACK_RELEASE} -w ${WORK_DIR}
