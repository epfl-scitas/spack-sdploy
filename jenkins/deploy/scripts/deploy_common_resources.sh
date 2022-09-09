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

# At this point the compilers are already configured in
# /home/scitasbuildpr/l2/syrah-lite/spack-config/compilers.yaml
echo "Installing compilers.yaml"
SOURCE=${SPACK_SYSTEM_CONFIG_PATH}/compilers.yaml
DEST=${SPACK_INSTALL_PATH}/etc/spack
cp ${SOURCE} ${DEST}

echo "===================== COMPILERS DEBUG INFO: START ====================="
echo "SPACK_SYSTEM_CONFIG_PATH: ${SPACK_SYSTEM_CONFIG_PATH}"
echo "spack config blame compilers"
spack config blame compilers
echo "spack compilers"
spack compilers
echo "cat ${SPACK_SYSTEM_CONFIG_PATH}/compilers.yaml:"
cat ${SPACK_SYSTEM_CONFIG_PATH}/compilers.yaml
echo "${SPACK_INSTALL_PATH}/etc/spack/compilers.yaml"
cat ${SPACK_INSTALL_PATH}/etc/spack/compilers.yaml
echo "===================== COMPILERS DEBUG INFO: END ====================="

echo "Fixing intel compiler version"
spack_bin=$(spack location -r)/bin/spack
eval `${spack_bin} load --sh intel@20.0.4`
bad_ver=$(icc --version |grep icc |cut -d ' ' -f 3)
sed -i "s/intel@${bad_ver}/intel@20.0.4/" ${DEST}/compilers.yaml

echo "===================== COMPILERS DEBUG INFO: START ====================="
echo "SPACK_SYSTEM_CONFIG_PATH: ${SPACK_SYSTEM_CONFIG_PATH}"
echo "spack config blame compilers"
spack config blame compilers
echo "spack compilers"
spack compilers
echo "cat ${SPACK_SYSTEM_CONFIG_PATH}/compilers.yaml:"
cat ${SPACK_SYSTEM_CONFIG_PATH}/compilers.yaml
echo "${SPACK_INSTALL_PATH}/etc/spack/compilers.yaml"
cat ${SPACK_INSTALL_PATH}/etc/spack/compilers.yaml
echo "===================== COMPILERS DEBUG INFO: END ====================="
