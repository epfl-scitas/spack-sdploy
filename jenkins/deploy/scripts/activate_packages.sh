#!/bin/bash -l
set -euo pipefail

# Activate Spack
. $JENKINS/activate_spack.sh

echo "Activate packages"
spack write-activate-list -s ${STACK_RELEASE} -p ${environment}

echo "Loop through all packages"
packages_to_activate=$(cat packages_to_activate)

CACHE_FILE=${HOME}/.${STACK_RELEASE}.${STACK_RELEASE_VER}_activated_cache
touch ${CACHE_FILE}

set +e
while read -r spec
do
    hash=$(spack find -xL "${spec}" | grep -e "[a-z0-9]\{16\}" | awk '{ print $1 }')
    echo "Activating package ${spec} (${hash})"
    grep -q ${hash} ${CACHE_FILE}
    if [ $? -eq 0 ]; then
        echo "Already activated"
        continue
    fi

    spack -e ${environment} activate --force "/${hash}"
    if [ $? -eq 0 ]; then
        echo "ACTIVATED ${hash}"
        echo "$spec ($hash)" >> ${CACHE_FILE}
    fi
done <<< $(cat packages_to_activate)
set -e
