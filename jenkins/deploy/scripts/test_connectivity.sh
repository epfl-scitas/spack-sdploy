#!/usr/bin/env bash
set -euo pipefail

wget -v www.google.ch -O /tmp/index.html

if [ -e /tmp/index.html ]; then
    rm /tmp/index.html
fi
