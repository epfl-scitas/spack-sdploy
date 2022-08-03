#!/bin/bash -l
set -euo pipefail

export VERSION=v1
export SPACK_RELEASE=releases/v0.18
export SPACK_SDPLOY_PATH=spack-sdploy

echo === Exported variables ===
echo VERSION: ${VERSION}
echo SPACK_RELEASE: ${SPACK_RELEASE}
echo SPACK_SDPLOY_PATH: ${SPACK_SDPLOY_PATH}

echo === Test Access to variables defined in pipeline ===
echo STACK_RELEASE: ${STACK_RELEASE}
echo PYTHON_EXECUTABLE: ${PYTHON_EXECUTABLE}
