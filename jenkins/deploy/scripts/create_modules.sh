#!/bin/bash -l
set -euo pipefail

# Activating Spack
. $JENKINS/activate_spack.sh

# Gather values
LMOD_PREFIX=`yareed -file stacks/${STACK_RELEASE}/common.yaml -keys modules roots lmod`
LMOD_SUBDIR=`yareed -file stacks/${STACK_RELEASE}/platforms/${environment}.yaml -keys platform tokens lmod_root`
ARCH=`yareed -file stacks/${STACK_RELEASE}/platforms/${environment}.yaml -keys platform tokens lmod_arch`
COMPILER=`yareed -file stacks/${STACK_RELEASE}/${STACK_RELEASE}.yaml -keys intel stable compiler |awk -F'@' '{print $1}'`
COMPILER_VER=`yareed -file stacks/${STACK_RELEASE}/${STACK_RELEASE}.yaml -keys intel stable compiler |awk -F'@' '{print $2}'`
COMPILER_SPEC=`yareed -file stacks/${STACK_RELEASE}/${STACK_RELEASE}.yaml -keys intel stable compiler_spec |awk -F'@' '{print $1}'`
COMPILER_SPEC_VER=`yareed -file stacks/${STACK_RELEASE}/${STACK_RELEASE}.yaml -keys intel stable compiler_spec |awk -F'@' '{print $2}'`

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
spack module lmod refresh -y

# What's happening ?
# ----------------
# step 1: create the new module
# step 2: add the missing directives to the new module
# step 3: backup the old module

# step 1
cp -r ${LMOD_CORE}/${COMPILER_SPEC} ${LMOD_CORE}/intel

# step 2
cat >> ${LMOD_CORE}/${COMPILER}/${COMPILER_VER}.lua<<EOL
-- Services provided by the package
family("compiler")

-- Loading this module unlocks the path below unconditionally
prepend_path("MODULEPATH", "${LMOD_INTEL}/${COMPILER_VER}")
EOL

# step 3
mv ${LMOD_CORE}/${COMPILER_SPEC}/${COMPILER_SPEC_VER}.lua ${LMOD_CORE}/${COMPILER_SPEC}/${COMPILER_SPEC_VER}.lua.bckp
