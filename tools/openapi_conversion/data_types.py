import dataclasses
from typing import Any, Dict, List, Optional, Set, Tuple


@dataclasses.dataclass
class ObjectField:
    """A data field within an Object data type"""

    api_name: str
    """Name of the field in the API (generally snake cased)"""

    python_type: str
    """The name of the Python data type which represents this field's value"""

    description: str
    """Documentation of this field"""

    required: bool
    """True if an instance of the parent object must specify a value for this field"""

    default: Optional[Any]
    """Default value for field, if specified"""

    literal_default: bool = False
    """If true, render the default without quotes even if it's a string"""


@dataclasses.dataclass
class DataType:
    """A specific data type defined in the API"""

    name: str
    """Name of this data type, as defined in the API"""

    python_type: str = ''
    """Name of the Python data type ('ImplicitDict' for Object data types)"""

    description: str = ''
    """Documentation of this data type"""

    fields: List[ObjectField] = dataclasses.field(default_factory=list)
    """If this is an Object data type, a list of fields contained in that Object"""

    enum_values: Dict[str, str] = dataclasses.field(default_factory=dict)
    """If this is a enum data type, a map from values it may take on to Python names for those values"""



python_primitives: Dict[str, str] = {
    'string': 'str',
    'boolean': 'bool',
}
"""Maps OpenAPI `type` to Python primitive type"""

python_numbers: Dict[str, str] = {
    'float': 'float',
    'double': 'float',
    'int32': 'int',
    'int64': 'int',
    'number': 'float',
    'integer': 'int',
}
"""Maps OpenAPI `format` (defaulting to `type` if `format` is missing) to Python primitive type"""


def is_primitive_python_type(python_type_name: str) -> bool:
    """True iff python_type_name describes a built-in Python type"""
    return python_type_name in python_primitives.values() or python_type_name in python_numbers.values()


def get_data_type_name(component_name: str, data_type_name: str) -> str:
    """Get the plain data type name from a $ref URI.

    :param component_name: $ref URI to the data type of interest
    :param data_type_name: context in which the data type is being retrieved (used for error message only)
    :return: Plain data type name in the relative $ref URI
    """
    if component_name == '':
        return ''
    elif component_name.startswith('#/components/schemas/'):
        return component_name[len('#/components/schemas/'):]
    else:
        if '#/components/schemas/' not in component_name:
            raise ValueError('$ref expected to contain `#/components/schemas/`, but found `{}` instead for {}'.format(component_name, data_type_name))
        name = get_data_type_name(component_name[component_name.index('#'):], data_type_name)
        print(f'WARNING: Assuming the variable type of {component_name} should be "{name}" and that it will be manually declared')
        return name


def _parse_referenced_type_name(schema: Dict, data_type_name: str) -> str:
    options = schema['anyOf'] if 'anyOf' in schema else schema['allOf']
    if len(options) != 1:
        raise NotImplementedError('Only one $ref is supported for anyOf and allOf; found {} elements instead'.format(len(options)))
    option = options[0]
    if not isinstance(option, dict):
        raise ValueError('Expected dict entries in anyOf/allOf block; found {} instead'.format(option))
    if len(option) != 1 or '$ref' not in option:
        raise NotImplementedError('The only element in anyOf/allOf must be a $ref dictionary; found {} instead'.format(option))
    return get_data_type_name(option['$ref'], data_type_name)


def _snake_to_pascal(snake_case: str) -> str:
    words = snake_case.split("_")
    return "".join(w[0].upper() + w[1:] for w in words)


def make_object_field(python_object_name: str, api_field_name: str, schema: Dict, required: Set[str]) -> Tuple[ObjectField, List[DataType]]:
    """Parse a single field in a data type or endpoint parameter schema.

    :param python_object_name: Name of the Python object containing this field, for error messages and inline type names
    :param api_field_name: Name of the object field being parsed, according to the API
    :param schema: Definition of the object field being parsed
    :param required: The set of required fields for the parent object
    :return: Tuple of
      * The object field defined by the provided schema
      * Any additional data types incidentally defined in the provided schema
    """
    is_required = api_field_name in required
    default_value = schema['default'] if 'default' in schema else None
    if '$ref' in schema:
        return ObjectField(
            api_name=api_field_name,
            python_type=get_data_type_name(schema['$ref'], python_object_name),
            description=schema.get('description', ''),
            required=is_required,
            default=default_value), []
    elif 'anyOf' in schema or 'allOf' in schema:
        return ObjectField(
            api_name=api_field_name,
            python_type=_parse_referenced_type_name(schema, python_object_name + '.' + api_field_name),
            description=schema.get('description', ''),
            required=is_required,
            default=default_value), []
    else:
        type_name = python_object_name + _snake_to_pascal(api_field_name)
        data_type, additional_types = make_data_types(type_name, schema)
        if is_primitive_python_type(data_type.python_type) and not data_type.enum_values:
            # No additional type declaration needed
            if additional_types:
                raise RuntimeError('{} field type `{}` was parsed as primitive {} but also generated {} additional types'.format(python_object_name, api_field_name, data_type.python_type, len(additional_types)))
            field_data_type = data_type.python_type
        elif data_type.python_type == 'StringBasedDateTime':
            # No additional type declaration needed
            field_data_type = data_type.python_type
        elif data_type.python_type.startswith('List['):
            # Use array data type as-is
            field_data_type = data_type.python_type
        else:
            additional_types.append(data_type)
            field_data_type = data_type.name
        if len(data_type.enum_values) == 1 and default_value is None:
            default_value = data_type.name + '.' + next(iter(data_type.enum_values.values()))
            literal_default = True
        else:
            literal_default = False
        return ObjectField(
            api_name=api_field_name,
            python_type=field_data_type,
            description=data_type.description,
            required=is_required,
            default=default_value,
            literal_default=literal_default), additional_types


def _make_object_fields(python_object_name: str, properties: Dict, required: Set[str]) -> Tuple[List[ObjectField], List[DataType]]:
    fields: List[ObjectField] = []
    additional_types: List[DataType] = []
    for field_name, schema in properties.items():
        field, further_types = make_object_field(python_object_name, field_name, schema, required)
        additional_types.extend(further_types)
        fields.append(field)
    return fields, additional_types


def _make_python_enums(values: List[str]) -> Dict[str, str]:
    valid_characters = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789_'
    valid_start_characters = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ_'
    result = {}
    for value in values:
        name = str(value)
        if name[0] not in valid_start_characters:
            name = '_' + name
        name = ''.join(c if c in valid_characters else '_' for c in name)
        result[str(value)] = name
    return result


def make_data_types(api_name: str, schema: Dict) -> Tuple[DataType, List[DataType]]:
    """Parse all data types necessary to express the provided data type schema.

    In addition to the primary data type described by `name`, this routine also
    generates additional data types defined inline in the provided schema.

    :param api_name: Name of the primary data type being parsed, according to the API
    :param schema: Definition of the data type being parsed
    :return: Tuple of
      * The primary data defined by the provided schema
      * Any additional data types incidentally defined in the provided schema
    """
    data_type = DataType(name=api_name)
    additional_types = []

    if 'description' in schema:
        data_type.description = schema['description']

    if 'type' in schema:
        if schema['type'] in python_primitives:
            data_type.python_type = python_primitives[schema['type']]
            if data_type.python_type == 'str' and 'format' in schema and schema['format'] == 'date-time':
                data_type.python_type = 'StringBasedDateTime'
        elif schema['type'] in {'number', 'integer'}:
            data_type.python_type = python_numbers.get(schema.get('format', schema['type']), '')
            if not data_type.python_type:
                raise ValueError('Unrecognized numeric format `{}` for {}'.format(schema.get('format', '<missing>'), api_name))
        elif schema['type'] == 'array':
            if 'items' in schema:
                items = schema['items']
                if '$ref' in items:
                    item_type_name = get_data_type_name(items['$ref'], api_name)
                else:
                    item_type, further_types = make_data_types(api_name + 'Item', items)
                    additional_types.extend(further_types)
                    if item_type.description != '' or not is_primitive_python_type(item_type.python_type):
                        additional_types.append(item_type)
                        item_type_name = item_type.name
                    else:
                        item_type_name = item_type.python_type
                data_type.python_type = f'List[{item_type_name}]'
            else:
                raise ValueError('Missing `items` declaration for {} array type'.format(api_name))
        elif schema['type'] == 'object':
            data_type.python_type = 'ImplicitDict'
            data_type.fields, further_types = _make_object_fields(
                api_name,
                schema.get('properties', {}),
                set(schema.get('required', [])))
            additional_types.extend(further_types)
        else:
            raise ValueError('Unrecognized type `{}` in {} type'.format(schema['type'], api_name))
    elif 'anyOf' in schema or 'allOf' in schema:
        data_type.python_type = _parse_referenced_type_name(schema, api_name)

    if 'enum' in schema:
        data_type.enum_values = _make_python_enums(schema['enum'])

    if not data_type.python_type:
        data_type.python_type = 'str'

    return data_type, additional_types


def parse(spec: dict) -> List[DataType]:
    if 'components' not in spec:
        raise ValueError('Missing `components` in YAML')
    components = spec['components']
    if 'schemas' not in components:
        raise ValueError('Missing `schemas` in `components`')
    declared_types = []
    for name, schema in components['schemas'].items():
        data_type, additional_types = make_data_types(name, schema)
        declared_types.extend(additional_types)
        declared_types.append(data_type)
    return declared_types
