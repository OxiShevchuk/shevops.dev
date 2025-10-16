from .models import User, login_manager


# Flask-Login requires a user_loader callback
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))