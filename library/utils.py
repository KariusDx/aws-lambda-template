from typing import Any, Dict

import os
import json


def get_env(env_var: str) -> str:
    value = os.getenv(env_var)
    if value is None:
        raise Exception(env_var + ' is not defined')
    return value


def respond_success(event: Any) -> Dict[str, Any]:
    body = {
        "message": "Finished processing successfully.",
        "input": event
    }
    response = {
        "statusCode": 200,
        "body": json.dumps(body)
    }
    return response
