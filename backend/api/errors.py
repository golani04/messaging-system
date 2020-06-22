from collections import defaultdict
from typing import Dict, List, Union

from flask import jsonify, Response
from werkzeug.http import HTTP_STATUS_CODES

from . import bp


def error_response(status_code: int, message: Union[str, List, Dict] = None) -> Response:
    payload = {"error": HTTP_STATUS_CODES.get(status_code, "Unknown error")}
    payload["messages"] = message or payload["error"]
    response = jsonify(payload)
    response.status_code = status_code

    return response


def bad_request(message: str = "Bad request") -> Dict:
    return error_response(400, message)


def unauthorized(message: str = "Unauthorized") -> Dict:
    return error_response(401, message)


def forbidden(message: str = "Forbidden") -> Dict:
    return error_response(403, message)


def not_found(message: str = "Not found") -> Dict:
    return error_response(404, message)


def internal_error(message: str = "Internal Error") -> Dict:
    return error_response(500, message)


@bp.app_errorhandler(422)
def entity_unprocessable(err):
    error = defaultdict(dict, err.data.get("messages", dict))
    if json := error["json"]:
        return error_response(400, json)

    return error_response(400)
