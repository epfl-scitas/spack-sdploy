#!/bin/bash -l
set -euo pipefail

# Activate spack
. $JENKINS/activate_spack.sh

# Read compilers defined in stack for given environment
# and writes two files, one with each compiler spec in
# its own line (compilers-perline) and a second with all
# the compiler specs in a single row (compilers-inline).
spack -e ${environment} list-compilers -s ${STACK_RELEASE} | tee compilers.list


compilers=$(cat compilers.list)

# We can remove --debug from the spack install
# command if the compilers are already installed.
echo "Installing compilers"
spack spec -Ilt ${compilers}

echo "spack install --log-format junit --log-file install_compilers.xml ${compilers}"
spack install --log-format junit --log-file install_compilers.xml ${compilers}

echo "Adding stack compilers to ${SPACK_SYSTEM_CONFIG_PATH}/compilers.yaml"
while read -r spec
do
    spec_path=$(spack location -i ${spec})
    echo "spack compiler find --scope system ${spec_path} || true"

    if [[ "$spec" =~ "intel@" ]]; then
	compiler_add=1
	if [ -e ${SPACK_SYSTEM_CONFIG_PATH}/compilers.yaml ]; then
	    grep -q ${spec_path} ${SPACK_SYSTEM_CONFIG_PATH}/compilers.yaml
	    if [ $? -eq 0 ]; then
		compiler_add=0
	    fi
	fi
	if [ ${compiler_add} -eq 1 ]; then
	    spack compiler find --scope system ${spec_path} || true
	fi
	version=$(${spec_path}/bin/icc --version | grep ICC | sed 's/icc (ICC) \([0-9.]*\) .*/\1/')
	spec_version=$(echo $spec |  sed 's/intel@\([0-9.]*\).*/\1/')
	sed -i -e "s/intel@${version}/intel@${spec_version}/" ${SPACK_SYSTEM_CONFIG_PATH}/compilers.yaml
    else
	spack compiler find --scope system ${spec_path} || true
    fi
done <<< $(cat compilers.list)

# Hack for intel compiler.
#  >>> to modify the following files: ifort.cfg, icc.cfg and icpc.cfg.
#  files location: intel-oneapi-compilers-2022.1.0-67zhngwawhy57xzjpoc5mwbj6vzsk6jp/compiler/2022.1.0/linux/bin/intel64
#  ifort.cfg (overwrite): 
#  -isystem/ssoft/spack/syrah/v1/opt/spack/linux-rhel8-x86_64_v2/gcc-8.5.0/intel-oneapi-compilers-classic-2021.6.0-q3mi2mylw3zyuht6p72u25ruqnpptpym/compiler/include/intel64
#  icc.cfg/icpc.cfg (overwrite):
#  -isystem/ssoft/spack/syrah/v1/opt/spack/linux-rhel8-x86_64_v2/gcc-8.5.0/intel-oneapi-compilers-classic-2021.6.0-q3mi2mylw3zyuht6p72u25ruqnpptpym/compiler/include/icc

DST_DIR=`spack location -i intel-oneapi-compilers`/compiler/2022.1.0/linux/bin/intel64
CONTENT=`spack location -i intel-oneapi-compilers-classic`/compiler/include
echo -isystem$CONTENT/intel64 > $DST_DIR/ifort.cfg
echo -isystem$CONTENT/icc > $DST_DIR/icc.cfg
echo -isystem$CONTENT/icc > $DST_DIR/icpc.cfg
# ~end of hack~

echo "============= COMPILERS DEBUG INFO ============="

echo "SPACK_SYSTEM_CONFIG_PATH: ${SPACK_SYSTEM_CONFIG_PATH}"

echo "spack config blame compilers"
spack config blame compilers

echo "spack compilers"
spack compilers

echo "cat ${SPACK_SYSTEM_CONFIG_PATH}/compilers.yaml:"
cat ${SPACK_SYSTEM_CONFIG_PATH}/compilers.yaml
