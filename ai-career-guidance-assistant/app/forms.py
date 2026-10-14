from flask_wtf import FlaskForm
from wtforms import (
    StringField, PasswordField, EmailField, TextAreaField,
    SelectField, SelectMultipleField, BooleanField, SubmitField,
    URLField, DateField, widgets
)
from wtforms.validators import (
    DataRequired, Email, Length, EqualTo, Optional, URL, ValidationError
)
from app.models import User


# ── Auth forms ────────────────────────────────────────────────────────────────

class RegistrationForm(FlaskForm):
    username = StringField("Username", validators=[DataRequired(), Length(3, 80)])
    email = EmailField("Email", validators=[DataRequired(), Email(), Length(max=150)])
    password = PasswordField("Password", validators=[DataRequired(), Length(8, 128)])
    confirm_password = PasswordField(
        "Confirm Password", validators=[DataRequired(), EqualTo("password", message="Passwords must match.")]
    )
    submit = SubmitField("Create Account")

    def validate_email(self, field):
        if User.query.filter_by(email=field.data.lower()).first():
            raise ValidationError("An account with this email already exists.")

    def validate_username(self, field):
        if User.query.filter_by(username=field.data).first():
            raise ValidationError("This username is already taken.")


class LoginForm(FlaskForm):
    email = EmailField("Email", validators=[DataRequired(), Email()])
    password = PasswordField("Password", validators=[DataRequired()])
    remember = BooleanField("Remember me")
    submit = SubmitField("Log In")


# ── Profile form ──────────────────────────────────────────────────────────────

EDUCATION_CHOICES = [
    ("", "Select…"),
    ("high_school", "High School"),
    ("diploma", "Diploma / Associate"),
    ("bachelor", "Bachelor's Degree"),
    ("master", "Master's Degree"),
    ("phd", "PhD / Doctorate"),
    ("self_taught", "Self-Taught"),
    ("other", "Other"),
]


class ProfileForm(FlaskForm):
    full_name = StringField("Full Name", validators=[Optional(), Length(max=150)])
    bio = TextAreaField("Short Bio", validators=[Optional(), Length(max=500)])
    education_level = SelectField("Education Level", choices=EDUCATION_CHOICES, validators=[Optional()])
    field_of_study = StringField("Field of Study", validators=[Optional(), Length(max=150)])
    location = StringField("Location", validators=[Optional(), Length(max=150)])
    linkedin_url = URLField("LinkedIn URL", validators=[Optional(), URL()])
    github_url = URLField("GitHub URL", validators=[Optional(), URL()])
    career_goal = StringField("Career Goal", validators=[Optional(), Length(max=255)])
    submit = SubmitField("Save Profile")


# ── Assessment form ───────────────────────────────────────────────────────────

INTEREST_CHOICES = [
    ("programming", "Programming & Coding"),
    ("data", "Data & Analytics"),
    ("design", "Design & Creativity"),
    ("business", "Business & Management"),
    ("security", "Cybersecurity"),
    ("ai_ml", "Artificial Intelligence / ML"),
    ("cloud", "Cloud & DevOps"),
    ("writing", "Writing & Communication"),
    ("teaching", "Teaching & Mentoring"),
    ("problem_solving", "Problem Solving"),
]

WORKING_STYLE_CHOICES = [
    ("", "Select…"),
    ("remote", "Fully Remote"),
    ("hybrid", "Hybrid"),
    ("onsite", "On-site / Office"),
    ("freelance", "Freelance / Independent"),
    ("startup", "Start-up Environment"),
    ("corporate", "Large Corporate"),
    ("any", "No Preference"),
]


class MultiCheckboxField(SelectMultipleField):
    widget = widgets.ListWidget(prefix_label=False)
    option_widget = widgets.CheckboxInput()


class AssessmentForm(FlaskForm):
    education_level = SelectField(
        "Education Level", choices=EDUCATION_CHOICES, validators=[DataRequired(message="Please select your education level.")]
    )
    field_of_study = StringField("Field of Study / Major", validators=[Optional(), Length(max=150)])
    interests = MultiCheckboxField("Your Interests (pick all that apply)", choices=INTEREST_CHOICES)
    favourite_subjects = StringField(
        "Favourite Subjects (comma-separated)", validators=[Optional(), Length(max=300)]
    )
    technical_skills = TextAreaField(
        "Technical Skills you already have (comma-separated, or 'none')",
        validators=[Optional(), Length(max=500)]
    )
    soft_skills = TextAreaField(
        "Soft Skills (e.g. teamwork, communication)",
        validators=[Optional(), Length(max=500)]
    )
    preferred_activities = MultiCheckboxField(
        "Preferred Activities",
        choices=[
            ("coding", "Writing code"),
            ("analysing", "Analysing data"),
            ("designing", "Designing visuals"),
            ("communicating", "Communicating / presenting"),
            ("researching", "Researching / reading"),
            ("building", "Building / making things"),
            ("helping", "Helping others"),
            ("strategising", "Strategising / planning"),
        ]
    )
    career_goals = TextAreaField(
        "Describe your career goals (optional)",
        validators=[Optional(), Length(max=600)]
    )
    working_style = SelectField("Preferred Working Style", choices=WORKING_STYLE_CHOICES, validators=[Optional()])
    submit = SubmitField("Get Career Recommendations")


# ── Skill analysis ────────────────────────────────────────────────────────────

class SkillAnalysisForm(FlaskForm):
    career_id = SelectField("Target Career", coerce=int, validators=[DataRequired()])
    submit = SubmitField("Analyse Skill Gap")


# ── Resume form ───────────────────────────────────────────────────────────────

class ResumeDraftForm(FlaskForm):
    title = StringField("Resume Title", validators=[DataRequired(), Length(max=200)])
    target_career = StringField("Target Career / Role", validators=[Optional(), Length(max=150)])
    objective = TextAreaField("Career Objective / Summary", validators=[Optional(), Length(max=600)])
    education = TextAreaField("Education", validators=[Optional()])
    experience = TextAreaField("Work / Internship Experience", validators=[Optional()])
    skills_text = TextAreaField("Skills", validators=[Optional()])
    projects_text = TextAreaField("Projects", validators=[Optional()])
    certifications = TextAreaField("Certifications & Courses", validators=[Optional()])
    submit = SubmitField("Save Resume Draft")


# ── Job application tracker ───────────────────────────────────────────────────

class JobApplicationForm(FlaskForm):
    company = StringField("Company Name", validators=[DataRequired(), Length(max=150)])
    role = StringField("Role / Position", validators=[DataRequired(), Length(max=150)])
    status = SelectField(
        "Status",
        choices=[
            ("Applied", "Applied"),
            ("Assessment", "Assessment / Test"),
            ("Interview", "Interview"),
            ("Offer", "Offer Received"),
            ("Rejected", "Rejected"),
            ("Withdrawn", "Withdrawn"),
        ],
        default="Applied",
    )
    applied_date = DateField("Application Date", validators=[Optional()])
    url = URLField("Job Posting URL", validators=[Optional(), URL()])
    notes = TextAreaField("Notes", validators=[Optional(), Length(max=1000)])
    submit = SubmitField("Save Application")


# ── Contact form ──────────────────────────────────────────────────────────────

class ContactForm(FlaskForm):
    name = StringField("Your Name", validators=[DataRequired(), Length(max=100)])
    email = EmailField("Email Address", validators=[DataRequired(), Email()])
    subject = StringField("Subject", validators=[DataRequired(), Length(max=200)])
    message = TextAreaField("Message", validators=[DataRequired(), Length(min=20, max=2000)])
    submit = SubmitField("Send Message")
