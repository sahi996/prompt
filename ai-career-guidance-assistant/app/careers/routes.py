import json
from flask import render_template, request, redirect, url_for
from app.careers import bp
from app.models import Career, Skill


@bp.route("/")
def explore():
    q = request.args.get("q", "").strip()
    category = request.args.get("category", "")
    beginner = request.args.get("beginner", "")

    query = Career.query
    if q:
        query = query.filter(
            Career.title.ilike(f"%{q}%") |
            Career.description.ilike(f"%{q}%") |
            Career.short_description.ilike(f"%{q}%")
        )
    if category:
        query = query.filter_by(category=category)
    if beginner == "1":
        query = query.filter_by(is_beginner_friendly=True)

    careers = query.order_by(Career.title).all()
    categories = [r[0] for r in Career.query.with_entities(Career.category).distinct().order_by(Career.category).all()]

    return render_template(
        "careers/explore.html",
        careers=careers,
        categories=categories,
        q=q,
        selected_category=category,
        beginner_filter=beginner,
    )


@bp.route("/<slug>")
def detail(slug):
    career = Career.query.filter_by(slug=slug).first_or_404()
    is_saved = False
    from flask_login import current_user
    if current_user.is_authenticated:
        is_saved = career in current_user.saved_careers
    return render_template("careers/detail.html", career=career, is_saved=is_saved)
