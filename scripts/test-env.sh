#!/bin/sh

export kongAdminAPI="http://127.0.0.1:8001"
export kongKey=$(cat /proc/sys/kernel/random/uuid |tr -d -)
export kongSecret=$(cat /proc/sys/kernel/random/uuid |tr -d -)
export UserName=$(cat /dev/urandom | tr -dc 'a-z' | fold -w 6 | head -n 1)
export WritePassword=$(cat /dev/urandom | tr -dc 'a-zA-Z0-9' | fold -w 10 | head -n 1)
exec $SHELL -i
