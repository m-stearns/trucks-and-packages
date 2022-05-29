import json

from flask import Flask, render_template, session

from trucksandpackages import auth, config

app = Flask(__name__)
app.config.from_object(config.DevelopmentConfig())

auth.register_to_auth0(app)

app.register_blueprint(auth.bp)

@app.route("/")
def home():
    return render_template(
        "home.html",
        session=session.get("user"),
        pretty=json.dumps(session.get("user"), indent=4)
    )
