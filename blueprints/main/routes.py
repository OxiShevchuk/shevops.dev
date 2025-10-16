from flask import render_template
from . import main_bp
from blueprints.services.models import Service
from blueprints.faq.models import Faq
import logging



# Set log level (DEBUG for dev, WARNING for prod)
logging.basicConfig(level=logging.DEBUG)

@main_bp.route("/")
def home():
    logging.debug("Inside home() route")
    services = Service.query.all()
    faqs = Faq.query.order_by(Faq.sort_order, Faq.fid).all()
    return render_template("main/index.html", services=services, faqs=faqs)