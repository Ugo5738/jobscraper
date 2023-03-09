from flask import flash, redirect, render_template, request, url_for
from flask_login import current_user, login_user, logout_user
from werkzeug.security import check_password_hash, generate_password_hash

from app.auth import bp
from app.extensions import db
from app.models.admin import admin_models

# from app.forms.auth import LoginForm, SignUpForm


@bp.route("/signup", methods=["GET"])
def signup():
    return render_template("auth/signup.html")


@bp.route("/signup", methods=["POST"])
def signup_post():
    email = request.form.get("email")
    name = request.form.get("name")
    password = request.form.get("password")

    user = admin_models.User.query.filter_by(email=email).first()

    if user:  # if a user is found, we want to redirect back to signup page so user can try again
        flash("Email address already exists")
        return redirect(url_for("auth.signup"))

    # create a new user with the form data. Hash the password so the plaintext version isn't saved.
    new_user = admin_models.User(
        email=email, name=name, password=generate_password_hash(password, method="sha256")
    )

    # add the new user to the database
    db.session.add(new_user)
    db.session.commit()

    return redirect(url_for("auth.login"))


@bp.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form.get("email")
        password = request.form.get("password")
        remember = True if request.form.get("remember") else False

        user = admin_models.User.query.filter_by(email=email).first()

        login_user(user)

        # if the above check passes, then we know the user has the right credentials
        return redirect(url_for("admin.index"))
    return render_template("auth/login.html")


@bp.route("/logout")
def logout():
    logout_user()
    return redirect(url_for("auth.login"))
