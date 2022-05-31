import json
from typing import List
from urllib.parse import quote_plus, urlencode
from urllib.request import urlopen

import flask
from authlib.integrations.flask_client import OAuth
from jose import jwt

from trucksandpackages import exceptions
from trucksandpackages.services import services, unit_of_work
from trucksandpackages.domain import model

bp = flask.Blueprint("auth", __name__, url_prefix="/auth")

def register_to_auth0(app: flask.Flask) -> OAuth:
    oauth = OAuth(app)
    auth0 = oauth.register(
        "auth0",
        client_id=app.config["AUTH0_CLIENT_ID"],
        client_secret=app.config["AUTH0_CLIENT_SECRET"],
        api_base_url=f"https://{app.config['AUTH0_DOMAIN']}",
        access_token_url=f"https://{app.config['AUTH0_DOMAIN']}/oauth/token",
        authorize_url=f"https://{app.config['AUTH0_DOMAIN']}/authorize",
        client_kwargs={
            "scope": "openid profile email"
        },
        server_metadata_url=f'https://{app.config["AUTH0_DOMAIN"]}/.well-known/openid-configuration'
    )
    app.config["oauth"] = oauth

def verify_jwt(request):
    """
    Verifies the JWT supplied in a request's Authorization header.
    Code pulled from the 'Authentication in Python' exploration from Week 7's module.
    """
    if 'Authorization' in request.headers:
        auth_header = request.headers['Authorization'].split()
        token = auth_header[1]
    else:
        raise exceptions.NoAuthHeaderError(
            {
                "code": "no auth header",
                "description": "Authorization header is missing"
            },
            401
        )
    
    jsonurl = urlopen("https://"+ flask.current_app.config["AUTH0_DOMAIN"] + \
        "/.well-known/jwks.json")
    jwks = json.loads(jsonurl.read())
    
    try:
        unverified_header = jwt.get_unverified_header(token)
    except jwt.JWTError:
        raise exceptions.InvalidHeaderError(
            {
                "code": "invalid_header",
                "description": "Invalid header. Use an RS256 signed JWT Access Token"
            }, 
            401
        )
    if unverified_header["alg"] == "HS256":
        raise exceptions.InvalidHeaderError(
            {
                "code": "invalid_header",
                "description": "Invalid header. Use an RS256 signed JWT Access Token"
            },
            401
        )
    
    rsa_key = {}
    for key in jwks["keys"]:
        if key["kid"] == unverified_header["kid"]:
            rsa_key = {
                "kty": key["kty"],
                "kid": key["kid"],
                "use": key["use"],
                "n": key["n"],
                "e": key["e"]
            }
    if rsa_key:
        try:
            payload = jwt.decode(
                token,
                rsa_key,
                algorithms=["RS256"],
                audience=flask.current_app.config["AUTH0_CLIENT_ID"],
                issuer="https://"+ flask.current_app.config["AUTH0_DOMAIN"] + "/"
            )
        except jwt.ExpiredSignatureError:
            raise exceptions.TokenExpiredError(
                {
                    "code": "token_expired",
                    "description": "token is expired"
                },
                401
            )
        except jwt.JWTClaimsError:
            raise exceptions.InvalidClaimsError(
                {
                    "code": "invalid_claims",
                    "description": "incorrect claims, please check the audience and issuer"
                },
                401
            )
        except Exception:
            raise exceptions.InvalidHeaderError(
                {
                    "code": "invalid_header",
                    "description": "Unable to parse authentication token."
                },
            401)

        return payload
    else:
        raise exceptions.NoRSAKeyError(
            {
                "code": "no_rsa_key",
                "description": "No RSA key in JWKS"
            },
            401
        )

def user_already_saved(auth_id: str, users: List[model.User]) -> bool:
    for user in users:
        if user.auth_id == auth_id:
            return True
    return False

@bp.route("/login")
def login():
    oauth: OAuth = flask.current_app.config["oauth"]
    return oauth.auth0.authorize_redirect(
        redirect_uri=flask.url_for("auth.callback", _external=True)
    )

@bp.route("/callback", methods=["GET", "POST"])
def callback():
    oauth = flask.current_app.config["oauth"]
    token = oauth.auth0.authorize_access_token()

    auth_id = token["userinfo"]["sub"]
    users = services.get_all_truck_managers(unit_of_work.DatastoreUnitOfWork())
    if not user_already_saved(auth_id, users):
        services.create_truck_manager(
            auth_id, unit_of_work.DatastoreUnitOfWork()
        )
    
    flask.session["user"] = token
    return flask.redirect("/")

@bp.route("/logout")
def logout():
    flask.session.clear()
    redirect_url = f"https://{flask.current_app.config['AUTH0_DOMAIN']}/v2/logout?"
    redirect_url += urlencode(
        {
            "returnTo": flask.url_for("home", _external=True),
            "client_id": flask.current_app.config["AUTH0_CLIENT_ID"]
        },
        quote_via=quote_plus
    )
    return flask.redirect(redirect_url)
