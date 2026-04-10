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

DOCKER_CMD="docker container run --rm \
  -u ${USER_GROUP} \
  -v $(pwd):/resources \
  openapi-python-converter"

# Usage: generate "Label" "Interface YAML" "Output Python Path"
generate_api() {
    local label=$1
    local api_path=$2
    local output_path=$3
    local output_dir=$(dirname "$output_path")

    echo "Building: $label"

    # Create directory if it doesn't exist
    mkdir -p "./$output_dir"

    # Execute converter
    $DOCKER_CMD \
        --api "/resources/$api_path" \
        --python_output "/resources/$output_path"
}

# --- ASTM Standards ---
generate_api "F3411-19" "interfaces/astm/f3411/v19/remoteid/augmented.yaml" "src/uas_standards/astm/f3411/v19/api.py"
generate_api "F3411-22a" "interfaces/astm/f3411/v22a/remoteid/updated.yaml" "src/uas_standards/astm/f3411/v22a/api.py"
generate_api "F3548-21" "interfaces/astm/f3548/v21/utm.yaml" "src/uas_standards/astm/f3548/v21/api.py"

# --- InterUSS Automated Testing ---
TEST_BASE="interfaces/interuss/automated_testing"
SRC_BASE="src/uas_standards/interuss/automated_testing"

generate_api "Geo-awareness" "$TEST_BASE/geo-awareness/v1/geo-awareness.yaml" "$SRC_BASE/geo_awareness/v1/api.py"
generate_api "RID injection" "$TEST_BASE/rid/v1/injection.yaml" "$SRC_BASE/rid/v1/injection.py"
generate_api "RID observation" "$TEST_BASE/rid/v1/observation.yaml" "$SRC_BASE/rid/v1/observation.py"
generate_api "SCD" "$TEST_BASE/scd/v1/scd.yaml" "$SRC_BASE/scd/v1/api.py"
generate_api "Geospatial map" "$TEST_BASE/geospatial_map/v1/geospatial_map.yaml" "$SRC_BASE/geospatial_map/v1/api.py"
generate_api "Flight planning" "$TEST_BASE/flight_planning/v1/flight_planning.yaml" "$SRC_BASE/flight_planning/v1/api.py"
generate_api "Versioning" "$TEST_BASE/versioning/versioning.yaml" "$SRC_BASE/versioning/api.py"

# --- DSS ---
generate_api "DSS aux interface" "interfaces/interuss/dss/aux/aux_.yaml" "src/uas_standards/interuss/dss/aux/api.py"

echo "Running formatter"
uv run ruff check --fix
uv run ruff format
