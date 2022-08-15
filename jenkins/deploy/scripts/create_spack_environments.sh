#!/bin/bash -l

echo 'Activating Spack'
. $JENKINS/activate_spack.sh

spack create-environments
