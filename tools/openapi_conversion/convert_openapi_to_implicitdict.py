# This tool generates Python data types from an OpenAPI YAML file.

import argparse

import yaml

import data_types
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

    # Parse data types
    types = data_types.parse(spec)

    # Render Python code
    with open(args.python_output, 'w') as f:
        f.write(f'"""Data types from {spec["info"]["title"]} {spec["info"]["version"]} OpenAPI"""\n\n')
        f.write('\n'.join(rendering.data_types(types, args.default_package)))


if __name__ == '__main__':
    main()
