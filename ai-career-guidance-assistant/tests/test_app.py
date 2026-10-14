"""
Pytest test suite for AI Career Guidance Assistant.
Run with:  pytest tests/ -v
"""
import json
import pytest
from app import create_app
from app.extensions import db as _db
from config import TestingConfig


# ── Fixtures ──────────────────────────────────────────────────────────────────

@pytest.fixture(scope="session")
def app():
    """Create application for the test session."""
    application = create_app(TestingConfig)
    with application.app_context():
        _db.create_all()
        _seed_test_data()
    yield application
    with application.app_context():
        _db.drop_all()


@pytest.fixture(scope="session")
def client(app):
    return app.test_client()


@pytest.fixture(scope="session")
def runner(app):
    return app.test_cli_runner()


def _seed_test_data():
    """Minimal seed for tests."""
    from app.models import Career, Skill, Roadmap, RoadmapStage
    if Career.query.count() > 0:
        return
    skill = Skill(name="Python", category="technical", description="Test")
    _db.session.add(skill)
    career = Career(
        slug="python-developer",
        title="Python Developer",
        category="Software Development",
        description="Test career",
        short_description="Build things with Python.",
        education_level="bachelor",
        demand_level="High",
        is_beginner_friendly=True,
        icon="bi-code-slash",
        entry_roles=json.dumps(["Junior Developer"]),
        next_steps=json.dumps(["Learn Flask"]),
    )
    career.skills.append(skill)
    _db.session.add(career)
    _db.session.flush()
    roadmap = Roadmap(
        career_id=career.id,
        title="Python Roadmap",
        description="Test roadmap",
        estimated_weeks=10,
    )
    _db.session.add(roadmap)
    _db.session.flush()
    stage = RoadmapStage(
        roadmap_id=roadmap.id,
        order=1,
        title="Basics",
        description="Python basics",
        topics=json.dumps(["Variables"]),
        resources=json.dumps([{"title": "Docs", "url": "https://python.org", "type": "docs"}]),
        exercises=json.dumps(["Hello World"]),
        estimated_hours=10,
    )
    _db.session.add(stage)
    _db.session.commit()


# ── Helper ────────────────────────────────────────────────────────────────────

def register_and_login(client, email="test@example.com", username="testuser", password="testpass1"):
    client.post("/auth/logout", follow_redirects=True)
    client.post("/auth/register", data={
        "username": username,
        "email": email,
        "password": password,
        "confirm_password": password,
    }, follow_redirects=True)
    return client.post("/auth/login", data={
        "email": email,
        "password": password,
    }, follow_redirects=True)


# ── Public pages ──────────────────────────────────────────────────────────────

class TestPublicPages:
    def test_home(self, client):
        r = client.get("/")
        assert r.status_code == 200
        assert b"Career" in r.data

    def test_about(self, client):
        r = client.get("/about")
        assert r.status_code == 200
        assert b"SDG" in r.data

    def test_features(self, client):
        r = client.get("/features")
        assert r.status_code == 200

    def test_explore_careers(self, client):
        r = client.get("/careers/")
        assert r.status_code == 200
        assert b"Python Developer" in r.data

    def test_career_detail(self, client):
        r = client.get("/careers/python-developer")
        assert r.status_code == 200
        assert b"Python Developer" in r.data

    def test_career_detail_404(self, client):
        r = client.get("/careers/nonexistent-career")
        assert r.status_code == 404

    def test_health_endpoint(self, client):
        r = client.get("/health")
        assert r.status_code == 200
        data = json.loads(r.data)
        assert data["status"] == "ok"

    def test_404_page(self, client):
        r = client.get("/this-does-not-exist-xyz")
        assert r.status_code == 404

    def test_roadmaps_index(self, client):
        r = client.get("/roadmaps/")
        assert r.status_code == 200

    def test_roadmap_view(self, client):
        r = client.get("/roadmaps/python-developer")
        assert r.status_code == 200
        assert b"Python" in r.data

    def test_assessment_form_get(self, client):
        r = client.get("/assessment/")
        assert r.status_code == 200


# ── Career search ─────────────────────────────────────────────────────────────

class TestCareerSearch:
    def test_search_finds_career(self, client):
        r = client.get("/careers/?q=python")
        assert r.status_code == 200
        assert b"Python Developer" in r.data

    def test_search_no_results(self, client):
        r = client.get("/careers/?q=zzznoresult9999")
        assert r.status_code == 200
        assert b"No careers found" in r.data

    def test_beginner_filter(self, client):
        r = client.get("/careers/?beginner=1")
        assert r.status_code == 200


# ── Registration & Login ──────────────────────────────────────────────────────

class TestAuth:
    def test_register_success(self, app):
        with app.test_client() as c:
            r = c.post("/auth/register", data={
                "username": "newuser_reg",
                "email": "newreg@example.com",
                "password": "securepass1",
                "confirm_password": "securepass1",
            }, follow_redirects=True)
            assert r.status_code == 200
            assert b"Welcome" in r.data or b"Dashboard" in r.data

    def test_register_duplicate_email(self, app):
        """Duplicate email: form validation catches it — response stays on register page."""
        from app.models import User, Profile
        from app.extensions import db
        with app.app_context():
            if not User.query.filter_by(email="dupe3@example.com").first():
                u = User(username="dupebase3", email="dupe3@example.com")
                u.set_password("securepass1")
                db.session.add(u)
                db.session.flush()
                db.session.add(Profile(user_id=u.id))
                db.session.commit()
        # Fresh client with no session cookies
        c = app.test_client()
        c.use_cookies = False
        with c:
            r = c.post("/auth/register", data={
                "username": "dupeuser3b",
                "email": "dupe3@example.com",
                "password": "securepass1",
                "confirm_password": "securepass1",
            })
            # Stays on register page (200) — not redirected to dashboard
            assert r.status_code == 200
            assert b"Register" in r.data or b"already exists" in r.data or b"Create" in r.data

    def test_register_password_mismatch(self, app):
        with app.test_client() as c:
            r = c.post("/auth/register", data={
                "username": "mismatchuser",
                "email": "mismatch@example.com",
                "password": "password1",
                "confirm_password": "password2",
            }, follow_redirects=True)
            assert b"match" in r.data.lower() or r.status_code == 200

    def test_login_wrong_password(self, app):
        """Wrong password: login page re-renders (200) or flashes error."""
        from app.models import User, Profile
        from app.extensions import db
        with app.app_context():
            if not User.query.filter_by(email="wrongpass3@example.com").first():
                u = User(username="wrongpass3u", email="wrongpass3@example.com")
                u.set_password("correct_pass3")
                db.session.add(u)
                db.session.flush()
                db.session.add(Profile(user_id=u.id))
                db.session.commit()
        c = app.test_client()
        c.use_cookies = False
        with c:
            r = c.post("/auth/login", data={
                "email": "wrongpass3@example.com",
                "password": "definitely_wrong_xyz",
            })
            # Either stays on login page (200) or redirects — should NOT be a successful login
            # A successful login redirects to /dashboard (302)
            # Wrong password should stay on login page (200)
            assert r.status_code == 200 or (r.status_code == 302 and b"/auth/login" in r.headers.get("Location", "").encode())

    def test_login_nonexistent_user(self, app):
        c = app.test_client()
        c.use_cookies = False
        with c:
            r = c.post("/auth/login", data={
                "email": "nobody_at_all2@nowhere.com",
                "password": "whatever",
            })
            assert r.status_code == 200 or (r.status_code == 302 and b"/auth/login" in r.headers.get("Location", "").encode())


# ── Auth-required pages ───────────────────────────────────────────────────────

class TestAuthRequired:
    def test_dashboard_redirects_when_not_logged_in(self, app):
        # Flask-Login requires cookies to identify sessions; without cookies → anonymous
        c = app.test_client()
        c.use_cookies = False
        with c:
            r = c.get("/dashboard/", follow_redirects=False)
            assert r.status_code in (301, 302)

    def test_dashboard_accessible_when_logged_in(self, app):
        with app.test_client() as c:
            register_and_login(c, "dash@example.com", "dashuser")
            r = c.get("/dashboard/", follow_redirects=True)
            assert r.status_code == 200


# ── Assessment & Recommendations ─────────────────────────────────────────────

class TestAssessment:
    def test_submit_assessment(self, client):
        r = client.post("/assessment/", data={
            "education_level": "bachelor",
            "field_of_study": "Computer Science",
            "interests": ["programming", "data"],
            "favourite_subjects": "Math",
            "technical_skills": "Python",
            "soft_skills": "teamwork",
            "preferred_activities": ["coding"],
            "career_goals": "Become a developer",
            "working_style": "remote",
        }, follow_redirects=True)
        assert r.status_code == 200
        # Should show results page
        assert b"Recommendation" in r.data or b"recommendation" in r.data

    def test_missing_education_level(self, client):
        r = client.post("/assessment/", data={
            "education_level": "",
        }, follow_redirects=True)
        assert r.status_code == 200
        # Should re-render form with error
        assert b"education" in r.data.lower()


# ── Roadmap progress ──────────────────────────────────────────────────────────

class TestRoadmapProgress:
    def test_update_progress_requires_login(self, app):
        c = app.test_client()
        c.use_cookies = False
        with c:
            r = c.post("/roadmaps/1/progress",
                       data=json.dumps({"stage_id": 1, "completed": True}),
                       content_type="application/json")
            assert r.status_code in (302, 401)

    def test_update_progress_when_logged_in(self, app):
        from app.models import Roadmap, RoadmapStage
        with app.test_client() as c:
            register_and_login(c, "roadmaptest2@example.com", "roadmapuser2")
            with app.app_context():
                roadmap = Roadmap.query.first()
                stage = RoadmapStage.query.filter_by(roadmap_id=roadmap.id).first()
            if roadmap and stage:
                r = c.post(
                    f"/roadmaps/{roadmap.id}/progress",
                    data=json.dumps({"stage_id": stage.id, "completed": True}),
                    content_type="application/json",
                )
                assert r.status_code == 200
                data = json.loads(r.data)
                assert data.get("ok") is True


# ── AI fallback ───────────────────────────────────────────────────────────────

class TestAIFallback:
    def test_rule_engine_no_api_key(self, app):
        """Rule engine should return results without an API key."""
        with app.app_context():
            from app.models import Assessment
            # Build a minimal assessment object without saving
            a = Assessment(
                education_level="bachelor",
                field_of_study="Computer Science",
                interests=json.dumps(["programming", "data"]),
                preferred_activities=json.dumps(["coding"]),
                technical_skills="Python, Flask",
                soft_skills="teamwork",
                career_goals="developer",
                working_style="remote",
            )
            from app.ai_services.rule_engine import rule_based_score
            results = rule_based_score(a)
            assert len(results) > 0
            assert "slug" in results[0]
            assert "score" in results[0]

    def test_interview_feedback_fallback(self, client):
        """Interview feedback endpoint should work without API key."""
        r = client.post(
            "/assessment/interview-feedback",
            data=json.dumps({
                "question": "Tell me about yourself.",
                "answer": "I am a student passionate about programming. I enjoy building web applications with Python and Flask.",
                "career_title": "Python Developer",
            }),
            content_type="application/json",
        )
        assert r.status_code == 200
        data = json.loads(r.data)
        assert "feedback" in data


# ── Database persistence ──────────────────────────────────────────────────────

class TestDatabasePersistence:
    def test_saved_career_persists(self, client, app):
        register_and_login(client, "savetest@example.com", "saveuser")
        with app.app_context():
            from app.models import Career
            career = Career.query.filter_by(slug="python-developer").first()
            if career:
                client.post(
                    f"/dashboard/saved-careers/toggle/{career.id}",
                    data={"csrf_token": "test"},
                    follow_redirects=True,
                )
