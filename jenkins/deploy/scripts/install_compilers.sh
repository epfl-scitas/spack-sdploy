#!/bin/bash -l

echo 'Activating Spack'
. $JENKINS/activate_spack.sh

yareed -file stacks/common.yaml -keys environments

#spack install-compilers --templates stacks/syrah-lite/templates
#mv spack.yaml /home/scitasbuildpr/syrah/spack.v1/var/spack/environments/ph02-avx
#env
