#!/bin/bash -l
set -euo pipefail

export VERSION=v1
export SPACK_RELEASE=releases/v0.18

echo === Exported variables ===
echo VERSION: ${VERSION}
echo SPACK_RELEASE: ${SPACK_RELEASE}
