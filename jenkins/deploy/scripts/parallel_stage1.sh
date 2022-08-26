#!/usr/bin/env bash
set -euo pipefail

environment=$(echo $NODE_LABELS | cut -d '-' -f 1)

echo "Running the 1st stage in parallel for env ${environment} of ${STACK_RELEASE}"
