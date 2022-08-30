#!/bin/bash -l
set -euo pipefail

echo 'Activating Python virtual environment'
. ${PYTHON_VIRTUALENV_PATH}/bin/activate

echo 'Source Spack'
. $SPACK_INSTALL_PATH/share/spack/setup-env.sh

echo "SPACK_SYSTEM_CONFIG_PATH: ${SPACK_SYSTEM_CONFIG_PATH}"

if [ -e ${SPACK_SYSTEM_CONFIG_PATH} ]; then
    echo 'Previous configuration directory detected, removing...'
    rm -rf ${SPACK_SYSTEM_CONFIG_PATH}
fi

mkdir ${SPACK_SYSTEM_CONFIG_PATH}
cat > ${SPACK_SYSTEM_CONFIG_PATH}/config.yaml << EOF
config:
  extensions:
  - ${SPACK_SDPLOY_INSTALL_PATH}
EOF

echo "spack config blame config"
spack config blame config
