from flask import Blueprint
from extensions import db
from blueprints.why_choose_me.models import Reason


why_choose_me_bp = Blueprint("why_choose_me", __name__, template_folder="templates")