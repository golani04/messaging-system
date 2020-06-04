from flask import jsonify, request
from flask_jwt_extended import create_access_token

from backend.api import errors
from backend.models.users import User

from . import bp


@bp.route("/login", methods=["POST"])
def login():
    if not request.is_json:
        return errors.bad_request("Accepts only data as json")

    data = request.get_json()
    password = data.get("password")
    email = data.get("email")

    if not email or not password:
        return errors.bad_request("Missing email or password.")

    user = User.autenticate(email)

    # TODO: if email is missing, using brute force to get existing users
    #       Consider limit number of tries or show 401 error Bad email or password
    if user is None:
        return errors.not_found("User with this email does not exist.")

    if not user.verify_passw(password, user.password):
        return errors.error_response(401, "Bad email or password.")

    access_token = create_access_token(identity=user.id)

    return jsonify(access_token=access_token), 200
