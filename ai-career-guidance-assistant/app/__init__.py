import os
import logging
from flask import Flask
from config import get_config
from app.extensions import db, login_manager, csrf, migrate, limiter, bcrypt


def create_app(config_class=None):
    app = Flask(__name__, template_folder="templates", static_folder="static")

    # ── Configuration ────────────────────────────────────────────────────────
    if config_class is None:
        config_class = get_config()
    app.config.from_object(config_class)

    # ── Logging ──────────────────────────────────────────────────────────────
    if not app.debug:
        logging.basicConfig(level=logging.INFO)

    # ── Extensions ───────────────────────────────────────────────────────────
    db.init_app(app)
    bcrypt.init_app(app)
    login_manager.init_app(app)
    csrf.init_app(app)
    migrate.init_app(app, db)
    limiter.init_app(app)

   

    # ── User loader ──────────────────────────────────────────────────────────
    from app.models import User

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    # ── Blueprints ───────────────────────────────────────────────────────────
    from app.main import bp as main_bp
    from app.auth import bp as auth_bp
    from app.careers import bp as careers_bp
    from app.assessments import bp as assessments_bp
    from app.roadmaps import bp as roadmaps_bp
    from app.dashboard import bp as dashboard_bp

    app.register_blueprint(main_bp)
    app.register_blueprint(auth_bp, url_prefix="/auth")
    app.register_blueprint(careers_bp, url_prefix="/careers")
    app.register_blueprint(assessments_bp, url_prefix="/assessment")
    app.register_blueprint(roadmaps_bp, url_prefix="/roadmaps")
    app.register_blueprint(dashboard_bp, url_prefix="/dashboard")

    # ── Template filters ─────────────────────────────────────────────────────
    from app.template_filters import register_filters
    register_filters(app)

    # ── CLI commands ─────────────────────────────────────────────────────────
    _register_cli(app)

    # ── Error handlers ───────────────────────────────────────────────────────
    _register_error_handlers(app)

    return app


def _register_cli(app):
    import click
    from flask.cli import with_appcontext

    @app.cli.command("seed-db")
    @with_appcontext
    def seed_db():
        """Seed database with careers, skills, roadmaps, and projects."""
        from app.seed_data import SKILLS_DATA, CAREERS_DATA, ROADMAPS_DATA, PROJECTS_DATA
        from app.models import Skill, Career, Roadmap, RoadmapStage, Project

        click.echo("Seeding skills…")
        skill_map = {}
        for s in SKILLS_DATA:
            existing = Skill.query.filter_by(name=s["name"]).first()
            if not existing:
                skill = Skill(**s)
                db.session.add(skill)
                db.session.flush()
                skill_map[s["name"]] = skill
            else:
                skill_map[s["name"]] = existing
        db.session.commit()

        click.echo("Seeding careers…")
        for c in CAREERS_DATA:
            if Career.query.filter_by(slug=c["slug"]).first():
                continue
            skill_names = c.pop("skills", [])
            career = Career(**c)
            for sname in skill_names:
                if sname in skill_map:
                    career.skills.append(skill_map[sname])
            db.session.add(career)
        db.session.commit()

        click.echo("Seeding roadmaps…")
        for slug, rdata in ROADMAPS_DATA.items():
            career = Career.query.filter_by(slug=slug).first()
            if not career or Roadmap.query.filter_by(career_id=career.id).first():
                continue
            stages_data = rdata.pop("stages", [])
            roadmap = Roadmap(career_id=career.id, **rdata)
            db.session.add(roadmap)
            db.session.flush()
            for st in stages_data:
                stage = RoadmapStage(roadmap_id=roadmap.id, **st)
                db.session.add(stage)
        db.session.commit()

        click.echo("Seeding projects…")
        for p in PROJECTS_DATA:
            slug = p.pop("career_slug")
            career = Career.query.filter_by(slug=slug).first()
            if not career:
                continue
            project = Project(career_id=career.id, **p)
            db.session.add(project)
        db.session.commit()

        click.echo("✅ Database seeded successfully.")

    @app.cli.command("create-tables")
    @with_appcontext
    def create_tables():
        """Create all database tables (for simple deployments without migrations)."""
        db.create_all()
        click.echo("✅ Tables created.")


def _register_error_handlers(app):
    from flask import render_template

    @app.errorhandler(400)
    def bad_request(e):
        return render_template("errors/400.html"), 400

    @app.errorhandler(403)
    def forbidden(e):
        return render_template("errors/403.html"), 403

    @app.errorhandler(404)
    def not_found(e):
        return render_template("errors/404.html"), 404

    @app.errorhandler(429)
    def too_many_requests(e):
        return render_template("errors/429.html"), 429

    @app.errorhandler(500)
    def server_error(e):
        app.logger.error("500 error: %s", e)
        return render_template("errors/500.html"), 500

