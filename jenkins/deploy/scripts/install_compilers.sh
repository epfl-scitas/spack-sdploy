#!/bin/bash -l
set -euo pipefail

environment=$(echo $NODE_LABELS | cut -d '-' -f 1)
echo "ENVIRONMENT ${environment}"

echo 'Activating Spack'
. $JENKINS/activate_spack.sh

echo 'Installing License'
# If directory already exists, remove it
SOURCE_PATH=${SPACK_SDPLOY_INSTALL_PATH}/external/licenses/intel
LICENSE_PATH=${SPACK_INSTALL_PATH}/etc/spack/licenses/intel
if [ ! -d ${LICENSE_PATH} ]; then
    mkdir -p ${LICENSE_PATH}
    cp ${SOURCE_PATH}/USE_SERVER.lic ${LICENSE_PATH}/license.lic
else
    rm -r ${LICENSE_PATH}
    mkdir -p ${LICENSE_PATH}
    cp ${SOURCE_PATH}/USE_SERVER.lic ${LICENSE_PATH}/license.lic
fi

spack readc -s ${STACK_RELEASE} -p ${environment}

echo "Contents of compilers.${environment}:"
cat compilers-inline.${environment}

echo ""
echo "Contents of compilers variable:"
compilers=$(cat compilers-inline.${environment})
echo $compilers

echo "Reporting BEFORE installing compilers:"
cat $(spack location -e $environment)/spack.yaml

echo "Installing compilers"
spack -v --env ${environment} install ${compilers}

echo "Reporting BEFORE modules generation:"
cat $(spack location -e $environment)/spack.yaml

echo "Add seen in spack-packagelist"
spack -v --env ${environment} module lmod refresh -y ${compilers}

echo "Reporting BEFORE while loop:"
cat $(spack location -e $environment)/spack.yaml

echo "Adding stack compilers"
while read -r line
do
    spec_path=$(spack location -i ${line})
    spack compiler find --scope system ${spec_path}
done <<< $(cat compilers-perline.${environment})

echo "Reporting AFTER while loop:"
cat $(spack location -e $environment)/spack.yaml

echo "spack  blame compilers before sed:"
spack config blame compilers

sed -i 's/intel@19.1.3.304/intel@20.0.4/' ${SPACK_SYSTEM_CONFIG_PATH}/compilers.yaml

echo "spack  blame compilers after sed:"
spack config blame compilers

echo "Reporting BEFORE system compiler I:"
# already has the extra compiler lines in spack.yaml
cat $(spack location -e $environment)/spack.yaml

echo "Adding system compiler I"
spack compiler find --scope system
cat $(spack location -e ${environment})/spack.yaml

echo "Reporting BEFORE system compiler II:"
cat $(spack location -e $environment)/spack.yaml

#echo "Adding system compiler II"
#spack compiler find --env
#cat $(spack location -e ${environment})/spack.yaml

echo "Reporting AT THE END:"
cat $(spack location -e $environment)/spack.yaml
