from flask import request, render_template, redirect, url_for, Blueprint
from extensions import db
from services.models import Service


services_bp = Blueprint("services", __name__, template_folder="templates")

@services_bp.route('/')
def public_services():
    services = Service.query.all()
    return render_template('services/public.html', services=services)