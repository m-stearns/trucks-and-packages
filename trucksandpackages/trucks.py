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

def create_list_of_package_dict(packages: Set[model.Package], host_url: str) -> List:
    return [package_to_dict(package, host_url) for package in packages]

def package_to_dict(package: model.Package, host_url: str):
    return {
        "id": package.package_id,
        "self": f"{host_url}/{package.package_id}"
    }

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

@bp.route("/<truck_id>", methods=["GET"])
def get_truck(truck_id: str):
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

        owner = payload["sub"]
        truck = services.get_truck(
            truck_id, owner, unit_of_work.DatastoreUnitOfWork()
        )
        if not truck:
            response_400_error = make_response(
                jsonify({
                    "Error": "No truck with this truck_id exists"
                })
            )
            response_400_error.status_code = 400
            return response_400_error
            
        elif truck.owner != owner:
            return "Bad stuff bro", 400
        else:
            response_200 = jsonify(
                truck_to_dict(
                    truck,
                    f"{request.base_url}",
                    create_list_of_package_dict(truck.packages, f"{request.host_url}packages")
                )
            )
            response_200.status_code = 200
            return response_200
