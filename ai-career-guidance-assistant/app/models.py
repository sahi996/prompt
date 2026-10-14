from datetime import datetime
from flask_login import UserMixin
from app.extensions import db, bcrypt


# ── Association tables ────────────────────────────────────────────────────────

career_skill = db.Table(
    "career_skill",
    db.Column("career_id", db.Integer, db.ForeignKey("career.id"), primary_key=True),
    db.Column("skill_id", db.Integer, db.ForeignKey("skill.id"), primary_key=True),
)

user_saved_career = db.Table(
    "user_saved_career",
    db.Column("user_id", db.Integer, db.ForeignKey("user.id"), primary_key=True),
    db.Column("career_id", db.Integer, db.ForeignKey("career.id"), primary_key=True),
)


# ── User ──────────────────────────────────────────────────────────────────────

class User(UserMixin, db.Model):
    __tablename__ = "user"

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(150), unique=True, nullable=False, index=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password_hash = db.Column(db.String(256), nullable=False)
    is_active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    last_login = db.Column(db.DateTime)

    # relationships
    profile = db.relationship("Profile", back_populates="user", uselist=False, cascade="all, delete-orphan")
    saved_careers = db.relationship("Career", secondary=user_saved_career, backref="saved_by_users")
    assessments = db.relationship("Assessment", back_populates="user", cascade="all, delete-orphan")
    roadmap_progresses = db.relationship("UserRoadmapProgress", back_populates="user", cascade="all, delete-orphan")
    skill_analyses = db.relationship("SkillAnalysis", back_populates="user", cascade="all, delete-orphan")
    resume_drafts = db.relationship("ResumeDraft", back_populates="user", cascade="all, delete-orphan")
    interview_sessions = db.relationship("InterviewSession", back_populates="user", cascade="all, delete-orphan")
    job_applications = db.relationship("JobApplication", back_populates="user", cascade="all, delete-orphan")

    def set_password(self, password):
        self.password_hash = bcrypt.generate_password_hash(password).decode("utf-8")

    def check_password(self, password):
        return bcrypt.check_password_hash(self.password_hash, password)

    def __repr__(self):
        return f"<User {self.username}>"


class Profile(db.Model):
    __tablename__ = "profile"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    full_name = db.Column(db.String(150))
    bio = db.Column(db.Text)
    education_level = db.Column(db.String(80))
    field_of_study = db.Column(db.String(150))
    location = db.Column(db.String(150))
    linkedin_url = db.Column(db.String(255))
    github_url = db.Column(db.String(255))
    career_goal = db.Column(db.String(255))
    avatar_url = db.Column(db.String(255))
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    user = db.relationship("User", back_populates="profile")


# ── Career ────────────────────────────────────────────────────────────────────

class Career(db.Model):
    __tablename__ = "career"

    id = db.Column(db.Integer, primary_key=True)
    slug = db.Column(db.String(100), unique=True, nullable=False, index=True)
    title = db.Column(db.String(150), nullable=False)
    category = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=False)
    short_description = db.Column(db.String(300))
    education_level = db.Column(db.String(80))
    avg_salary = db.Column(db.String(80))
    demand_level = db.Column(db.String(50))  # High / Medium / Low
    is_beginner_friendly = db.Column(db.Boolean, default=False)
    icon = db.Column(db.String(80))  # Bootstrap icon class
    entry_roles = db.Column(db.Text)   # JSON string list
    next_steps = db.Column(db.Text)    # JSON string list
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    skills = db.relationship("Skill", secondary=career_skill, backref="careers")
    roadmap = db.relationship("Roadmap", back_populates="career", uselist=False, cascade="all, delete-orphan")
    projects = db.relationship("Project", back_populates="career", cascade="all, delete-orphan")
    recommendations = db.relationship("Recommendation", back_populates="career", cascade="all, delete-orphan")

    def __repr__(self):
        return f"<Career {self.title}>"


class Skill(db.Model):
    __tablename__ = "skill"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True, nullable=False)
    category = db.Column(db.String(80))  # technical / soft
    description = db.Column(db.String(300))

    def __repr__(self):
        return f"<Skill {self.name}>"


# ── Assessment & Recommendations ──────────────────────────────────────────────

class Assessment(db.Model):
    __tablename__ = "assessment"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=True)
    education_level = db.Column(db.String(80))
    field_of_study = db.Column(db.String(150))
    interests = db.Column(db.Text)
    favourite_subjects = db.Column(db.Text)
    technical_skills = db.Column(db.Text)
    soft_skills = db.Column(db.Text)
    preferred_activities = db.Column(db.Text)
    career_goals = db.Column(db.Text)
    working_style = db.Column(db.String(80))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    user = db.relationship("User", back_populates="assessments")
    recommendations = db.relationship("Recommendation", back_populates="assessment", cascade="all, delete-orphan")


class Recommendation(db.Model):
    __tablename__ = "recommendation"

    id = db.Column(db.Integer, primary_key=True)
    assessment_id = db.Column(db.Integer, db.ForeignKey("assessment.id"), nullable=False)
    career_id = db.Column(db.Integer, db.ForeignKey("career.id"), nullable=False)
    score = db.Column(db.Float, default=0.0)
    match_reason = db.Column(db.Text)
    ai_explanation = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    assessment = db.relationship("Assessment", back_populates="recommendations")
    career = db.relationship("Career", back_populates="recommendations")


# ── Roadmaps ──────────────────────────────────────────────────────────────────

class Roadmap(db.Model):
    __tablename__ = "roadmap"

    id = db.Column(db.Integer, primary_key=True)
    career_id = db.Column(db.Integer, db.ForeignKey("career.id"), nullable=False)
    title = db.Column(db.String(200))
    description = db.Column(db.Text)
    estimated_weeks = db.Column(db.Integer)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    career = db.relationship("Career", back_populates="roadmap")
    stages = db.relationship("RoadmapStage", back_populates="roadmap", order_by="RoadmapStage.order", cascade="all, delete-orphan")
    user_progresses = db.relationship("UserRoadmapProgress", back_populates="roadmap", cascade="all, delete-orphan")


class RoadmapStage(db.Model):
    __tablename__ = "roadmap_stage"

    id = db.Column(db.Integer, primary_key=True)
    roadmap_id = db.Column(db.Integer, db.ForeignKey("roadmap.id"), nullable=False)
    order = db.Column(db.Integer, nullable=False)
    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text)
    topics = db.Column(db.Text)       # JSON list
    resources = db.Column(db.Text)    # JSON list of {title, url, type}
    exercises = db.Column(db.Text)    # JSON list
    estimated_hours = db.Column(db.Integer)

    roadmap = db.relationship("Roadmap", back_populates="stages")
    progress_entries = db.relationship("UserRoadmapProgress", back_populates="stage", cascade="all, delete-orphan")


class UserRoadmapProgress(db.Model):
    __tablename__ = "user_roadmap_progress"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    roadmap_id = db.Column(db.Integer, db.ForeignKey("roadmap.id"), nullable=False)
    stage_id = db.Column(db.Integer, db.ForeignKey("roadmap_stage.id"), nullable=False)
    completed = db.Column(db.Boolean, default=False)
    completed_at = db.Column(db.DateTime)
    notes = db.Column(db.Text)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    user = db.relationship("User", back_populates="roadmap_progresses")
    roadmap = db.relationship("Roadmap", back_populates="user_progresses")
    stage = db.relationship("RoadmapStage", back_populates="progress_entries")

    __table_args__ = (db.UniqueConstraint("user_id", "stage_id", name="uq_user_stage"),)


# ── Skill Analysis ────────────────────────────────────────────────────────────

class SkillAnalysis(db.Model):
    __tablename__ = "skill_analysis"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    career_id = db.Column(db.Integer, db.ForeignKey("career.id"), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    user = db.relationship("User", back_populates="skill_analyses")
    career = db.relationship("Career")
    items = db.relationship("SkillAnalysisItem", back_populates="analysis", cascade="all, delete-orphan")


class SkillAnalysisItem(db.Model):
    __tablename__ = "skill_analysis_item"

    id = db.Column(db.Integer, primary_key=True)
    analysis_id = db.Column(db.Integer, db.ForeignKey("skill_analysis.id"), nullable=False)
    skill_id = db.Column(db.Integer, db.ForeignKey("skill.id"), nullable=False)
    known = db.Column(db.Boolean, default=False)
    priority = db.Column(db.Integer, default=3)  # 1=high … 5=low

    analysis = db.relationship("SkillAnalysis", back_populates="items")
    skill = db.relationship("Skill")


# ── Projects ──────────────────────────────────────────────────────────────────

class Project(db.Model):
    __tablename__ = "project"

    id = db.Column(db.Integer, primary_key=True)
    career_id = db.Column(db.Integer, db.ForeignKey("career.id"), nullable=False)
    title = db.Column(db.String(200), nullable=False)
    problem_statement = db.Column(db.Text)
    difficulty = db.Column(db.String(50))  # Beginner / Intermediate / Advanced
    technologies = db.Column(db.Text)      # JSON list
    core_features = db.Column(db.Text)     # JSON list
    milestones = db.Column(db.Text)        # JSON list
    learning_outcomes = db.Column(db.Text) # JSON list
    advanced_features = db.Column(db.Text) # JSON list

    career = db.relationship("Career", back_populates="projects")


# ── Resume & Interview ────────────────────────────────────────────────────────

class ResumeDraft(db.Model):
    __tablename__ = "resume_draft"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    title = db.Column(db.String(200))
    content = db.Column(db.Text)  # JSON blob
    target_career = db.Column(db.String(150))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    user = db.relationship("User", back_populates="resume_drafts")


class InterviewSession(db.Model):
    __tablename__ = "interview_session"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    career_id = db.Column(db.Integer, db.ForeignKey("career.id"), nullable=True)
    questions_json = db.Column(db.Text)   # JSON list of {question, answer, feedback}
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    user = db.relationship("User", back_populates="interview_sessions")
    career = db.relationship("Career")


class JobApplication(db.Model):
    __tablename__ = "job_application"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    company = db.Column(db.String(150))
    role = db.Column(db.String(150))
    status = db.Column(db.String(80), default="Applied")  # Applied/Interview/Offer/Rejected
    applied_date = db.Column(db.Date)
    notes = db.Column(db.Text)
    url = db.Column(db.String(255))
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    user = db.relationship("User", back_populates="job_applications")
