from flask import Flask, render_template, session

from trucksandpackages import auth, config, trucks

app = Flask(__name__)
app.config.from_object(config.DevelopmentConfig())

auth.register_to_auth0(app)

app.register_blueprint(auth.bp)
app.register_blueprint(trucks.bp)

@app.route("/")
def home():
    token = session.get("user")
    if token:
        return render_template(
            "home.html",
            session=token,
            unique_id=token["userinfo"]["sub"]
        )
    else:
        return render_template("home.html")
