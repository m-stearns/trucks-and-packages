
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

@bp.route("", methods=["GET", "POST"])
def get_package():
    if request.method == "GET":
        return "OK", 200
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
