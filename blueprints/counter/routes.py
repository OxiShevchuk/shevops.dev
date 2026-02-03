from flask import Blueprint
from extensions import db
from blueprints.counter.models import Counter


counter_bp = Blueprint("counter")