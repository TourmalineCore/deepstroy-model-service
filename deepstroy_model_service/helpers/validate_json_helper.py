import jsonschema
from jsonschema import validate


def validate_json_schema(schema, response) -> bool:
    try:
        validate(instance=response.json, schema=schema)
    except jsonschema.exceptions.ValidationError:
        return False
    return True
