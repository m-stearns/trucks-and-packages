import os

from dotenv import find_dotenv, load_dotenv

load_dotenv(find_dotenv())

class BaseConfig(object):
    FLASK_APP = "trucksanditems"
    STATIC_FOLDER = "static"
    TEMPLATES_FOLDER = "templates"
    AUTH0_DOMAIN = os.environ.get("AUTH0_DOMAIN")
    AUTH0_CLIENT_ID = os.environ.get("AUTH0_CLIENT_ID")
    AUTH0_CLIENT_SECRET = os.environ.get("AUTH0_CLIENT_SECRET")
    SECRET_KEY = os.environ.get("SECRET_KEY")

class DevelopmentConfig(BaseConfig):
    FLASK_ENV = os.environ.get("FLASK_ENV")
    DEBUG = True
    TESTING = True

class ProductionConfig(BaseConfig):
    FLASK_ENV = os.environ.get("FLASK_ENV")
    DEBUG = False
    TESTING = False