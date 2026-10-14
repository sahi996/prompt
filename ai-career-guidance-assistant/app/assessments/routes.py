import json
from flask import render_template, redirect, url_for, flash, request, jsonify
from flask_login import login_required, current_user
from app.assessments import bp
from app.extensions import db, limiter
from app.models import Assessment, Recommendation, Career
from app.forms import AssessmentForm


@bp.route("/", methods=["GET", "POST"])
def index():
    form = AssessmentForm()
    if form.validate_on_submit():
        assessment = Assessment(
            user_id=current_user.id if current_user.is_authenticated else None,
            education_level=form.education_level.data,
            field_of_study=form.field_of_study.data,
            interests=json.dumps(form.interests.data),
            favourite_subjects=form.favourite_subjects.data,
            technical_skills=form.technical_skills.data,
            soft_skills=form.soft_skills.data,
            preferred_activities=json.dumps(form.preferred_activities.data),
            career_goals=form.career_goals.data,
            working_style=form.working_style.data,
        )
        db.session.add(assessment)
        db.session.flush()

        from app.ai_services.ai_service import get_career_recommendations
        recommendations, used_ai = get_career_recommendations(assessment)

        for rec in recommendations:
            career = Career.query.filter_by(slug=rec["slug"]).first()
            if career:
                r = Recommendation(
                    assessment_id=assessment.id,
                    career_id=career.id,
                    score=rec.get("score", 0),
                    match_reason=rec.get("reason", ""),
                    ai_explanation=rec.get("ai_explanation", ""),
                )
                db.session.add(r)

        db.session.commit()
        return redirect(url_for("assessments.results", assessment_id=assessment.id))

    return render_template("assessments/form.html", form=form)


@bp.route("/results/<int:assessment_id>")
def results(assessment_id):
    assessment = Assessment.query.get_or_404(assessment_id)
    # Authorization: only the owner OR anonymous (user_id is None) can view
    if assessment.user_id and (not current_user.is_authenticated or current_user.id != assessment.user_id):
        flash("You don't have permission to view that assessment.", "danger")
        return redirect(url_for("assessments.index"))
    recommendations = (
        Recommendation.query
        .filter_by(assessment_id=assessment_id)
        .order_by(Recommendation.score.desc())
        .all()
    )
    return render_template(
        "assessments/results.html",
        assessment=assessment,
        recommendations=recommendations,
        used_ai=any(r.ai_explanation for r in recommendations),
    )


@bp.route("/history")
@login_required
def history():
    assessments = (
        Assessment.query
        .filter_by(user_id=current_user.id)
        .order_by(Assessment.created_at.desc())
        .all()
    )
    return render_template("assessments/history.html", assessments=assessments)


@bp.route("/interview-feedback", methods=["POST"])
@limiter.limit("30 per hour")
def interview_feedback():
    data = request.get_json(silent=True) or {}
    question = data.get("question", "")
    answer = data.get("answer", "")
    career_title = data.get("career_title", "")
    if not answer or not question:
        return jsonify({"feedback": "Please provide both a question and an answer."}), 400
    from app.ai_services.ai_service import generate_interview_feedback
    feedback = generate_interview_feedback(question, answer, career_title)
    return jsonify({"feedback": feedback})
