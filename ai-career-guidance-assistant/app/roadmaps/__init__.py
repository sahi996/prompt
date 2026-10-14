from flask import Blueprint

bp = Blueprint("roadmaps", __name__)

from app.roadmaps import routes  # noqa: F401, E402
