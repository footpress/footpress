import jwt
import os
from flask import Flask, request, abort, render_template
from flask_sqlalchemy import SQLAlchemy


config = dict(
    DEBUG=False,
    TESTING=False,
    SQLALCHEMY_DATABASE_URI="sqlite:///db.sqlite",
    SQLALCHEMY_TRACK_MODIFICATIONS=False,
    SECRET_KEY=os.environ.get("SECRET_KEY","mm7hEF8VcfQPkQ9M4rFe3MaKStDLgxnEwUkp7uwNPR8n9vUJNSryCcTgLpAY",)
)

app = Flask(__name__)
app.config.update(**config)
db = SQLAlchemy(app)


class Supporter(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.Text, nullable=False)
    password = db.Column(db.Text, nullable=False)


@app.route("/")
@app.route("/index")
def index():
    return render_template("index.html")


@app.route("/admin")
def admin():
    if is_token_valid(request):
        supporters = Supporter.query.all()
        return render_template("admin.html", supporters=supporters)
    else:
        return abort(403)


def is_token_valid(request):
    if request.headers.get("X-TOKEN", None):
        try:
            jwt_token = request.headers.get("X-TOKEN", None)
            jwt.decode(jwt_token, app.config["SECRET_KEY"], "HS256")
            return True
        except:
            return false
    else:
        return False

