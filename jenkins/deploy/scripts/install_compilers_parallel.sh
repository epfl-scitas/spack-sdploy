#!/bin/bash -l
set -euo pipefail

environment=$(echo $NODE_LABELS | cut -d '-' -f 1)
echo "ENVIRONMENT ${environment}"

# Activate spack
. $JENKINS/activate_spack.sh

# Read compilers defined in stack for given environment
# and writes two files, one with each compiler spec in
# its own line (compilers-perline) and a second with all
# the compiler specs in a single row (compilers-inline).
spack readc -s ${STACK_RELEASE} -p ${environment}

echo "Contents of compilers.${environment}:"
cat compilers-inline.${environment}

echo ""
echo "Contents of compilers variable:"
compilers=$(cat compilers-inline.${environment})
echo $compilers

# We can remove --debug from the spack install
# command if the compilers are already installed.
echo "Installing compilers"
spack --debug install ${compilers}

echo "Adding stack compilers to ${SPACK_SYSTEM_CONFIG_PATH}/compilers.yaml"
while read -r line
do
    spec_path=$(spack location -i ${line})
    spack compiler find --scope system ${spec_path}
done <<< $(cat compilers-perline.${environment})

echo "============= COMPILERS DEBUG INFO ============="

echo "SPACK_SYSTEM_CONFIG_PATH: ${SPACK_SYSTEM_CONFIG_PATH}"

echo "spack config blame compilers"
spack config blame compilers

echo "spack compilers"
spack compilers

echo "cat ${SPACK_SYSTEM_CONFIG_PATH}/compilers.yaml:"
cat ${SPACK_SYSTEM_CONFIG_PATH}/compilers.yaml
