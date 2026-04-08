#!/usr/bin/env bash

OS=$(uname)
if [[ $OS == "Darwin" ]]; then
	# OSX uses BSD readlink
	BASEDIR="$(dirname "$0")"
else
	BASEDIR=$(readlink -e "$(dirname "$0")")
fi

cd "${BASEDIR}/../.." || exit

USER_GROUP="$(id -u):$(id -g)"

docker image build --build-context root=. -t openapi-python-converter ./tools/openapi_conversion

mkdir -p .cache

echo "F3411-19"
mkdir -p $(pwd)/src/uas_standards/astm/f3411/v19
docker container run -it \
    -u ${USER_GROUP} -v "$(pwd):/resources" -v "$(pwd)/.cache:/.cache" \
	  openapi-python-converter \
	      --api /resources/interfaces/astm/f3411/v19/remoteid/augmented.yaml \
	      --python_output /resources/src/uas_standards/astm/f3411/v19/api.py

echo "F3411-22a"
mkdir -p $(pwd)/src/uas_standards/astm/f3411/v22a
docker container run -it \
    -u ${USER_GROUP} -v "$(pwd):/resources" -v "$(pwd)/.cache:/.cache" \
	  openapi-python-converter \
	      --api /resources/interfaces/astm/f3411/v22a/remoteid/updated.yaml \
	      --python_output /resources/src/uas_standards/astm/f3411/v22a/api.py

echo "F3548-21"
mkdir -p $(pwd)/src/uas_standards/astm/f3548/v21
docker container run -it \
    -u ${USER_GROUP} -v "$(pwd):/resources" -v "$(pwd)/.cache:/.cache" \
	  openapi-python-converter \
	      --api /resources/interfaces/astm/f3548/v21/utm.yaml \
	      --python_output /resources/src/uas_standards/astm/f3548/v21/api.py

echo "Geo-awareness automated testing"
mkdir -p $(pwd)/src/uas_standards/interuss/automated_testing/geo-awareness/v1
docker container run -it \
    -u ${USER_GROUP} -v "$(pwd):/resources" -v "$(pwd)/.cache:/.cache" \
	  openapi-python-converter \
	      --api /resources/interfaces/interuss/automated_testing/geo-awareness/v1/geo-awareness.yaml \
	      --python_output /resources/src/uas_standards/interuss/automated_testing/geo_awareness/v1/api.py

echo "RID injection automated testing"
mkdir -p $(pwd)/src/uas_standards/interuss/automated_testing/rid/v1
docker container run -it \
    -u ${USER_GROUP} -v "$(pwd):/resources" -v "$(pwd)/.cache:/.cache" \
	  openapi-python-converter \
	      --api /resources/interfaces/interuss/automated_testing/rid/v1/injection.yaml \
	      --python_output /resources/src/uas_standards/interuss/automated_testing/rid/v1/injection.py

echo "RID observation automated testing"
docker container run -it \
    -u ${USER_GROUP} -v "$(pwd):/resources" -v "$(pwd)/.cache:/.cache" \
	  openapi-python-converter \
	      --api /resources/interfaces/interuss/automated_testing/rid/v1/observation.yaml \
	      --python_output /resources/src/uas_standards/interuss/automated_testing/rid/v1/observation.py

echo "SCD automated testing"
mkdir -p $(pwd)/src/uas_standards/interuss/automated_testing/scd/v1
docker container run -it \
    -u ${USER_GROUP} -v "$(pwd):/resources" -v "$(pwd)/.cache:/.cache" \
	  openapi-python-converter \
	      --api /resources/interfaces/interuss/automated_testing/scd/v1/scd.yaml \
	      --python_output /resources/src/uas_standards/interuss/automated_testing/scd/v1/api.py

echo "Geospatial map automated testing"
mkdir -p $(pwd)/src/uas_standards/interuss/automated_testing/geospatial_map/v1
docker container run -it \
    -u ${USER_GROUP} -v "$(pwd):/resources" -v "$(pwd)/.cache:/.cache" \
	  openapi-python-converter \
	      --api /resources/interfaces/interuss/automated_testing/geospatial_map/v1/geospatial_map.yaml \
	      --python_output /resources/src/uas_standards/interuss/automated_testing/geospatial_map/v1/api.py

echo "Flight planning automated testing"
mkdir -p $(pwd)/src/uas_standards/interuss/automated_testing/flight_planning/v1
docker container run -it \
    -u ${USER_GROUP} -v "$(pwd):/resources" -v "$(pwd)/.cache:/.cache" \
	  openapi-python-converter \
	      --api /resources/interfaces/interuss/automated_testing/flight_planning/v1/flight_planning.yaml \
	      --python_output /resources/src/uas_standards/interuss/automated_testing/flight_planning/v1/api.py

echo "Versioning for automated testing"
mkdir -p $(pwd)/src/uas_standards/interuss/automated_testing/versioning
docker container run -it \
    -u ${USER_GROUP} -v "$(pwd):/resources" -v "$(pwd)/.cache:/.cache" \
	  openapi-python-converter \
	      --api /resources/interfaces/interuss/automated_testing/versioning/versioning.yaml \
	      --python_output /resources/src/uas_standards/interuss/automated_testing/versioning/api.py

echo "DSS aux interface"
mkdir -p $(pwd)/src/uas_standards/interuss/dss/aux
docker container run -it \
    -u ${USER_GROUP} -v "$(pwd):/resources" -v "$(pwd)/.cache:/.cache" \
	  openapi-python-converter \
	      --api /resources/interfaces/interuss/dss/aux/aux_.yaml \
	      --python_output /resources/src/uas_standards/interuss/dss/aux/api.py

echo "Running formatter"
uv run --index https://pypi.org/simple ruff check --fix
uv run --index https://pypi.org/simple ruff format
