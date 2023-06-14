#!/bin/bash -l
set -euo pipefail

# Activating Spack
. $JENKINS/activate_spack.sh

# Gather values
LMOD_PREFIX=`yq .modules.roots.lmod stacks/${STACK_RELEASE}/common.yaml`

TOKENS=`yq -s '.[0].tokens + .[1].platform.tokens'  stacks/${STACK_RELEASE}/common.yaml stacks/${STACK_RELEASE}/platforms/${environment}.yaml`

LMOD_SUBDIR=`echo ${TOKENS} | yq .lmod_root`
ARCH=`echo ${TOKENS} | yq .lmod_arch`

INTEL_YAML=`yq '.intel.stable.compiler | split("@")' stacks/${STACK_RELEASE}/${STACK_RELEASE}.yaml`
COMPILER=`echo ${INTEL_YAML} | yq '.[0]'`
COMPILER_VER=`echo ${INTEL_YAML} | yq '.[1]'`
INTEL_SPEC_YAML=`yq '.intel.stable.compiler_spec | split("@")' stacks/${STACK_RELEASE}/${STACK_RELEASE}.yaml`
COMPILER_SPEC=`echo ${INTEL_SPEC_YAML} | yq '.[0]'`
COMPILER_SPEC_VER=`echo ${INTEL_SPEC_YAML} | yq '.[1]'`


# Compose values
LMOD_CORE=$STACK_PREFIX/$STACK_RELEASE_VER/$LMOD_PREFIX/${LMOD_SUBDIR}/${ARCH}/Core
LMOD_INTEL=$STACK_PREFIX/$STACK_RELEASE_VER/$LMOD_PREFIX/${LMOD_SUBDIR}/${ARCH}/intel

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

# What's happening ?
# ----------------
# step 0: make sure the directory `intel` exists (or create it)
# step 1: copy the module created for `intel-oneapi-compiler-classic` into `intel` directory
# step 2: add the missing directives to the new module
# step 3: backup the old module

# step 0
if [ -e ${LMOD_CORE}/${COMPILER_SPEC}/${COMPILER_SPEC_VER}.lua ]; then
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
