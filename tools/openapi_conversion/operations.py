from dataclasses import dataclass
from typing import List, Dict, Optional


@dataclass
class Operation(object):
    id: str
    path: str
    verb: str
    request_body_type: Optional[str]
    response_body_type: Dict[int, Optional[str]]

    @property
    def name(self) -> str:
        return self.id[0].upper() + self.id[1:]


def get_operations(spec: dict) -> List[Operation]:
    ref_prefix = '#/components/schemas/'
    operations: List[Operation] = []
    all_verbs = {"get", "put", "post", "delete", "patch"}
    for path, body in spec["paths"].items():
        for k, v in body.items():
            if k not in all_verbs:
                continue

            ref = v.get("requestBody", {}).get("content", {}).get("application/json", {}).get("schema", {}).get("$ref", '')
            request_body_type = ref[len(ref_prefix):] if ref.startswith(ref_prefix) else None

            response_body_type = {}
            for code, response_content in v["responses"].items():
                ref = response_content.get("content", {}).get("application/json", {}).get("schema", {}).get("$ref", '')
                response_body_type[int(code)] = ref[len(ref_prefix):] if ref.startswith(ref_prefix) else None

            op_id = v.get("operationId", None)
            if not op_id:
                print(f'WARNING: {k} {path} is missing an operationId')
                path_parts = path.split('/')
                if path_parts[-1].startswith('{') or '_' in path_parts[-1]:
                    raise NotImplementedError('Cannot construct operationId')
                op_id = k.lower() + path_parts[-1][0].upper() + path_parts[-1][1:]
            operations.append(Operation(
                id=op_id,
                path=path,
                verb=k.upper(),
                request_body_type=request_body_type,
                response_body_type=response_body_type,
            ))
    return operations
