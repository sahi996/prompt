from flask import Blueprint

bp = Blueprint("careers", __name__)

from app.careers import routes  # noqa: F401, E402
