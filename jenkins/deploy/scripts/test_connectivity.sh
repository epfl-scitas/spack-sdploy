#!/usr/bin/env bash

wget --timeout=3 -v www.google.ch -O /tmp/index.html

if [ $? -eq 0 ]; then
    rm /tmp/index.html
    exit 0
else
    env | grep -i proxy
    exit -1
fi
