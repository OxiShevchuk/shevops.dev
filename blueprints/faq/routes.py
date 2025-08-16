from flask import request, render_template, redirect, url_for, Blueprint
from extensions import db
from blueprints.faq.models import Faq


faq_bp = Blueprint("faq", __name__, template_folder="templates")

@faq_bp.route('/')
def public_faq():
    faq = Faq.query.all()
    return render_template('faq/public.html', faq=faq)