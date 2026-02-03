from flask import render_template
from . import main_bp
from blueprints.services.models import Service
from blueprints.why_choose_me.models import Reason


@main_bp.route("/")
def home():
    services = Service.query.all()
    reasons = Reason.query.order_by(Reason.sort_order, Reason.id).all()
    return render_template("main/index.html", services=services, reasons=reasons)