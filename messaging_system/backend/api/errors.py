from typing import Dict

from flask import jsonify, Response
from werkzeug.http import HTTP_STATUS_CODES


def error_response(status_code: int, message: str = None) -> Response:
    payload = {"error": HTTP_STATUS_CODES.get(status_code, "Unknown error")}
    payload["message"] = message or payload["error"]
    response = jsonify(payload)
    response.status_code = status_code

    return response


def bad_request(message: str = "Bad request",) -> Dict:
    return error_response(400, message)


def not_found(message: str = "Not found") -> Dict:
    return error_response(404, message)
