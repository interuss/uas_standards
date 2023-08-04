# This tool generates Python data types and path constants from an OpenAPI YAML file.

import argparse
import os

import yaml

import data_types
import flattening
import operations
import rendering


def _parse_args():
    parser = argparse.ArgumentParser(description='Autogenerate Python data types from an OpenAPI YAML')

    # Input/output specifications
    parser.add_argument('--api', dest='api', type=str,
                        help='Source YAML to preprocess.')
    parser.add_argument('--python_output', dest='python_output', type=str,
                        help='Output file for generated Python code')
    parser.add_argument('--default_package', dest='default_package', type=str,
                        help='If this API refers to objects in another API, the Python package name where those other objects may be found',
                        default='<not_defined>')

    return parser.parse_args()


def main():
    args = _parse_args()

    # Parse OpenAPI
    with open(args.api, mode='r') as f:
        spec = yaml.full_load(f)

    # Flatten external $refs
    flattening.flatten(spec, os.path.dirname(os.path.abspath(args.api)))

    # Parse data types
    types = data_types.parse(spec)

    # Parse operations
    ops = operations.get_operations(spec)

    # Render Python code
    with open(args.python_output, 'w') as f:
        f.write(f'"""Data types and operations from {spec["info"]["title"]} {spec["info"]["version"]} OpenAPI"""\n\n')
        f.write('\n'.join(rendering.header(types)))
        f.write('\n\n\n')
        f.write('\n'.join(rendering.api_version(spec)))
        f.write('\n'.join(rendering.data_types(types, args.default_package)))
        f.write('\n\n')
        f.write('\n'.join(rendering.operations(ops)))
        f.write('\n')


if __name__ == '__main__':
    main()
