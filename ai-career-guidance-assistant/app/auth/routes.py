from datetime import datetime
from flask import render_template, redirect, url_for, flash, request
from flask_login import login_user, logout_user, login_required, current_user
from app.auth import bp
from app.extensions import db, limiter
from app.models import User, Profile
from app.forms import RegistrationForm, LoginForm


@bp.route("/register", methods=["GET", "POST"])
@limiter.limit("10 per hour")
def register():
    if current_user.is_authenticated:
        return redirect(url_for("dashboard.index"))
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(
            username=form.username.data.strip(),
            email=form.email.data.lower().strip(),
        )
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.flush()
        profile = Profile(user_id=user.id)
        db.session.add(profile)
        db.session.commit()
        login_user(user)
        flash("Welcome to AI Career Guidance Assistant! Your account has been created.", "success")
        return redirect(url_for("dashboard.index"))
    return render_template("auth/register.html", form=form)


@bp.route("/login", methods=["GET", "POST"])
@limiter.limit("20 per hour")
def login():
    if current_user.is_authenticated:
        return redirect(url_for("dashboard.index"))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data.lower().strip()).first()
        if user and user.check_password(form.password.data) and user.is_active:
            login_user(user, remember=form.remember.data)
            user.last_login = datetime.utcnow()
            db.session.commit()
            next_page = request.args.get("next")
            # Safety check: only allow relative redirects
            if next_page and next_page.startswith("/"):
                return redirect(next_page)
            return redirect(url_for("dashboard.index"))
        flash("Invalid email or password.", "danger")
    return render_template("auth/login.html", form=form)


@bp.route("/logout")
@login_required
def logout():
    logout_user()
    flash("You have been logged out.", "info")
    return redirect(url_for("main.index"))
