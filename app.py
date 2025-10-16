from flask import Flask, request
from flask_bootstrap import Bootstrap5
from flask_sqlalchemy import SQLAlchemy
from extensions import db, login_manager
from dotenv import load_dotenv
import os
import html
from flask_login import LoginManager

from blueprints.main import main_bp
from blueprints.services.models import db, Service
from blueprints.faq.models import db, Faq

load_dotenv()  # This loads variables from .env


app = Flask(__name__)
Bootstrap5(app)
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv("DATABASE_URL")
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# python -c "import secrets; print(secrets.token_hex(32))"
# to generate a secret key
app.secret_key = os.getenv("SECRET_KEY")

db.init_app(app)

# Create DB
with app.app_context():
    db.create_all()



# ---- Flask-Login setup ----
login_manager.init_app(app)
login_manager.login_view = "auth.login" # redirect here if @login_required fails
login_manager.login_message = "You must log in to continue."
login_manager.login_message_category = "warning"



# import and register all Blueprints
app.register_blueprint(main_bp)

from blueprints.auth.routes import auth_bp
app.register_blueprint(auth_bp, url_prefix=None)

from blueprints.admin.routes import admin_bp
app.register_blueprint(admin_bp, url_prefix='/admin')

from blueprints.services.routes import services_bp
app.register_blueprint(services_bp, url_prefix="/services")

from blueprints.faq.routes import faq_bp
app.register_blueprint(faq_bp, url_prefix="/faq")


# @app.route("/")
# def home():
#     services = Service.query.all()
#     faqs = Faq.query.all()
#     return render_template("index.html", services=services, faqs=faqs)



if (__name__) == "__main__":
    app.run(debug=True)