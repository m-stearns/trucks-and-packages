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

@bp.route("", methods=["POST", "GET"])
def create_truck():
    try:
        payload = auth.verify_jwt(request)
    except (exceptions.NoAuthHeaderError, exceptions.InvalidHeaderError) as e:
        response_401_error = make_response(e.error)
        response_401_error.status_code = e.status_code
        return response_401_error
    
    if request.method == "POST":
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
        
        truck_type = json_data["type"]
        length = json_data["length"]
        axles = json_data["axles"]
        auth_id = payload["sub"]

        truck_id = services.create_truck(
            truck_type, length, axles, auth_id, unit_of_work.DatastoreUnitOfWork()
        )
        response_201 = make_response(
            jsonify({
                "id": truck_id,
                "type": truck_type,
                "length": length,
                "axles": axles,
                "packages": [],
                "owner": auth_id,
                "self": f"{request.base_url}/{truck_id}"
            })
        )
        response_201.status_code = 201
        return response_201

    if request.method == "GET":
        response_406_error = common.check_for_accept_error_406(
            request, ["application/json"]
        )
        if response_406_error:
            return response_406_error

        query_offset = int(request.args.get("offset", "0"))
        query_limit = 5
        trucks, next_page_available = services.get_trucks(
            query_limit, query_offset, unit_of_work.DatastoreUnitOfWork()
        )
        response_200 = jsonify(
            {
                "trucks": [
                    truck_to_dict(
                        truck,
                        f"{request.base_url}",
                        create_list_of_package_dict(truck.package_ids, f"{request.host_url}packages")
                    ) for truck in trucks
                ],
                "next": f"{request.base_url}?limit=5&offset={query_offset + query_limit}" if next_page_available else None
            }
        )
        response_200.status_code = 200
        return response_200


@bp.route("/<truck_id>", methods=["GET", "PATCH", "PUT", "DELETE"])
def get_update_or_delete_truck(truck_id: str):
    try:
        payload = auth.verify_jwt(request)
    except (exceptions.NoAuthHeaderError, exceptions.InvalidHeaderError) as e:
        response_401_error = make_response(e.error)
        response_401_error.status_code = e.status_code
        return response_401_error

    if request.method == "GET":
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
            response_404_error = make_response(
                jsonify({
                    "Error": "No truck with this truck_id exists"
                })
            )
            response_404_error.status_code = 404
            return response_404_error
            
        elif truck.owner != auth_id:
            response_403_error = make_response()
            response_403_error.status_code = 403
            return response_403_error
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
        
        auth_id = payload["sub"]
        truck = services.get_truck(truck_id, unit_of_work.DatastoreUnitOfWork())
        if truck:
            if truck.owner == auth_id:
                truck_type = json_data.get("type", None)
                truck_length = json_data.get("length", None)
                axles = json_data.get("axles", None)
                services.edit_truck(
                    truck,
                    truck_type,
                    truck_length,
                    axles,
                    unit_of_work.DatastoreUnitOfWork()
                )
                response_200 = jsonify(
                    truck_to_dict(
                        truck,
                        f"{request.base_url}",
                        create_list_of_package_dict(truck.package_ids, f"{request.host_url}packages")
                    )
                )
                response_200.status_code = 200
                return response_200

            else:
                response_403_error = make_response()
                response_403_error.status_code = 403
                return response_403_error

        else:
            response_404_error = make_response(
                jsonify({
                    "Error": "No truck with this truck_id exists"
                })
            )
            response_404_error.status_code = 404
            return response_404_error

    elif request.method == "PUT":
        response_415_error = common.check_for_content_type_error_415(request)
        if response_415_error:
            return response_415_error

        response_406_error = common.check_for_accept_error_406(
            request, ["application/json"]
        )
        if response_406_error:
            return response_406_error

        json_data = request.get_json()
        if not json_data or not has_required_values_for_create_truck(json_data) \
            or contains_unallowed_attributes(json_data):
            response_400_error = make_response({
                "Error": "The request object is missing all of the required attributes"
            })
            response_400_error.status_code = 400
            return response_400_error

        auth_id = payload["sub"]
        truck = services.get_truck(
            truck_id, unit_of_work.DatastoreUnitOfWork()
        )
        if truck:
            if truck.owner == auth_id:
                truck_type = json_data["type"]
                length = json_data["length"]
                axles = json_data["axles"]
                services.edit_truck(
                    truck,
                    truck_type,
                    length,
                    axles,
                    unit_of_work.DatastoreUnitOfWork(),
                    clear_package_ids=True,
                )
                response_303 = make_response()
                response_303.status_code = 303
                response_303.headers["Location"] = f"{request.host_url}trucks/{truck_id}"
                return response_303

            else:
                response_403_error = make_response()
                response_403_error.status_code = 403
                return response_403_error
        else:
            response_404_error = make_response(
                jsonify({
                    "Error": "No truck with this truck_id exists"
                })
            )
            response_404_error.status_code = 404
            return response_404_error

    if request.method == "DELETE":
        response_406_error = common.check_for_accept_error_406(
            request, ["application/json"]
        )
        if response_406_error:
            return response_406_error

        auth_id = payload["sub"]
        truck = services.get_truck(
            truck_id, unit_of_work.DatastoreUnitOfWork()
        )
        if truck:
            if truck.owner == auth_id:
                services.delete_truck(
                    truck_id, unit_of_work.DatastoreUnitOfWork()
                )
                response_200 = make_response()
                response_200.status_code = 204
                return response_200
            else:
                response_403_error = make_response()
                response_403_error.status_code = 403
                return response_403_error
        else:
            response_404_error = make_response(
                jsonify({
                    "Error": "No truck with this truck_id exists"
                })
            )
            response_404_error.status_code = 404
            return response_404_error
