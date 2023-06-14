#!/bin/bash -l
set -euo pipefail

# Activating Spack
. $JENKINS/activate_spack.sh 2> /dev/null

TOKENS=`yq -s '.[0].tokens + .[1].platform.tokens'  stacks/${STACK_RELEASE}/common.yaml stacks/${STACK_RELEASE}/platforms/${environment}.yaml`
echo $TOKENS | yq -r ".$1"
