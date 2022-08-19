#!bin/bash

# This variable is used to define the what's below
STACK_PATH=/work/scitas-ge/erothe/work_dir/spack-sdploy/stacks/sizar

WORK_DIR=`cat ${STACK_PATH}/common.yaml |grep work_directory: | cut -n -d " " -f 2`
STACK_RELEASE=`cat ${STACK_PATH}/common.yaml |grep stack_release: | cut -n -d " " -f 2`
PYTHON_VENV=`cat ${STACK_PATH}/common.yaml |grep python_venv: | cut -n -d " " -f 2`
JENKINS=`cat ${STACK_PATH}/common.yaml |grep jenkins: | cut -n -d " " -f 2`
SPACK_RELEASE=`cat ${STACK_PATH}/common.yaml |grep spack_release: | cut -n -d " " -f 2`
SPACK_EXTENSION=`cat ${STACK_PATH}/common.yaml |grep extensions: | cut -n -d " " -f 2`
STACK_RELEASE_VER=`cat ${STACK_PATH}/common.yaml |grep stack_version: | cut -n -d " " -f 2`
SPACK_PATH=`cat ${STACK_PATH}/common.yaml |grep spack: | cut -n -d " " -f 2`
SPACK_SDPLOY=`cat ${STACK_PATH}/common.yaml |grep spack_sdploy: | cut -n -d " " -f 2`

# Composed variables (from above values).
export PYTHON_VIRTUALENV_PATH="${WORK_DIR}/${STACK_RELEASE}/${PYTHON_VENV}"
export STACK_PREFIX="${WORK_DIR}/${STACK_RELEASE}"
export STACK_INSTALL_PATH="${WORK_DIR}/${STACK_RELEASE}/${SPACK_PATH}.${STACK_RELEASE_VER}"
export SPACK_INSTALL_PATH="${WORK_DIR}/${STACK_RELEASE}/${SPACK_PATH}.${STACK_RELEASE_VER}"
export SPACK_USER_CONFIG_PATH="${WORK_DIR}/${STACK_RELEASE}/${SPACK_EXTENSION}"
export SPACK_SYSTEM_CONFIG_PATH="${WORK_DIR}/${STACK_RELEASE}/${SPACK_EXTENSION}"
export SPACK_SDPLOY_INSTALL_PATH="${WORK_DIR}/${STACK_RELEASE}/${SPACK_SDPLOY}"
export SPACK_DEFAULT_CONFIG_PATH="${SPACK_INSTALL_PATH}/etc/spack"
