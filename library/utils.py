from typing import Any, Dict, Callable

import os
import json


def get_env(env_var: str) -> str:
    value = os.getenv(env_var)
    if value is None:
        raise Exception(env_var + ' is not defined')
    return value


def deploy_check(
        continuation: Callable[..., Dict[str, Any]], event: Any, *args: Any) -> Dict[str, Any]:
    """
    If the function is invoked with json with 'verify-commit' as a key,
    check that the value matches the git-commit.txt file and exit.

    If this parameter is not passed in, continue with normal operation
    """
    if event is None:
        return continuation(event, *args)

    sent_commit = event.get('verify-commit')
    if sent_commit is None:
        return continuation(event, *args)

    with open("git-commit.txt") as handle:
        commit = handle.readline().strip()
        if commit == sent_commit:
            return respond_success(event)
        else:
            msg = "Git commit differs. Expected: " + sent_commit + " Got: " + commit
            return respond_failure(event, msg)


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


def respond_failure(event: Any, message: str) -> Dict[str, Any]:
    body = {
        "message": message,
        "input": event
    }
    response = {
        "statusCode": 400,
        "body": json.dumps(body)
    }
    return response
