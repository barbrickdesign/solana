#!/usr/bin/env bash
#
# Formats a URL to be clickable from a Buildkite log
# When running in Buildkite CI, wraps URLs with ANSI escape codes to make them clickable
#
# Usage: $0 <url>
#

if [[ $# -eq 0 ]]; then
  echo "Usage: $0 url"
  exit 1
fi

if [[ -z $BUILDKITE ]]; then
  echo "$1"
else
  # shellcheck disable=SC2001
  URL="$(echo "$1" | sed 's/;/%3b/g')" # Escape semicolons for URL

  printf '\033]1339;url='
  echo -n "$URL"
  printf '\a\n'
fi
