#!/usr/bin/env bash

export WORK_DIR_INTERNAL=`cat stacks/${STACK}/common.yaml |grep work_directory: | cut -n -d " " -f 2`

set +u
if [ "x${WORK_DIR}" == "x" ]; then
    export WORK_DIR=${WORK_DIR_INTERNAL}
fi
if [ "x${IN_PR}" == "x" ]; then
    set +e
    IN_PR=`[ "${WORK_DIR}" != "${WORK_DIR_INTERNAL}" ]`
    set -e
fi
set -u

export IN_PR

export STACK_RELEASE=`cat stacks/${STACK}/common.yaml |grep stack_release: | cut -n -d " " -f 2`
export STACK_RELEASE_VER=`cat stacks/${STACK}/common.yaml |grep stack_version: | cut -n -d " " -f 2`

export PYTHON_VENV_SUFFIX=`cat stacks/${STACK}/common.yaml |grep python_venv: | cut -n -d " " -f 2`

export SPACK_RELEASE=`cat stacks/${STACK}/common.yaml |grep spack_release: | cut -n -d " " -f 2`
export SPACK_EXTENSION=`cat stacks/${STACK}/common.yaml |grep extensions: | cut -n -d " " -f 2`
export SPACK_PATH=`cat stacks/${STACK}/common.yaml |grep spack: | cut -n -d " " -f 2`
export SPACK_SDPLOY=`cat stacks/${STACK}/common.yaml |grep spack_sdploy: | cut -n -d " " -f 2`

# Composed variables (from above values).
export STACK_PREFIX="${WORK_DIR}/${STACK_RELEASE}"

export PYTHON_VIRTUALENV_PATH="${STACK_PREFIX}/${PYTHON_VENV_SUFFIX}"

export SPACK_INSTALL_PATH="${STACK_PREFIX}/${SPACK_PATH}.${STACK_RELEASE_VER}"
export SPACK_SDPLOY_INSTALL_PATH="${STACK_PREFIX}/${SPACK_SDPLOY}"
export SPACK_BUILDCACHE_PATH="${STACK_PREFIX}/buildcache"
