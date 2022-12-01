#!/usr/bin/env bash

set -euo pipefail

. activate_spack.sh

#Pushing to buildcache
spack -e ${environment} buildcache create -d ${SPACK_BUILDCACHE_PATH}
