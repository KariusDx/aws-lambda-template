from typing import NamedTuple, Dict, Any

import json
import sys
import os
import boto3

here = os.path.dirname(os.path.realpath(__file__))
sys.path.append(os.path.join(here, "vendor"))
from vendor import requests  # noqa

Message = Dict[str, Any]

def handler(event: Any, context: Any) -> Message:
    body = {
        "message": "Finished processing successfully.",
        "input": event
    }
    response = {
        "statusCode": 200,
        "body": json.dumps(body)
    }
    return response


def get_env(env_var: str) -> str:
    value = os.getenv(env_var)
    if value is None:
        raise Exception(env_var + ' is not defined')
    return value
