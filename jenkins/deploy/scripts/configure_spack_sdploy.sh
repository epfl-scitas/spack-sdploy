#!/bin/bash -l
set -euo pipefail

echo 'Activating Python virtual environment'
. ${PYTHON_VIRTUALENV_PATH}/bin/activate

echo 'Load variables'
. $JENKINS_SCRIPTS_PATH/config.sh

cat > ${SPACK_USER_CONFIG_PATH}/config.yaml << EOF
config:
  extensions:
    ${SPACK_SDPLOY_INSTALL_PATH}
EOF
