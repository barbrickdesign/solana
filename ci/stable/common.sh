#!/usr/bin/env bash
#
# Common CI configuration for stable channel tests
# Sets up Rust environment with strict error checking
#
set -e

export RUST_BACKTRACE=1
export RUSTFLAGS="-D warnings"

source ci/_
