#!/bin/bash -l
set -euo pipefail

# Activating Spack
. $JENKINS/activate_spack.sh

# Gather values
LMOD_PREFIX=`yq -r '.modules.roots.lmod' stacks/${STACK_RELEASE}/common.yaml`

TOKENS=`yq -r -s '.[0].tokens + .[1].platform.tokens'  stacks/${STACK_RELEASE}/common.yaml stacks/${STACK_RELEASE}/platforms/${environment}.yaml`

LMOD_SUBDIR=`echo ${TOKENS} | yq -r .lmod_root`
ARCH=`echo ${TOKENS} | yq -r .lmod_arch`

INTEL_YAML=`yq -r '.intel.stable.compiler | split("@")' stacks/${STACK_RELEASE}/${STACK_RELEASE}.yaml`
COMPILER=`echo ${INTEL_YAML} | yq -r '.[0]'`
COMPILER_VER=`echo ${INTEL_YAML} | yq -r '.[1]'`
INTEL_SPEC_YAML=`yq -r '.intel.stable.compiler_spec | split("@")' stacks/${STACK_RELEASE}/${STACK_RELEASE}.yaml`
COMPILER_SPEC=`echo ${INTEL_SPEC_YAML} | yq -r '.[0]'`
COMPILER_SPEC_VER=`echo ${INTEL_SPEC_YAML} | yq -r '.[1]'`


LMOD_MODULES_PREFIX=$STACK_PREFIX/$STACK_RELEASE_VER/$LMOD_PREFIX/${LMOD_SUBDIR}/${ARCH}
# Compose values
LMOD_CORE=${LMOD_MODULES_PREFIX}/Core
LMOD_INTEL=${LMOD_MODULES_PREFIX}/intel

# Show final values
echo "LMOD_CORE: $LMOD_CORE"
echo "LMOD_INTEL: $LMOD_INTEL"
echo "COMPILER: $COMPILER"
echo "COMPILER_VER: $COMPILER_VER"
echo "COMPILER_SPEC: $COMPILER_SPEC"
echo "COMPILER_SPEC_VER: $COMPILER_SPEC_VER"

echo "Creating modules"
# we can pass -e ${environment} to the spack command
spack --env ${environment} module lmod refresh -y

echo "Correcting LLVM module"
LLVM_LMOD_PATH=${LMOD_MODULES_PREFIX}/gcc/`yq -r '.gcc.stable.compiler | split("@") | .[1]' stacks/syrah/syrah.yaml`/llvm/15.0.2-julia.lua
if [ -e ${LLVM_LMOD_PATH} ]; then
    cat ${LLVM_LMOD_PATH} | grep -v family | grep -v MODULEPATH > /tmp/llvm-15.0.2-julia.lua

    mv /tmp/llvm-15.0.2-julia.lua ${LLVM_LMOD_PATH}
fi

# What's happening ?
# ----------------
# step 0: make sure the directory `intel` exists (or create it)
# step 1: copy the module created for `intel-oneapi-compiler-classic` into `intel` directory
# step 2: add the missing directives to the new module
# step 3: backup the old module

# step 0
if [ -e ${LMOD_CORE}/${COMPILER_SPEC}/${COMPILER_SPEC_VER}.lua ]; then
    echo "Correcting Intel module"
    mkdir -p ${LMOD_CORE}/${COMPILER}

    # step 1
    cp -f ${LMOD_CORE}/${COMPILER_SPEC}/${COMPILER_SPEC_VER}.lua ${LMOD_CORE}/${COMPILER}/${COMPILER_VER}.lua

    # step 2
    cat >> ${LMOD_CORE}/${COMPILER}/${COMPILER_VER}.lua<<-EOL
	-- Services provided by the package
	family("compiler")

	-- Loading this module unlocks the path below unconditionally
	prepend_path("MODULEPATH", "${LMOD_INTEL}/${COMPILER_VER}")
	EOL

    # step 3
    mv ${LMOD_CORE}/${COMPILER_SPEC}/${COMPILER_SPEC_VER}.lua ${LMOD_CORE}/${COMPILER_SPEC}/${COMPILER_SPEC_VER}.lua.bckp
fi
