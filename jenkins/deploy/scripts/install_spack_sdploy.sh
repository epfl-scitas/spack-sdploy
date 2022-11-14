#!/bin/bash -l
set -euo pipefail

echo 'Activating Spack'
. $JENKINS/activate_spack.sh

rsync -auv $PWD/ ${SPACK_SDPLOY_INSTALL_PATH}/

echo "Adding extension key to config.yaml"
# mkdir ${SPACK_SYSTEM_CONFIG_PATH}
cat > ${SPACK_INSTALL_PATH}/etc/spack/config.yaml << EOF
config:
  extensions:
  - ${SPACK_SDPLOY_INSTALL_PATH}
  db_lock_timeout: 10
  build_jobs: 32
EOF

echo "spack config blame config"
spack config blame config

