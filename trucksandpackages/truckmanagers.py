import re
from flask import Blueprint, jsonify, make_response, request

from trucksandpackages.domain import model
from trucksandpackages import common
from trucksandpackages.services import services, unit_of_work

bp = Blueprint("truckmanagers", __name__, url_prefix="/truckmanagers")

@bp.route("", methods=["GET"])
def get_all_truck_managers():
    if request.method == "GET":
        response_406_error = common.check_for_accept_error_406(
            request, ["application/json"]
        )
        if response_406_error:
            return response_406_error

        truck_managers = services.get_all_truck_managers(
            unit_of_work.DatastoreUnitOfWork()
        )
        response_200 = make_response()
        response_200.status_code = 200
        return response_200