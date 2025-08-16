from flask import Blueprint

admin_bp = Blueprint(
    'admin',
    __name__,
    template_folder='templates',
    static_folder='static',
    static_url_path='/static'
)

from . import routes  # Import routes to register them
