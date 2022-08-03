#!/bin/bash -l
set -euo pipefail

echo 'Activating Python virtual environment'
. ${PYTHON_VIRTUALENV_PATH}/bin/activate

echo 'Load variables'
. $JENKINS_SCRIPTS_PATH/config.sh

if [ -e ${SPACK_USER_CONFIG_PATH} ]; then
    echo 'Previous configuration directory detected, removing...'
    rm -rf ${SPACK_USER_CONFIG_PATH}
fi

mkdir ${SPACK_USER_CONFIG_PATH}
cat > ${SPACK_USER_CONFIG_PATH}/config.yaml << EOF
config:
  extensions:
    ${SPACK_SDPLOY_INSTALL_PATH}
EOF
