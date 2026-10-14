"""
Jinja2 template filters and context processors registered on the app.
Called from app/__init__.py after blueprint registration.
"""
import json as _json


def register_filters(app):
    @app.template_filter("from_json")
    def from_json_filter(value):
        if not value:
            return []
        try:
            return _json.loads(value)
        except (ValueError, TypeError):
            return []

    @app.template_global("enumerate")
    def jinja_enumerate(iterable, start=0):
        return enumerate(iterable, start=start)
