
from calendar import c
import datetime
from decimal import Decimal

from flask import Blueprint, jsonify, make_response, request

from trucksandpackages import common
from trucksandpackages.domain import model
from trucksandpackages.services import services, unit_of_work

bp = Blueprint("packages", __name__, url_prefix="/packages")

CREATE_PACKAGE_REQUIRED_VALUES = ["shipping_type", "weight", "shipping_date"]

def has_required_values_for_create_package(json_data: dict):
    for value in CREATE_PACKAGE_REQUIRED_VALUES:
        if value not in json_data:
            return False
    return True

def package_to_dict(package: model.Package, self_link: str, carrier_dict: dict) -> dict:
    return {
        "id": package.package_id,
        "shipping_type": package.shipping_type,
        "weight": package.weight,
        "shipping_date": package.shipping_date.strftime("%m/%d/%Y"),
        "carrier": carrier_dict,
        "self": self_link
    }

def carrier_to_dict(carrier_id: str, host_url: str) -> dict:
    if carrier_id:
        return {
            "id": carrier_id,
            "self": f"{host_url}/{carrier_id}"
        }
    else:
        return None

def contains_unallowed_attributes(json_data: dict) -> bool:
    for key in json_data:
        if key not in CREATE_PACKAGE_REQUIRED_VALUES:
            return True
    return False

@bp.route("", methods=["GET", "POST"])
def create_package_or_get_packages():
    if request.method == "GET":
        response_406_error = common.check_for_accept_error_406(
            request, ["application/json"]
        )
        if response_406_error:
            return response_406_error

        query_offset = int(request.args.get("offset", "0"))
        query_limit = 5
        packages, next_page_available = services.get_packages(
            query_limit, query_offset, unit_of_work.DatastoreUnitOfWork()
        )
        response_200 = jsonify(
            {
                "packages": [
                    package_to_dict(
                        package,
                        f"{request.base_url}/{package.package_id}",
                        carrier_to_dict(package.carrier_id, f"{request.host_url}trucks")
                    ) for package in packages
                ],
                "next": f"{request.base_url}?limit=5&offset={query_offset + query_limit}" if next_page_available else None
            }
        )
        response_200.status_code = 200
        return response_200
        
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
        if not has_required_values_for_create_package(json_data):
            response_400_error = make_response(
                jsonify({
                    "Error": \
                    "The request object is missing at least one of the required attributes"
                })
            )
            response_400_error.status_code = 400
            return response_400_error

        shipping_type = json_data["shipping_type"]
        weight = Decimal(str(json_data["weight"]))
        shipping_date = datetime.datetime.strptime(
            json_data["shipping_date"], "%m/%d/%Y"
        ).date()
        package_id = services.create_package(
            shipping_type,
            weight,
            shipping_date,
            unit_of_work.DatastoreUnitOfWork()
        )
        response_201 = jsonify({
            "id": package_id,
            "shipping_type": shipping_type,
            "weight": weight,
            "shipping_date": shipping_date.strftime("%m/%d/%Y"),
            "carrier": None,
            "self": f"{request.base_url}/{package_id}"
        })
        response_201.status_code = 201
        return response_201

@bp.route("/<package_id>", methods=["GET", "PATCH", "PUT", "DELETE"])
def get_edit_or_delete_package(package_id: str):
    if request.method == "GET":
        response_406_error = common.check_for_accept_error_406(
            request, ["application/json"]
        )
        if response_406_error:
            return response_406_error

        package = services.get_package(
            package_id, unit_of_work.DatastoreUnitOfWork()
        )
        if not package:
            response_404_error = make_response(
                jsonify({
                    "Error": "No package with this package_id exists"
                })
            )
            response_404_error.status_code = 404
            return response_404_error
        else:
            response_200 = jsonify(
                package_to_dict(
                    package,
                    f"{request.base_url}",
                    carrier_to_dict(package.carrier_id, f"{request.host_url}trucks")
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
        
        package = services.get_package(package_id, unit_of_work.DatastoreUnitOfWork())
        if package:
            shipping_type = json_data.get("shipping_type", None)
            weight = json_data.get("weight", None)
            if weight:
                weight = Decimal(str(json_data["weight"]))
            shipping_date = json_data.get("shipping_date", None)
            if shipping_date:
                shipping_date = datetime.datetime.strptime(
                    json_data["shipping_date"], "%m/%d/%Y"
                ).date()
            
            services.edit_package(
                package,
                shipping_type=shipping_type,
                weight=weight,
                shipping_date=shipping_date,
                unit_of_work=unit_of_work.DatastoreUnitOfWork()
            )
            response_200 = jsonify(
                package_to_dict(
                    package,
                    f"{request.base_url}",
                    carrier_to_dict(package.carrier_id, f"{request.host_url}trucks")
                )
            )
            response_200.status_code = 200
            return response_200

        else:
            response_404_error = make_response(
                jsonify({
                    "Error": "No package with this package_id exists"
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
        if not json_data or not has_required_values_for_create_package(json_data) \
            or contains_unallowed_attributes(json_data):
            response_400_error = make_response({
                "Error": "The request object is missing all of the required attributes"
            })
            response_400_error.status_code = 400
            return response_400_error

        package = services.get_package(
            package_id, unit_of_work.DatastoreUnitOfWork()
        )
        if package:
            shipping_type = json_data["shipping_type"]
            weight = Decimal(str(json_data["weight"]))
            shipping_date = datetime.datetime.strptime(
                json_data["shipping_date"], "%m/%d/%Y"
            ).date()
            services.edit_package(
                package,
                shipping_type=shipping_type,
                weight=weight,
                shipping_date=shipping_date,
                unit_of_work=unit_of_work.DatastoreUnitOfWork(),
                clear_carrier=True,
            )
            response_303 = make_response()
            response_303.status_code = 303
            response_303.headers["Location"] = f"{request.host_url}packages/{package_id}"
            return response_303
        else:
            response_404_error = make_response(
                jsonify({
                    "Error": "No package with this package_id exists"
                })
            )
            response_404_error.status_code = 404
            return response_404_error

    elif request.method == "DELETE":
        response_406_error = common.check_for_accept_error_406(
            request, ["application/json"]
        )
        if response_406_error:
            return response_406_error

        package = services.get_package(
            package_id, unit_of_work.DatastoreUnitOfWork()
        )
        if package:
            delete_successful = services.delete_package(
                package_id, unit_of_work.DatastoreUnitOfWork()
            )
            if delete_successful:
                response_204 = make_response()
                response_204.status_code = 204
                return response_204
            else:
                return "Oh no", 500
        else:
            response_404_error = make_response(
                jsonify({
                    "Error": "No package with this package_id exists"
                })
            )
            response_404_error.status_code = 404
            return response_404_error