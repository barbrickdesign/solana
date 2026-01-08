#!/usr/bin/env bash
#
# Configure system timezone to America/Los_Angeles (Pacific Time)
# Ensures consistent timestamps across validator infrastructure
#
set -ex

[[ $(uname) = Linux ]] || exit 1
[[ $USER = root ]] || exit 1

ln -sf /usr/share/zoneinfo/America/Los_Angeles /etc/localtime
