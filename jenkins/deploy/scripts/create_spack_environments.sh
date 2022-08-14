#!/bin/bash -l

echo 'Activating Spack'
. $JENKINS_SCRIPTS_PATH/activate_spack.sh

spack create-environments
