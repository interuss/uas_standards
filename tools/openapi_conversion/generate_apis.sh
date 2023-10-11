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

echo "F3411-19"
docker container run -it \
  	-v "$(pwd)/../..:/resources" \
	  openapi-python-converter \
	      --api /resources/interfaces/astm/f3411/v19/remoteid/augmented.yaml \
	      --python_output /resources/src/uas_standards/astm/f3411/v19/api.py

echo "F3411-22a"
docker container run -it \
  	-v "$(pwd)/../..:/resources" \
	  openapi-python-converter \
	      --api /resources/interfaces/astm/f3411/v22a/remoteid/updated.yaml \
	      --python_output /resources/src/uas_standards/astm/f3411/v22a/api.py

echo "F3548-21"
docker container run -it \
  	-v "$(pwd)/../..:/resources" \
	  openapi-python-converter \
	      --api /resources/interfaces/astm/f3548/v21/utm.yaml \
	      --python_output /resources/src/uas_standards/astm/f3548/v21/api.py

echo "Geo-awareness automated testing"
docker container run -it \
  	-v "$(pwd)/../..:/resources" \
	  openapi-python-converter \
	      --api /resources/interfaces/interuss/automated_testing/geo-awareness/v1/geo-awareness.yaml \
	      --python_output /resources/src/uas_standards/interuss/automated_testing/geo_awareness/v1/api.py

echo "RID injection automated testing"
docker container run -it \
  	-v "$(pwd)/../..:/resources" \
	  openapi-python-converter \
	      --api /resources/interfaces/interuss/automated_testing/rid/v1/injection.yaml \
	      --python_output /resources/src/uas_standards/interuss/automated_testing/rid/v1/injection.py

echo "RID observation automated testing"
docker container run -it \
  	-v "$(pwd)/../..:/resources" \
	  openapi-python-converter \
	      --api /resources/interfaces/interuss/automated_testing/rid/v1/observation.yaml \
	      --python_output /resources/src/uas_standards/interuss/automated_testing/rid/v1/observation.py

echo "SCD automated testing"
mkdir -p $(pwd)/../../src/uas_standards/interuss/automated_testing/scd/v1
docker container run -it \
  	-v "$(pwd)/../..:/resources" \
	  openapi-python-converter \
	      --api /resources/interfaces/interuss/automated_testing/scd/v1/scd.yaml \
	      --python_output /resources/src/uas_standards/interuss/automated_testing/scd/v1/api.py

echo "Geospatial map automated testing"
mkdir -p $(pwd)/../../src/uas_standards/interuss/automated_testing/geospatial_map/v1
docker container run -it \
  	-v "$(pwd)/../..:/resources" \
	  openapi-python-converter \
	      --api /resources/interfaces/interuss/automated_testing/geospatial_map/v1/geospatial_map.yaml \
	      --python_output /resources/src/uas_standards/interuss/automated_testing/geospatial_map/v1/api.py

echo "Flight planning automated testing"
mkdir -p $(pwd)/../../src/uas_standards/interuss/automated_testing/flight_planning/v1
docker container run -it \
  	-v "$(pwd)/../..:/resources" \
	  openapi-python-converter \
	      --api /resources/interfaces/interuss/automated_testing/flight_planning/v1/flight_planning.yaml \
	      --python_output /resources/src/uas_standards/interuss/automated_testing/flight_planning/v1/api.py

echo "Versioning for automated testing"
mkdir -p $(pwd)/../../src/uas_standards/interuss/automated_testing/versioning
docker container run -it \
  	-v "$(pwd)/../..:/resources" \
	  openapi-python-converter \
	      --api /resources/interfaces/interuss/automated_testing/versioning/versioning.yaml \
	      --python_output /resources/src/uas_standards/interuss/automated_testing/versioning/api.py
