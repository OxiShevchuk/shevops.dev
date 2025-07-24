from flask import Flask, render_template, request, redirect, url_for
from flask_bootstrap import Bootstrap5
from flask_sqlalchemy import SQLAlchemy
from extensions import db
from dotenv import load_dotenv
import os
import html

from services.models import db, Service

load_dotenv()  # This loads variables from .env


app = Flask(__name__)
Bootstrap5(app)
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv("DATABASE_URL")
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)

# Create DB
with app.app_context():
    db.create_all()


# import and register all Blueprints

from services.routes import services_bp
app.register_blueprint(services_bp, url_prefix="/services")

@app.route("/")
def home():
    services = Service.query.all()
    print(services[0].name)
    return render_template("index.html", services=services)


# @app.route("/admin")
# def admin():
#     services = Service.query.all()
#     return render_template("dashboard.html", services=services)



if (__name__) == "__main__":
    app.run(debug=True)