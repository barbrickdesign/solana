#!/usr/bin/env bash
#
# Install rsync for remote file synchronization
# Required for deployment and backup operations
#
set -ex

[[ $(uname) = Linux ]] || exit 1
[[ $USER = root ]] || exit 1

apt-get --assume-yes install rsync
