from flask import Blueprint

bp = Blueprint("assessments", __name__)

from app.assessments import routes  # noqa: F401, E402
