#!/bin/bash -l
set -euo pipefail

echo 'Activating Spack'
. $JENKINS/activate_spack.sh

echo "Checking for previous spack-sdploy installation:"
if [ -e ${SPACK_SDPLOY_INSTALL_PATH} ]; then
    echo 'Previous installation of spack-sdploy detected, removing...'
    rm -rf ${SPACK_SDPLOY_INSTALL_PATH}
else
    echo "Previous installation of spack-sdploy not found"
fi

echo "Cloning spack-sdploy"
git clone --branch debug https://github.com/epfl-scitas/spack-sdploy ${SPACK_SDPLOY_INSTALL_PATH}

echo "Adding extension key to config.yaml"
# mkdir ${SPACK_SYSTEM_CONFIG_PATH}
cat > ${SPACK_INSTALL_PATH}/etc/spack/config.yaml << EOF
config:
  extensions:
  - ${SPACK_SDPLOY_INSTALL_PATH}
  db_lock_timeout: 10
EOF

echo "spack config blame config"
spack config blame config
