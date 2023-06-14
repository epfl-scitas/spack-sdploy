#!/bin/bash -l
set -euo pipefail

# Activating Spack
. $JENKINS/activate_spack.sh 2> /dev/null

if [ "$#" -eq 2 ]; then
    TOKENS=`yq -s '.[0].tokens + .[1].platform.tokens' stacks/${STACK_RELEASE}/common.yaml stacks/${STACK_RELEASE}/platforms/$2.yaml`
else
    TOKENS=`yq '.tokens' stacks/${STACK_RELEASE}/common.yaml`
fi

echo $TOKENS | yq -r ".$1"
