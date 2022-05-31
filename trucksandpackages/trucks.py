from typing import List, Set
from flask import Blueprint, jsonify, make_response, request

from trucksandpackages import auth, common, exceptions
from trucksandpackages.services import services, unit_of_work
from trucksandpackages.domain import model

bp = Blueprint("trucks", __name__, url_prefix="/trucks")

CREATE_TRUCK_REQUIRED_VALUES = ["type", "length", "axles"]

def has_required_values_for_create_truck(json_data: dict) -> bool:
    for value in CREATE_TRUCK_REQUIRED_VALUES:
        if value not in json_data:
            return False
    return True

def truck_to_dict(truck: model.Truck, self_link: str, packages_dict: List) -> dict:
    return {
        "id": truck.truck_id,
        "type": truck.truck_type,
        "length": truck.truck_length,
        "axles": truck.axles,
        "packages": packages_dict,
        "owner": truck.owner,
        "self": self_link
    }

def create_list_of_package_dict(package_ids: Set[str], host_url: str) -> List:
    return [package_to_dict(package_id, host_url) for package_id in package_ids]

def package_to_dict(package_id: str, host_url: str):
    return {
        "id": package_id,
        "self": f"{host_url}/{package_id}"
    }

def contains_unallowed_attributes(json_data: dict) -> bool:
    for key in json_data:
        if key not in CREATE_TRUCK_REQUIRED_VALUES:
            return True
    return False

@bp.route("", methods=["POST"])
def create_truck():
    if request.method == "POST":
        try:
            payload = auth.verify_jwt(request)
        except (exceptions.NoAuthHeaderError, exceptions.InvalidHeaderError) as e:
            response_401_error = make_response(e.error)
            response_401_error.status_code = e.status_code
            return response_401_error

        response_415_error = common.check_for_content_type_error_415(request)
        if response_415_error:
            return response_415_error

        response_406_error = common.check_for_accept_error_406(
            request, ["application/json"]
        )
        if response_406_error:
            return response_406_error

        json_data = request.get_json()
        if not has_required_values_for_create_truck(json_data):
            response_400_error = make_response(
                jsonify({
                    "Error": "The request object is missing at least one of the \
                        required attributes"
                })
            )
            response_400_error.status_code = 400
            return response_400_error
        
        type = json_data["type"]
        length = json_data["length"]
        axles = json_data["axles"]
        auth_id = payload["sub"]

        truck_id = services.create_truck(
            type, length, axles, auth_id, unit_of_work.DatastoreUnitOfWork()
        )
        res = make_response(
            jsonify({
                "id": truck_id,
                "type": type,
                "length": length,
                "axles": axles,
                "packages": [],
                "owner": auth_id,
                "self": f"{request.base_url}/{truck_id}"
            })
        )
        res.status_code = 201
        return res


@bp.route("/<truck_id>", methods=["GET"])
def get_or_update_truck(truck_id: str):
    if request.method == "GET":
        try:
            payload = auth.verify_jwt(request)
        except (exceptions.NoAuthHeaderError, exceptions.InvalidHeaderError) as e:
            response_401_error = make_response(e.error)
            response_401_error.status_code = e.status_code
            return response_401_error

        response_406_error = common.check_for_accept_error_406(
            request, ["application/json"]
        )
        if response_406_error:
            return response_406_error

        auth_id = payload["sub"]
        truck = services.get_truck(
            truck_id, unit_of_work.DatastoreUnitOfWork()
        )
        if not truck:
            response_400_error = make_response(
                jsonify({
                    "Error": "No truck with this truck_id exists"
                })
            )
            response_400_error.status_code = 400
            return response_400_error
            
        elif truck.owner != auth_id:
            return "Bad stuff bro", 400
        else:
            response_200 = jsonify(
                truck_to_dict(
                    truck,
                    f"{request.base_url}",
                    create_list_of_package_dict(truck.package_ids, f"{request.host_url}packages")
                )
            )
            response_200.status_code = 200
            return response_200
    
    elif request.method == "PATCH":
        try:
            payload = auth.verify_jwt(request)
        except (exceptions.NoAuthHeaderError, exceptions.InvalidHeaderError) as e:
            response_401_error = make_response(e.error)
            response_401_error.status_code = e.status_code
            return response_401_error

        response_415_error = common.check_for_content_type_error_415(request)
        if response_415_error:
            return response_415_error

        response_406_error = common.check_for_accept_error_406(
            request, ["application/json"]
        )
        if response_406_error:
            return response_406_error

        json_data = request.get_json()
        if not json_data or contains_unallowed_attributes(json_data):
            response_400_error = make_response({
                "Error": "The request object is missing at least one of the \
                    required attributes"
            })
            response_400_error.status_code = 400
            response_400_error.headers.set(
                "Content-Type", "application/json"
            )
            return response_400_error

        truck_type = json_data.get("type", None)
        truck_length = json_data.get("length", None)
        axles = json_data.get("axles", None)

        result = services.edit_truck(
            truck_id,
            truck_type,
            truck_length,
            axles,
            unit_of_work.DatastoreUnitOfWork()
        )