#!/bin/bash -l
set -euo pipefail

environment=$(echo $NODE_LABELS | cut -d '-' -f 1)
echo "ENVIRONMENT ${environment}"

# Activate spack
. $JENKINS/activate_spack.sh

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

echo "Adding stack compilers"
while read -r line
do
    spec_path=$(spack location -i ${line})
    spack compiler find --scope system ${spec_path}
done <<< $(cat compilers-perline.${environment})
