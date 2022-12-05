#!/usr/bin/env bash
set -euo pipefail

. ${JENKINS}/activate_spack.sh

set +e # if grep fails it is normal
spack gpg list | grep -q ${STACK_RELEASE}_cache
res=$?
set -e
if [ $res -ne 0 ]; then
    spack gpg create ${STACK_RELEASE}_cache scitas@epfl.ch
fi

mkdir -p ${SPACK_BUILDCACHE_PATH}
