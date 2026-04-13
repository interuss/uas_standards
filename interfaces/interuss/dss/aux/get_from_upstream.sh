#!/bin/bash

OS=$(uname)
if [[ $OS == "Darwin" ]]; then
	# OSX uses BSD readlink
	BASEDIR="$(dirname "$0")"
else
	BASEDIR=$(readlink -e "$(dirname "$0")")
fi

cd "${BASEDIR}" || exit

# URL to raw content for this interface.  Should target pinned content: either a tag or commit.
URL="https://raw.githubusercontent.com/interuss/dss/refs/tags/interuss/dss/v0.21.1/interfaces/aux_/aux_.yaml"

wget -N $URL
