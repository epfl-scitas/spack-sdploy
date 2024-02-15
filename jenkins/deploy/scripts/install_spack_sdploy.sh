#!/bin/bash -l
set -euo pipefail

echo 'Activating Spack'
. $JENKINS/activate_spack.sh

mkdir -p ${SPACK_SDPLOY_INSTALL_PATH}/

rsync -auv $PWD/ ${SPACK_SDPLOY_INSTALL_PATH}/

echo "Adding extension key to config.yaml"
# mkdir ${SPACK_SYSTEM_CONFIG_PATH}
cat > ${SPACK_INSTALL_PATH}/etc/spack/config.yaml << EOF
config:
  extensions:
  - ${SPACK_SDPLOY_INSTALL_PATH}
  install_tree:
    root: ${STACK_PREFIX}/${STACK_RELEASE_VER}/opt/spack
EOF

echo "spack config blame config"
spack config blame config
