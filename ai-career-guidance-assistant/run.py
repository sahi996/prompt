"""
Application entry point.
Usage (development):  python run.py
Usage (production):   gunicorn "app:create_app()"
"""
import os
from app import create_app

app = create_app()

if __name__ == "__main__":
    debug = os.environ.get("FLASK_ENV", "development") == "development"
    app.run(debug=debug, host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
