#!/bin/bash -l
set -euo pipefail

export VERSION=v1
export SPACK_RELEASE=releases/v0.18
export SPACK_SDPLOY_PATH=spack-sdploy
export SPACK_CONFIG_PATH=spack-config
export SPACK_USER_CONFIG_PATH=${STACK_PREFIX}/${SPACK_CONFIG_PATH}
export SPACK_SDPLOY_INSTALL_PATH=${STACK_PREFIX}/${SPACK_SDPLOY_PATH}

echo === Exported variables ===
echo VERSION: ${VERSION}
echo SPACK_RELEASE: ${SPACK_RELEASE}
echo SPACK_SDPLOY_PATH: ${SPACK_SDPLOY_PATH}
echo SPACK_CONFIG_PATH: ${SPACK_CONFIG_PATH}
echo SPACK_USER_CONFIG_PATH: ${SPACK_USER_CONFIG_PATH}
echo SPACK_SDPLOY_INSTALL_PATH: $SPACK_SDPLOY_INSTALL_PATH
