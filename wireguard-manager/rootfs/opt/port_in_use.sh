#!/bin/bash

TYPE=$(echo $1 | tr '[:upper:]' '[:lower:]')
PORT=$2
PORTS_IN_USE=$(netstat -lntu)
REGEX='s/.*:([0-9]+)\>.*/\1/p}'

for p in $(echo "${PORTS_IN_USE[@]}" | sed -rne "/^$TYPE/ $REGEX"); do
    if [ $p -eq $PORT ]; then
        exit 1
    fi
done