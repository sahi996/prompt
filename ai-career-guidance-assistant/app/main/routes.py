from datetime import datetime
from flask import render_template, request, flash, redirect, url_for
from app.main import bp
from app.models import Career
from app.forms import ContactForm


@bp.context_processor
def inject_now():
    return {"now": datetime.utcnow()}


@bp.route("/")
def index():
    featured = Career.query.filter_by(is_beginner_friendly=True).limit(6).all()
    all_careers = Career.query.limit(10).all()
    return render_template("main/index.html", featured=featured, all_careers=all_careers)


@bp.route("/about")
def about():
    return render_template("main/about.html")


@bp.route("/features")
def features():
    return render_template("main/features.html")


@bp.route("/skills-analysis")
def skills_analysis():
    careers = Career.query.order_by(Career.title).all()
    return render_template("main/skills_analysis.html", careers=careers)


@bp.route("/projects")
def projects():
    from app.models import Project
    beginner = Project.query.filter_by(difficulty="Beginner").limit(6).all()
    intermediate = Project.query.filter_by(difficulty="Intermediate").limit(6).all()
    advanced = Project.query.filter_by(difficulty="Advanced").limit(4).all()
    return render_template("main/projects.html",
                           beginner=beginner,
                           intermediate=intermediate,
                           advanced=advanced)


@bp.route("/resume-prep")
def resume_prep():
    return render_template("main/resume_prep.html")


@bp.route("/contact", methods=["GET", "POST"])
def contact():
    form = ContactForm()
    if form.validate_on_submit():
        # In production you'd send an email here; we log it and show confirmation
        flash("Thank you for your message! We'll get back to you soon.", "success")
        return redirect(url_for("main.contact"))
    return render_template("main/contact.html", form=form)


@bp.route("/privacy")
def privacy():
    return render_template("main/privacy.html")


@bp.route("/terms")
def terms():
    return render_template("main/terms.html")


@bp.route("/health")
def health():
    from flask import jsonify
    from app.extensions import db
    try:
        db.session.execute(db.text("SELECT 1"))
        db_ok = True
    except Exception:
        db_ok = False
    return jsonify({"status": "ok", "db": db_ok}), 200
