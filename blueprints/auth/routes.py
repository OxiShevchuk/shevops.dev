from flask import request, render_template, redirect, url_for, Blueprint, flash
from flask_login import login_user, logout_user, login_required, current_user
from .forms import LoginForm
from extensions import db
from blueprints.auth.models import User
from werkzeug.security import check_password_hash


auth_bp = Blueprint("auth", __name__, template_folder="templates")


# Login route
@auth_bp.route("/login", methods=["GET", "POST"])
def login():
    form = LoginForm()

    if request.method == "POST":
        username = form.username.data
        password = form.password.data
        user = User.query.filter_by(username=username).first()
        if user and check_password_hash(user.password_hash, password):
            login_user(user)
            flash("Login successful!", "success")
            return redirect(url_for("admin.dashboard"))
        else:
            flash("Invalid username or password", "danger")
            return render_template("auth/login.html", form=form)

    return render_template("auth/login.html", form=form)

@auth_bp.route("/logout")
@login_required
def logout():
    logout_user()  # <-- clears session
    return redirect(url_for("main.home"))