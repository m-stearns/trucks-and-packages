from flask import Blueprint, jsonify, make_response, request

from trucksandpackages import auth, exceptions
from trucksandpackages.services import services, unit_of_work

bp = Blueprint("trucks", __name__, url_prefix="/trucks")

CREATE_TRUCK_REQUIRED_VALUES = ["type", "length", "axles"]

def has_required_values_for_create_truck(json_data: dict) -> bool:
    for value in CREATE_TRUCK_REQUIRED_VALUES:
        if value not in json_data:
            return False
    return True

@bp.route("", methods=["POST"])
def create_truck():
    if request.method == "POST":
        try:
            payload = auth.verify_jwt(request)
        except (exceptions.NoAuthHeaderError, exceptions.InvalidHeaderError) as e:
            response_401_error = make_response(e.error)
            response_401_error.status_code = e.status_code
            return response_401_error

        json_data = request.get_json()
        if not has_required_values_for_create_truck(json_data):
            response_400_error = make_response(
                jsonify({
                "Error": "The request object is missing at least one of the required attributes"
                })
            )
            response_400_error.status_code = 400
            return response_400_error
        
        type = json_data["type"]
        length = json_data["length"]
        axles = json_data["axles"]
        owner = payload["sub"]
        truck_id = services.create_truck(
            type, length, axles, owner, unit_of_work.DatastoreUnitOfWork()
        )
        res = make_response(
            jsonify({
                "id": truck_id,
                "type": type,
                "length": length,
                "axles": axles,
                "packages": [],
                "owner": owner,
                "self": f"{request.base_url}/{truck_id}"
            })
        )
        res.status_code = 201
        return res