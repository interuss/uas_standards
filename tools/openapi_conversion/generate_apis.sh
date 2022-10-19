#!/usr/bin/env bash

OS=$(uname)
if [[ $OS == "Darwin" ]]; then
	# OSX uses BSD readlink
	BASEDIR="$(dirname "$0")"
else
	BASEDIR=$(readlink -e "$(dirname "$0")")
fi

cd "${BASEDIR}" || exit

docker image build -t openapi-python-converter .

docker container run -it \
  	-v "$(pwd)/../..:/resources" \
	  openapi-python-converter \
	      --api /resources/interfaces/astm/f3411/v19/remoteid/augmented.yaml \
	      --python_output /resources/src/uas_standards/astm/f3411/v19/api.py

docker container run -it \
  	-v "$(pwd)/../..:/resources" \
	  openapi-python-converter \
	      --api /resources/interfaces/astm/f3411/v22a/remoteid/updated.yaml \
	      --python_output /resources/src/uas_standards/astm/f3411/v22a/api.py

docker container run -it \
  	-v "$(pwd)/../..:/resources" \
	  openapi-python-converter \
	      --api /resources/interfaces/astm/f3548/v21/utm.yaml \
	      --python_output /resources/src/uas_standards/astm/f3548/v21/api.py
