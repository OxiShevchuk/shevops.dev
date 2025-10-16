from extensions import db, login_manager
from flask_login import UserMixin, login_required



class User(db.Model, UserMixin):
    """
    SQLAlchemy model for user accounts.
    Inherits from UserMixin to provide the attributes Flask-Login expects:
      - is_authenticated, is_active, is_anonymous, get_id()
    """
    __tablename__ = "users"

    uid = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)
    is_active = db.Column(db.Boolean, default=True, nullable=False)

    def get_id(self):
        return str(self.uid)