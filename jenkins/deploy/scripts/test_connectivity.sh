#!/usr/bin/env bash

wget -v www.google.ch -O /tmp/index.html

if [ -e /tmp/index.html ]; then
    rm /tmp/index.html
    exit 0
else
    env | grep -i proxy
    exit -1
fi
