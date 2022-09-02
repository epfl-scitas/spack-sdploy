#!/bin/bash -l
set -euo pipefail

# Activating Spack
. $JENKINS/activate_spack.sh

# This is a workaround, we must specify an existing
# platform, because SpackFile will do stuff, even if
# not needed for the following two commands.

echo "Installing external repos for:"
spack write-repos-yaml -s ${STACK_RELEASE} -p ph02_avx
spack config blame repos

echo "Installing mirrors configuration"
spack write-mirrors-yaml -s ${STACK_RELEASE} -p ph02_avx
spack config blame mirrors

echo "Installing compilers.yaml"
SOURCE=${SPACK_SYSTEM_CONFIG_PATH}/compilers.yaml
DEST=${SPACK_INSTALL_PATH}/etc/spack
cp ${SOURCE} ${DEST}

echo "Blame compilers"
spack config blame compilers

echo "Fixing intel compiler version"
spack_bin=$(spack location -r)/bin/spack
eval `${spack_bin} load --sh intel@20.0.4`
bad_ver=$(icc --version |grep icc |cut -d ' ' -f 3)

sed -i "s/intel@${bad_ver}/intel@20.0.4/" ${DEST}/compilers.yaml

cat ${DEST}/compilers.yaml
