#!/bin/bash -l
set -euo pipefail

# This script assumes that the following variables are set in the environment:
#
# PYTHON_VIRTUALENV_PATH: path where to setup the Python virtual environment
#
#

echo 'Installing Python virtual environment'
mkdir -p ${PYTHON_VIRTUALENV_PATH}
python3 -m venv ${PYTHON_VIRTUALENV_PATH}

echo 'Activating Python virtual environment'
. ${PYTHON_VIRTUALENV_PATH}/bin/activate

echo 'Upgrading PIP'
pip install -U pip

echo 'Installing Jinja2'
pip install jinja2

echo 'Installing yareed'
pip install yareed/
