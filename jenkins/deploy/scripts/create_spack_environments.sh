#!/bin/bash -l

echo 'Activating Spack'
. $JENKINS/activate_spack.sh

# Manually deploy stack.yaml
#
# cp ${SPACK_SDPLOY_INSTALL_PATH}/temp/spack.yaml /home/scitasbuildpr/syrah-lite/spack.v1/var/spack/environments/ph02-avx2
# 
# cp ${SPACK_SDPLOY_INSTALL_PATH}/temp/spack.yaml /home/scitasbuildpr/syrah-lite/spack.v1/var/spack/environments/ph02-avx

# If the environments already exist, they will not be erased
spack create-environments
