#!/usr/bin/env bash
#
# Install The Silver Searcher (ag) - fast code searching tool
# ag is used for quick grep-like searches across the codebase
#
set -ex

[[ $(uname) = Linux ]] || exit 1
[[ $USER = root ]] || exit 1

apt-get update
apt-get --assume-yes install silversearcher-ag
