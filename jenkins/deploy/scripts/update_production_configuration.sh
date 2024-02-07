#!/bin/bash -l
set -euo pipefail

. ${JENKINS}/setenv.sh

echo "Installing Python virtual environment ${PYTHON_VIRTUALENV_PATH}"
mkdir -p ${PYTHON_VIRTUALENV_PATH}
python3 -m venv ${PYTHON_VIRTUALENV_PATH}

echo 'Activating Python virtual environment'
. ${PYTHON_VIRTUALENV_PATH}/bin/activate

echo 'Upgrading PIP'
pip install -U pip

echo 'Installing Jinja2'
pip install jinja2 jq yq

curl -L --output ${PYTHON_VIRTUALENV_PATH}/bin/jq https://github.com/jqlang/jq/releases/download/jq-1.7.1/jq-linux-amd64 
chmod +x ${PYTHON_VIRTUALENV_PATH}/bin/jq

#echo 'Installing yareed'
#pip install yareed/
