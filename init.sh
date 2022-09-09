#
#
#
#
#
# CONFIGURATION
export STACK=mkl
export ENVIRONMENT=avx2

# Variables needed to run this script
_BASE_DIR="."

set_base_dir () {
    _pwd=`pwd`
    cd ${_BASE_DIR}
    BASE_DIR=`pwd`
    cd ${_pwd}
}

set_base_dir
echo "spack-sdploy found: ${BASE_DIR}"

# Variables read from commons.yaml using cat, grep and cut.
export WORK_DIR=`cat ${BASE_DIR}/stacks/${STACK}/common.yaml |grep work_directory: | cut -n -d " " -f 2`
export STACK_RELEASE=`cat ${BASE_DIR}/stacks/${STACK}/common.yaml |grep stack_release: | cut -n -d " " -f 2`
export PYTHON_VENV=`cat ${BASE_DIR}/stacks/${STACK}/common.yaml |grep python_venv: | cut -n -d " " -f 2`
export SPACK_RELEASE=`cat ${BASE_DIR}/stacks/${STACK}/common.yaml |grep spack_release: | cut -n -d " " -f 2`
export SPACK_EXTENSION=`cat ${BASE_DIR}/stacks/${STACK}/common.yaml |grep extensions: | cut -n -d " " -f 2`
export STACK_RELEASE_VER=`cat ${BASE_DIR}/stacks/${STACK}/common.yaml |grep stack_version: | cut -n -d " " -f 2`
export SPACK_PATH=`cat ${BASE_DIR}/stacks/${STACK}/common.yaml |grep spack: | cut -n -d " " -f 2`
export SPACK_SDPLOY=`cat ${BASE_DIR}/stacks/${STACK}/common.yaml |grep spack_sdploy: | cut -n -d " " -f 2`

# Composed variables (from above values).
export STACK_PREFIX="${WORK_DIR}/${STACK_RELEASE}"
export PYTHON_VIRTUALENV_PATH="${STACK_PREFIX}/${PYTHON_VENV}"
export SPACK_INSTALL_PATH="${STACK_PREFIX}/${SPACK_PATH}.${STACK_RELEASE_VER}"
export SPACK_SDPLOY_INSTALL_PATH="${STACK_PREFIX}/${SPACK_SDPLOY}"
export SYSTEM_CONFIG_PREFIX="${STACK_PREFIX}/${STACK_RELEASE_VER}/config"

# Because this script is adapted from the Jenkins Pipiline, the environment
# names must be pulled from a variable called NODE_LABELS. This variable only
# exists in Jenkins environment and therefor we must create it artificially
# here. If the name of the environment is called "abc", then the value in the
# variable NODE_LABELS must be "abc-abc"
export NODE_LABELS=${ENVIRONMENT}-${ENVIRONMENT}

export JENKINS=jenkins/deploy/scripts
export _PREFIX=${BASE_DIR}/${JENKINS}

echo "Configuration:"
echo "WORK_DIR: $WORK_DIR"
echo "STACK_RELEASE: $STACK_RELEASE"
echo "PYTHON_VENV: ${PYTHON_VENV}"
echo "SPACK_RELEASE: ${SPACK_RELEASE}"
echo "SPACK_EXTENSION: ${SPACK_EXTENSION}"
echo "STACK_RELEASE_VER: ${STACK_RELEASE_VER}"
echo "SPACK_PATH: ${SPACK_PATH}"
echo "SPACK_SDPLOY: ${SPACK_SDPLOY}"

echo "STACK_PREFIX: ${STACK_PREFIX}"
echo "PYTHON_VIRTUALENV_PATH: ${PYTHON_VIRTUALENV_PATH}"
echo "SPACK_INSTALL_PATH: ${SPACK_INSTALL_PATH}"
echo "SPACK_SDPLOY_INSTALL_PATH: ${SPACK_SDPLOY_INSTALL_PATH}"
echo "SYSTEM_CONFIG_PREFIX: ${SYSTEM_CONFIG_PREFIX}"

echo "STACK: ${STACK}"
echo "ENVIRONMENT: ${ENVIRONMENT}"
echo "NODE_LABELS: ${NODE_LABELS}"

# STEP 1
${_PREFIX}/update_production_configuration.sh

# STEP 2
${_PREFIX}/install_spack.sh

# STEP 3
${_PREFIX}/install_spack_sdploy.sh

# STEP 4
${_PREFIX}/clone_external_repos.sh

# STEP 5
${_PREFIX}/init_environment.sh

# STEP 6
${_PREFIX}/install_compilers_parallel.sh

# STEP 7
${_PREFIX}/concretize.sh

# STEP 8
${_PREFIX}/add_mirror.sh

# STEP 9
${_PREFIX}/install_stack.sh
