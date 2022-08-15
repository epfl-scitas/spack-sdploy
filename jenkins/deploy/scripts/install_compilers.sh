#!/bin/bash -l

echo 'Activating Spack'
. $JENKINS/activate_spack.sh

echo "Running in environment: ${environment}"

spack --env ${environment} install-c
