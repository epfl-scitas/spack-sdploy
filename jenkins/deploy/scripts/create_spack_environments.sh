#!/bin/bash -l

echo 'Activating Spack'
. $JENKINS/activate_spack.sh

# If the environments already exist, they will not be erased
spack create-environments
