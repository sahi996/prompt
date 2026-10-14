import json
from datetime import datetime, date
from flask import render_template, redirect, url_for, flash, request, abort
from flask_login import login_required, current_user
from app.dashboard import bp
from app.extensions import db
from app.models import (
    Career, SkillAnalysis, SkillAnalysisItem, Skill,
    UserRoadmapProgress, ResumeDraft, InterviewSession, JobApplication, Profile
)
from app.forms import ProfileForm, ResumeDraftForm, JobApplicationForm


def _get_profile():
    profile = current_user.profile
    if not profile:
        profile = Profile(user_id=current_user.id)
        db.session.add(profile)
        db.session.commit()
    return profile


@bp.route("/")
@login_required
def index():
    profile = _get_profile()

    # Progress stats
    total_stages = UserRoadmapProgress.query.filter_by(user_id=current_user.id).count()
    done_stages = UserRoadmapProgress.query.filter_by(user_id=current_user.id, completed=True).count()
    roadmap_pct = int((done_stages / total_stages * 100) if total_stages else 0)

    saved_count = len(current_user.saved_careers)
    assessment_count = len(current_user.assessments)
    app_count = len(current_user.job_applications)

    recent_apps = JobApplication.query.filter_by(user_id=current_user.id).order_by(
        JobApplication.updated_at.desc()).limit(5).all()

    return render_template(
        "dashboard/index.html",
        profile=profile,
        roadmap_pct=roadmap_pct,
        done_stages=done_stages,
        total_stages=total_stages,
        saved_count=saved_count,
        assessment_count=assessment_count,
        app_count=app_count,
        recent_apps=recent_apps,
    )


@bp.route("/profile", methods=["GET", "POST"])
@login_required
def profile():
    profile = _get_profile()
    form = ProfileForm(obj=profile)
    if form.validate_on_submit():
        form.populate_obj(profile)
        profile.updated_at = datetime.utcnow()
        db.session.commit()
        flash("Profile updated successfully.", "success")
        return redirect(url_for("dashboard.profile"))
    return render_template("dashboard/profile.html", form=form, profile=profile)


@bp.route("/saved-careers")
@login_required
def saved_careers():
    return render_template("dashboard/saved_careers.html", careers=current_user.saved_careers)


@bp.route("/saved-careers/toggle/<int:career_id>", methods=["POST"])
@login_required
def toggle_saved_career(career_id):
    career = Career.query.get_or_404(career_id)
    if career in current_user.saved_careers:
        current_user.saved_careers.remove(career)
        flash(f"Removed '{career.title}' from saved careers.", "info")
    else:
        current_user.saved_careers.append(career)
        flash(f"Saved '{career.title}' to your careers.", "success")
    db.session.commit()
    return redirect(request.referrer or url_for("dashboard.saved_careers"))


@bp.route("/skill-analysis")
@bp.route("/skill-analysis/<int:career_id>")
@login_required
def skill_analysis(career_id=None):
    careers = Career.query.order_by(Career.title).all()
    analysis = None
    selected_career = None

    if career_id:
        selected_career = Career.query.get_or_404(career_id)
        analysis = SkillAnalysis.query.filter_by(
            user_id=current_user.id, career_id=career_id
        ).first()

    return render_template(
        "dashboard/skill_analysis.html",
        careers=careers,
        selected_career=selected_career,
        analysis=analysis,
    )


@bp.route("/skill-analysis/save/<int:career_id>", methods=["POST"])
@login_required
def save_skill_analysis(career_id):
    career = Career.query.get_or_404(career_id)
    known_ids = set(int(x) for x in request.form.getlist("known_skills"))

    analysis = SkillAnalysis.query.filter_by(
        user_id=current_user.id, career_id=career_id
    ).first()
    if not analysis:
        analysis = SkillAnalysis(user_id=current_user.id, career_id=career_id)
        db.session.add(analysis)
        db.session.flush()

    # Remove existing items and rebuild
    SkillAnalysisItem.query.filter_by(analysis_id=analysis.id).delete()
    for skill in career.skills:
        item = SkillAnalysisItem(
            analysis_id=analysis.id,
            skill_id=skill.id,
            known=(skill.id in known_ids),
        )
        db.session.add(item)
    db.session.commit()
    flash("Skill analysis saved.", "success")
    return redirect(url_for("dashboard.skill_analysis", career_id=career_id))


@bp.route("/roadmaps")
@login_required
def roadmaps():
    progresses = UserRoadmapProgress.query.filter_by(user_id=current_user.id).all()
    # Group by roadmap
    roadmap_ids = {p.roadmap_id for p in progresses}
    from app.models import Roadmap
    roadmaps_list = []
    for rid in roadmap_ids:
        roadmap = db.session.get(Roadmap, rid)
        if roadmap:
            total = len(roadmap.stages)
            done = sum(1 for p in progresses if p.roadmap_id == rid and p.completed)
            pct = int(done / total * 100) if total else 0
            roadmaps_list.append({"roadmap": roadmap, "done": done, "total": total, "pct": pct})
    return render_template("dashboard/roadmaps.html", roadmaps_list=roadmaps_list)


@bp.route("/resume", methods=["GET"])
@login_required
def resume():
    drafts = ResumeDraft.query.filter_by(user_id=current_user.id).order_by(ResumeDraft.updated_at.desc()).all()
    return render_template("dashboard/resume.html", drafts=drafts)


@bp.route("/resume/new", methods=["GET", "POST"])
@bp.route("/resume/edit/<int:draft_id>", methods=["GET", "POST"])
@login_required
def edit_resume(draft_id=None):
    draft = None
    if draft_id:
        draft = ResumeDraft.query.filter_by(id=draft_id, user_id=current_user.id).first_or_404()

    form = ResumeDraftForm()
    if request.method == "GET" and draft:
        form.title.data = draft.title
        form.target_career.data = draft.target_career
        content = json.loads(draft.content or "{}")
        form.objective.data = content.get("objective", "")
        form.education.data = content.get("education", "")
        form.experience.data = content.get("experience", "")
        form.skills_text.data = content.get("skills_text", "")
        form.projects_text.data = content.get("projects_text", "")
        form.certifications.data = content.get("certifications", "")

    if form.validate_on_submit():
        content = json.dumps({
            "objective": form.objective.data,
            "education": form.education.data,
            "experience": form.experience.data,
            "skills_text": form.skills_text.data,
            "projects_text": form.projects_text.data,
            "certifications": form.certifications.data,
        })
        if draft:
            draft.title = form.title.data
            draft.target_career = form.target_career.data
            draft.content = content
            draft.updated_at = datetime.utcnow()
        else:
            draft = ResumeDraft(
                user_id=current_user.id,
                title=form.title.data,
                target_career=form.target_career.data,
                content=content,
            )
            db.session.add(draft)
        db.session.commit()
        flash("Resume draft saved.", "success")
        return redirect(url_for("dashboard.resume"))

    return render_template("dashboard/edit_resume.html", form=form, draft=draft)


@bp.route("/resume/delete/<int:draft_id>", methods=["POST"])
@login_required
def delete_resume(draft_id):
    draft = ResumeDraft.query.filter_by(id=draft_id, user_id=current_user.id).first_or_404()
    db.session.delete(draft)
    db.session.commit()
    flash("Resume draft deleted.", "info")
    return redirect(url_for("dashboard.resume"))


@bp.route("/interviews")
@login_required
def interviews():
    sessions = InterviewSession.query.filter_by(user_id=current_user.id).order_by(
        InterviewSession.created_at.desc()).all()
    return render_template("dashboard/interviews.html", sessions=sessions)


@bp.route("/applications")
@login_required
def applications():
    apps = JobApplication.query.filter_by(user_id=current_user.id).order_by(
        JobApplication.updated_at.desc()).all()
    return render_template("dashboard/applications.html", apps=apps)


@bp.route("/applications/new", methods=["GET", "POST"])
@bp.route("/applications/edit/<int:app_id>", methods=["GET", "POST"])
@login_required
def add_application(app_id=None):
    app_obj = None
    if app_id:
        app_obj = JobApplication.query.filter_by(id=app_id, user_id=current_user.id).first_or_404()

    form = JobApplicationForm(obj=app_obj)
    if form.validate_on_submit():
        if app_obj:
            form.populate_obj(app_obj)
            app_obj.updated_at = datetime.utcnow()
        else:
            app_obj = JobApplication(user_id=current_user.id)
            form.populate_obj(app_obj)
            db.session.add(app_obj)
        db.session.commit()
        flash("Application saved.", "success")
        return redirect(url_for("dashboard.applications"))

    return render_template("dashboard/edit_application.html", form=form, app_obj=app_obj)


@bp.route("/applications/delete/<int:app_id>", methods=["POST"])
@login_required
def delete_application(app_id):
    app_obj = JobApplication.query.filter_by(id=app_id, user_id=current_user.id).first_or_404()
    db.session.delete(app_obj)
    db.session.commit()
    flash("Application deleted.", "info")
    return redirect(url_for("dashboard.applications"))
