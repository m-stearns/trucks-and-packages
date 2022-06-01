from typing import List

from flask import request, Response, make_response

def check_for_content_type_error_415(req: request) -> Response:
    if "Content-Type" not in req.headers or \
        req.headers["Content-Type"] != "application/json":
        error_res = make_response("Unsupported Media Type")
        error_res.status_code = 415
        return error_res
    else:
        return None

def check_for_accept_error_406(
    req: request, acceptable_MIME_types: List[str]
) -> Response:
    for mime_type in acceptable_MIME_types:
        if "Accept" in req.headers and mime_type == req.headers["Accept"]:
            return None
    error_res = make_response("Not Acceptable")
    error_res.status_code = 406
    return error_res