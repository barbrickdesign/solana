# shellcheck shell=bash
# |source| this file
#
# SPL Token CLI version configuration (populate this on the stable branch)
#
splTokenCliVersion=

maybeSplTokenCliVersionArg=
if [[ -n "$splTokenCliVersion" ]]; then
    # shellcheck disable=SC2034
    maybeSplTokenCliVersionArg="--version $splTokenCliVersion"
fi
