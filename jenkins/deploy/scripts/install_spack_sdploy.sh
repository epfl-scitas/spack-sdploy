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
EOF

echo "spack config blame config"
spack config blame config

echo 'Installing Intel license'
# If directory already exists, remove it
# This is done here beacuse it must be done only once !
SOURCE_PATH=${SPACK_SDPLOY_INSTALL_PATH}/external/licenses/intel
LICENSE_PATH=${SPACK_INSTALL_PATH}/etc/spack/licenses/intel
if [ ! -d ${LICENSE_PATH} ]; then
    mkdir -p ${LICENSE_PATH}
    cp ${SOURCE_PATH}/USE_SERVER.lic ${LICENSE_PATH}/license.lic
else
    rm -r ${LICENSE_PATH}
    mkdir -p ${LICENSE_PATH}
    cp ${SOURCE_PATH}/USE_SERVER.lic ${LICENSE_PATH}/license.lic
fi
