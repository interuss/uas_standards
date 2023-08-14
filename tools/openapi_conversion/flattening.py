from dataclasses import dataclass
import os
from typing import Union, Dict

import yaml


def flatten(spec: dict, path_of_spec: str) -> None:
    """Flatten an OpenAPI specification by moving external $refs into the spec.

    This function assumes all objects in `spec` are defined in /components/schemas, and all $refs to external
    specifications follow the same rules.

    Args:
        spec: OpenAPI specification to be mutated by flattening it.
        path_of_spec: Path to directory containing the specification being flattened.  Relative $ref paths (e.g.,
            "./other_spec.yaml#/components/objects/Foo") will be resolved relative to this path.
    """
    additional_components: Dict[str, _AdditionalComponent] = {}
    _flatten_part(spec, path_of_spec, spec, additional_components)
    for k, v in additional_components.items():
        spec["components"]["schemas"][k] = v.schema


@dataclass
class _AdditionalComponent(object):
    included_by: str
    """This additional component was added to the flattened schema by this (included/$ref'd) filename."""

    schema: dict
    """Object definition schema for this component to add to the flattened schema's components."""


def _flatten_part(spec: dict, path_of_spec: str, part: dict, additional_components: Dict[str, _AdditionalComponent]) -> None:
    """Flatten `spec` by adding externally-$ref'd components to `additional_components` and changing external $refs to internal.

    Args:
        spec: Full OpenAPI specification being flattened.  External $refs will be mutated to internal $refs.
        path_of_spec: Path to directory containing `spec`.
        part: Portion of `spec` being flattened.
        additional_components: Set of components that need to be added to `spec` to flatten it (these components need to
          be added to /components/schemas of `spec`).
    """
    mutations = {}
    for k, v in part.items():
        if k == "$ref":
            if not v.startswith("#"):
                # This is an external $ref
                anchor = _add_external_ref(v, path_of_spec, additional_components)
                mutations[k] = "#" + anchor
        elif isinstance(v, dict):
            _flatten_part(spec, path_of_spec, v, additional_components)
        elif isinstance(v, list):
            for item in v:
                if isinstance(item, dict):
                    _flatten_part(spec, path_of_spec, item, additional_components)

    for k, v in mutations.items():
        part[k] = v


def _add_external_ref(ref_path: str, path_of_spec: str, additional_components: Dict[str, _AdditionalComponent]) -> str:
    filename, anchor = ref_path.split("#")
    if not anchor.startswith("/components/schemas"):
        raise NotImplementedError(f"Flattening does not currently support reference to objects not defined at /components/schemas")
    if filename.startswith("http://") or filename.startswith("https://"):
        raise NotImplementedError(f"Cannot flatten schema with $ref to {filename}")
    if filename.startswith("file://"):
        filename = filename[len("file://")]
    elif filename.startswith("/"):
        pass  # No change needed for absolute paths
    else:
        # This is apparently a relative path
        filename = os.path.join(path_of_spec, filename)

    with open(filename, "r") as f:
        foreign_schema = yaml.full_load(f)

    _add_object_from_path_and_schema(foreign_schema, filename, "#" + anchor, additional_components)
    return anchor


def _add_object_from_path_and_schema(schema: dict, filename: str, path: str, additional_components: Dict[str, _AdditionalComponent]) -> None:
    """Add the schema for the object at `path` within `schema` to `additional_components` given that `schema` came from `filename`.

    Args:
        schema: Full schema read from a file $ref'd from the schema being flattened.
        filename: Path of file from which `schema` was obtained.
        path: Path to object in `schema` that should be added to `additional_components` (e.g., /components/schemas/Foo).
        additional_components: Map of component name to component schema of components to add to schema being flattened.
          Will be mutated by this function to add the object at `path` in `schema`, and all sub-$ref'd objects contained
          in the object at `path` in `schema`.
    """
    varpath = path.split("/")
    varpath = varpath[1:]
    varname = varpath[-1]
    if varname in additional_components:
        # A component by this name has already been added to the flattened schema
        if additional_components[varname].included_by != filename:
            raise ValueError(f"Flattening error: component named {varname} was already flattened into the schema from $ref'd {additional_components[varname].included_by} when attempting to flatten {varname} into the schema from $ref'd {filename}")
        return
    object_schema = schema
    while varpath:
        object_schema = object_schema[varpath[0]]
        varpath = varpath[1:]
    additional_components[varname] = _AdditionalComponent(schema=object_schema, included_by=filename)

    _include_subref_objects(schema, filename, object_schema, additional_components)


def _include_subref_objects(schema: dict, parent_filename: str, obj: Union[dict, list, tuple], additional_components: Dict[str, _AdditionalComponent]) -> None:
    """Include all `schema` objects $ref'd by `obj` or its descendants in `additional_components` given that `schema` came from `parent_filename`."""
    if isinstance(obj, dict):
        if "$ref" in obj:
            filename, anchor = obj["$ref"].split("#")
            if filename == "":
                # Local $ref (within file)
                if not anchor.startswith("/components/schemas"):
                    raise NotImplementedError(f"Flattening does not currently support reference to objects not defined at /components/schemas")
                _add_object_from_path_and_schema(schema, parent_filename, anchor, additional_components)
            else:
                path_of_spec = os.path.dirname(os.path.abspath(parent_filename))
                anchor = _add_external_ref(obj["$ref"], path_of_spec, additional_components)
                obj["$ref"] = f"#{anchor}"
        for k, v in obj.items():
            _include_subref_objects(schema, parent_filename, v, additional_components)
    elif isinstance(obj, list) or isinstance(obj, tuple):
        for v in obj:
            _include_subref_objects(schema, parent_filename, v, additional_components)
