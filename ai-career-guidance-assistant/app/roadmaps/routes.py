import json
from datetime import datetime
from flask import render_template, redirect, url_for, flash, request, jsonify
from flask_login import login_required, current_user
from app.roadmaps import bp
from app.extensions import db
from app.models import Career, Roadmap, RoadmapStage, UserRoadmapProgress


@bp.route("/")
def index():
    careers_with_roadmaps = (
        Career.query
        .join(Roadmap)
        .order_by(Career.title)
        .all()
    )
    return render_template("roadmaps/index.html", careers=careers_with_roadmaps)


@bp.route("/<career_slug>")
def view(career_slug):
    career = Career.query.filter_by(slug=career_slug).first_or_404()
    roadmap = Roadmap.query.filter_by(career_id=career.id).first_or_404()

    # Build progress map for logged-in users
    progress_map = {}
    if current_user.is_authenticated:
        records = UserRoadmapProgress.query.filter_by(
            user_id=current_user.id,
            roadmap_id=roadmap.id,
        ).all()
        progress_map = {r.stage_id: r for r in records}

    total = len(roadmap.stages)
    done = sum(1 for sid, r in progress_map.items() if r.completed)
    pct = int(done / total * 100) if total else 0

    return render_template(
        "roadmaps/view.html",
        career=career,
        roadmap=roadmap,
        progress_map=progress_map,
        pct=pct,
        done=done,
        total=total,
    )


@bp.route("/<int:roadmap_id>/progress", methods=["POST"])
@login_required
def update_progress(roadmap_id):
    data = request.get_json(silent=True) or {}
    stage_id = data.get("stage_id")
    completed = bool(data.get("completed"))

    if not stage_id:
        return jsonify({"error": "stage_id required"}), 400

    stage = RoadmapStage.query.get_or_404(int(stage_id))
    roadmap = Roadmap.query.get_or_404(roadmap_id)

    # Security: ensure stage belongs to roadmap
    if stage.roadmap_id != roadmap_id:
        return jsonify({"error": "forbidden"}), 403

    record = UserRoadmapProgress.query.filter_by(
        user_id=current_user.id,
        roadmap_id=roadmap_id,
        stage_id=stage.id,
    ).first()

    if not record:
        record = UserRoadmapProgress(
            user_id=current_user.id,
            roadmap_id=roadmap_id,
            stage_id=stage.id,
        )
        db.session.add(record)

    record.completed = completed
    if completed:
        record.completed_at = datetime.utcnow()
    else:
        record.completed_at = None
    db.session.commit()

    # Recalculate percentage
    all_stages = RoadmapStage.query.filter_by(roadmap_id=roadmap_id).count()
    done = UserRoadmapProgress.query.filter_by(
        user_id=current_user.id,
        roadmap_id=roadmap_id,
        completed=True,
    ).count()
    pct = int(done / all_stages * 100) if all_stages else 0

    return jsonify({"ok": True, "percent": pct, "done": done, "total": all_stages})
