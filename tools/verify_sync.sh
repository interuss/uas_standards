#!/bin/bash

OS=$(uname)
if [[ $OS == "Darwin" ]]; then
	# OSX uses BSD readlink
	BASEDIR="$(dirname "$0")"
else
	BASEDIR=$(readlink -e "$(dirname "$0")")
fi

cd "${BASEDIR}/.." || exit

# Format: ["path/to/update_script.sh"]="affected_file1.txt affected_file2.yaml dir/affected_file3.md"
declare -A SCRIPT_MAP
SCRIPT_MAP=(
    ["./interfaces/interuss/dss/aux/get_from_upstream.sh"]="./interfaces/interuss/dss/aux/aux_.yaml"
)

get_checksums() {
    local files=$1
    md5sum $files 2>/dev/null
}

failed_scripts=()

for script in "${!SCRIPT_MAP[@]}"; do
    files=${SCRIPT_MAP[$script]}

    echo "------------------------------------------------"
    echo "Checking script: $script"
    echo "Monitoring files: $files"

    # 1. Capture initial state
    pre_checksum=$(get_checksums "$files")

    # 2. Run the script
    if [[ -f "$script" ]]; then
        chmod +x "$script"
        echo "Running $script..."
        ./"$script"
    else
        echo "Error: Script '$script' not found. Skipping."
        failed_scripts+=("$script (Not Found)")
        continue
    fi

    # 3. Capture post state
    post_checksum=$(get_checksums "$files")

    # 4. Compare
    if [[ "$pre_checksum" == "$post_checksum" ]]; then
        echo "Success: No monitored files were changed by $script."
    else
        echo "FAILURE: One or more files were modified by $script!"
        failed_scripts+=("$script (Modified Files)")
    fi
done

echo "------------------------------------------------"
if [ ${#failed_scripts[@]} -eq 0 ]; then
    echo "All checks passed! All files are in sync."
    exit 0
else
    echo "The following operations needed to be performed to ensure files are in sync:"
    for item in "${failed_scripts[@]}"; do
        echo "  - $item"
    done
    exit 1
fi
