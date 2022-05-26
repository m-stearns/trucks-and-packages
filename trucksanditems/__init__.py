from flask import Flask

from trucksanditems import config

app = Flask(__name__)
app.config.from_object(config.DevelopmentConfig())

@app.route("/")
def home():
    return "You're home!"