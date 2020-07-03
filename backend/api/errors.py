from typing import Dict, List, Union

from flask import jsonify, Response
from werkzeug.http import HTTP_STATUS_CODES

from backend import secure_headers


def error_response(status_code: int, message: Union[str, List, Dict] = None) -> Response:
    payload = {"error": HTTP_STATUS_CODES.get(status_code, "Unknown error")}
    payload["messages"] = message or payload["error"]
    response = jsonify(payload)
    response.status_code = status_code

    secure_headers.flask(response)
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
