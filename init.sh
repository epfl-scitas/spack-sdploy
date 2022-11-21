#!/bin/bash
set -eo pipefail
option=$1
set -u
#
#
#
#
#
# CONFIGURATION
export STACK=syrah
export ENVIRONMENT=jed

# Variables needed to run this script
_BASE_DIR="."

BASE_DIR=`realpath ${_BASE_DIR}`
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

LOGS=${WORK_DIR}/logs
mkdir -p ${LOGS}

execution_timestamp=`date +%y%m%d.%H%m%M`
echo "Execution timestamp: ${execution_timestamp}"
echo
echo '  _________________________________________   ____ '
echo ' /   _____/\__    ___/\_   _____/\______   \ /_   |'
echo ' \_____  \   |    |    |    __)_  |     ___/  |   |'
echo ' /        \  |    |    |        \ |    |      |   |'
echo '/_______  /  |____|   /_______  / |____|      |___|'
echo '        \/                    \/                   '
echo
echo '> update_production_configuration.sh'
echo
${_PREFIX}/update_production_configuration.sh 2>&1 | tee ${LOGS}/01_update_production_configuration.${execution_timestamp}.log

echo '  _________________________________________  ________  '
echo ' /   _____/\__    ___/\_   _____/\______   \ \_____  \ '
echo ' \_____  \   |    |    |    __)_  |     ___/  /  ____/ '
echo ' /        \  |    |    |        \ |    |     /       \ '
echo '/_______  /  |____|   /_______  / |____|     \_______ \'
echo '        \/                    \/                     \/'
echo
echo '> install_spack.sh'
echo
${_PREFIX}/install_spack.sh 2>&1 | tee ${LOGS}/02_install_spack.${execution_timestamp}.log

echo '  _________________________________________  ________  '
echo ' /   _____/\__    ___/\_   _____/\______   \ \_____  \ '
echo ' \_____  \   |    |    |    __)_  |     ___/   _(__  < '
echo ' /        \  |    |    |        \ |    |      /       \'
echo '/_______  /  |____|   /_______  / |____|     /______  /'
echo '        \/                    \/                    \/ '
echo
echo '> install_spack_sdploy.sh'
echo
${_PREFIX}/install_spack_sdploy.sh 2>&1 | tee ${LOGS}/03_install_spack_sdploy.${execution_timestamp}.log


echo '  _________________________________________     _____  '
echo ' /   _____/\__    ___/\_   _____/\______   \   /  |  | '
echo ' \_____  \   |    |    |    __)_  |     ___/  /   |  |_'
echo ' /        \  |    |    |        \ |    |     /    ^   /'
echo '/_______  /  |____|   /_______  / |____|     \____   | '
echo '        \/                    \/                  |__| '
echo
echo '> clone_external_repos.sh'
echo
${_PREFIX}/clone_external_repos.sh 2>&1 | tee ${LOGS}/04_clone_external_repos.${execution_timestamp}.log

echo '  _________________________________________   .________'
echo ' /   _____/\__    ___/\_   _____/\______   \  |   ____/'
echo ' \_____  \   |    |    |    __)_  |     ___/  |____  \ '
echo ' /        \  |    |    |        \ |    |      /       \'
echo '/_______  /  |____|   /_______  / |____|     /______  /'
echo '        \/                    \/                    \/ '
echo
echo '> init_environment.sh'
echo
${_PREFIX}/init_environment.sh 2>&1 | tee ${LOGS}/05_init_environment.${execution_timestamp}.log

echo '  _________________________________________    ________'
echo ' /   _____/\__    ___/\_   _____/\______   \  /  _____/'
echo ' \_____  \   |    |    |    __)_  |     ___/ /   __  \ '
echo ' /        \  |    |    |        \ |    |     \  |__\  \'
echo '/_______  /  |____|   /_______  / |____|      \_____  /'
echo '        \/                    \/                    \/ '
echo
echo '> install_compilers_parallel.sh'
echo
${_PREFIX}/install_compilers_parallel.sh 2>&1 | tee ${LOGS}/06_install_compilers_parallel.${execution_timestamp}.log

echo '  _________________________________________  _________ '
echo ' /   _____/\__    ___/\_   _____/\______   \ \______  \'
echo ' \_____  \   |    |    |    __)_  |     ___/     /    /'
echo ' /        \  |    |    |        \ |    |        /    / '
echo '/_______  /  |____|   /_______  / |____|       /____/  '
echo '        \/                    \/                       '
echo
echo '> concretize.sh'
echo
${_PREFIX}/concretize.sh 2>&1 | tee ${LOGS}/07_concretize.${execution_timestamp}.log

if [[ $option = "concretize" ]]; then
    echo "program stopped at concretization step"
    return
fi

echo '  _________________________________________    ______  '
echo ' /   _____/\__    ___/\_   _____/\______   \  /  __  \ '
echo ' \_____  \   |    |    |    __)_  |     ___/  >      < '
echo ' /        \  |    |    |        \ |    |     /   --   \'
echo '/_______  /  |____|   /_______  / |____|     \______  /'
echo '        \/                    \/                    \/ '
echo
echo '> add_mirror.sh'
echo
${_PREFIX}/add_mirror.sh 2>&1 | tee ${LOGS}/08_add_mirror.${execution_timestamp}.log

echo '  _________________________________________   ________ '
echo ' /   _____/\__    ___/\_   _____/\______   \ /   __   \'
echo ' \_____  \   |    |    |    __)_  |     ___/ \____    /'
echo ' /        \  |    |    |        \ |    |        /    / '
echo '/_______  /  |____|   /_______  / |____|       /____/  '
echo '        \/                    \/                       '
echo
echo '> install_stack.sh'
echo
${_PREFIX}/install_stack.sh 2>&1 | tee ${LOGS}/09_install_stack.${execution_timestamp}.log
