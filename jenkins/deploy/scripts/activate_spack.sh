#!/bin/bash -l

echo 'Activating Python virtual environment'
. ${PYTHON_VIRTUALENV_PATH}/bin/activate

#echo 'Load variables'
#. $JENKINS_SCRIPTS_PATH/config.sh

echo 'Source Spack'
. $SPACK_INSTALL_PATH/share/spack/setup-env.sh

spack --version

