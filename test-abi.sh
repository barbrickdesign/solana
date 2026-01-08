#!/usr/bin/env bash
#
# Run ABI (Application Binary Interface) tests for the repository
# Executes ABI compatibility tests to ensure binary interfaces remain stable
#
# Usage:
#   $0  - Run all ABI tests in the repository
#

here=$(dirname "$0")
set -x
exec "${here}/cargo" nightly test --lib -- test_abi_ --nocapture
