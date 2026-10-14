# AI Career Guidance Assistant

> **Discover Your Strengths. Explore Your Career. Build Your Future.**

A full-stack web application aligned with **UN SDG 8 — Decent Work and Economic Growth**.
Built with Python, Flask, Bootstrap 5, and SQLAlchemy.

[![Python](https://img.shields.io/badge/Python-3.10%2B-blue)](https://python.org)
[![Flask](https://img.shields.io/badge/Flask-3.0-green)](https://flask.palletsprojects.com)
[![License](https://img.shields.io/badge/License-MIT-violet)](LICENSE)

---

## Features

| Feature | Description |
|---|---|
| 🤖 AI Career Assessment | Personalised career recommendations (AI API optional) |
| 🧭 Career Explorer | Searchable directory of 10+ career paths |
| 📊 Skill Gap Analysis | Compare your skills against career requirements |
| 🗺️ Learning Roadmaps | Stage-by-stage paths with free resources |
| 📁 Project Ideas | Beginner → Advanced portfolio project briefs |
| 📄 Resume & Interview | Resume drafts, interview practice, job tracker |
| 🔒 Auth & Dashboard | Registration, login, progress tracking |

---

## Quick Start (Local Development)

### 1. Clone and set up

```bash
git clone https://github.com/YOUR_USERNAME/ai-career-guidance-assistant.git
cd ai-career-guidance-assistant
python -m venv venv
# Windows:
venv\Scripts\activate
# macOS/Linux:
source venv/bin/activate
pip install -r requirements.txt
pip install -r requirements-dev.txt
```

### 2. Configure environment

```bash
cp .env.example .env
# Edit .env — at minimum set SECRET_KEY
```

### 3. Create tables and seed database

```bash
flask --app run create-tables
flask --app run seed-db
```

### 4. Run the development server

```bash
python run.py
# Open http://localhost:5000
```

---

## Running Tests

```bash
pytest tests/ -v
```

---

## Deploying to Render (Free HTTPS)

### Prerequisites
- GitHub account
- [Render](https://render.com) free account

### Step 1: Push to GitHub

```bash
git init
git add .
git commit -m "Initial commit"
git remote add origin https://github.com/YOUR_USERNAME/ai-career-guidance-assistant.git
git push -u origin main
```

### Step 2: Create a PostgreSQL database on Render

1. Log in to [render.com](https://render.com)
2. Click **New → PostgreSQL**
3. Choose a name (e.g. `career-db`) and the Free plan
4. Copy the **Internal Database URL**

### Step 3: Create a Web Service on Render

1. Click **New → Web Service**
2. Connect your GitHub repository
3. Configure:
   - **Runtime:** Python 3
   - **Build Command:** `pip install -r requirements.txt`
   - **Start Command:** `gunicorn "app:create_app()"`
4. Add Environment Variables:

| Variable | Value |
|---|---|
| `SECRET_KEY` | A long random string (see below) |
| `DATABASE_URL` | Paste the Internal Database URL from Step 2 |
| `FLASK_ENV` | `production` |
| `OPENAI_API_KEY` | Your OpenAI key (optional) |

Generate a secret key:
```bash
python -c "import secrets; print(secrets.token_hex(32))"
```

5. Click **Create Web Service**

### Step 4: Run database migrations on Render

In the Render dashboard, open the **Shell** tab and run:

```bash
flask create-tables
flask seed-db
```

Or use Flask-Migrate:
```bash
flask db upgrade
flask seed-db
```

### Step 5: Verify

Visit your Render URL (e.g. `https://ai-career-guidance-assistant.onrender.com`).
HTTPS is managed automatically by Render.

Check the health endpoint: `https://your-app.onrender.com/health`
Expected: `{"status": "ok", "db": true}`

---

## Environment Variables Reference

| Variable | Required | Description |
|---|---|---|
| `SECRET_KEY` | ✅ | Flask session secret (random 32+ chars) |
| `DATABASE_URL` | ✅ (prod) | PostgreSQL connection string |
| `FLASK_ENV` | ✅ | `development` or `production` |
| `OPENAI_API_KEY` | ❌ | Enables AI explanations (optional) |
| `OPENAI_MODEL` | ❌ | Model name (default: gpt-3.5-turbo) |
| `REDIS_URL` | ❌ | Persistent rate-limit storage |

---

## Project Structure

```
ai-career-guidance-assistant/
├── app/
│   ├── __init__.py          # App factory
│   ├── extensions.py        # db, login_manager, csrf, limiter, bcrypt
│   ├── models.py            # All SQLAlchemy models
│   ├── forms.py             # All WTForms
│   ├── template_filters.py  # Jinja2 custom filters
│   ├── seed_data.py         # Career/skill seed data
│   ├── main/                # Public routes
│   ├── auth/                # Registration & login
│   ├── careers/             # Career explorer
│   ├── assessments/         # Assessment form & recommendations
│   ├── roadmaps/            # Learning roadmaps
│   ├── dashboard/           # User dashboard
│   ├── ai_services/         # AI service + rule engine
│   ├── templates/           # Jinja2 templates
│   └── static/              # CSS & JS
├── tests/                   # Pytest test suite
├── config.py                # Configuration classes
├── run.py                   # Development entry point
├── requirements.txt         # Production dependencies
├── requirements-dev.txt     # Test dependencies
└── .env.example             # Environment variables template
```

---

## Security

- Passwords hashed with bcrypt
- CSRF protection on all forms
- Server-side authentication checks
- Secure session cookies in production
- Rate limiting on auth and AI endpoints
- AI API key never exposed to the browser
- Environment-based secrets (never committed)

---

## SDG 8 Alignment

This project contributes to **UN Sustainable Development Goal 8: Decent Work and Economic Growth** by:

- Providing free career guidance to students and graduates worldwide
- Reducing the career information gap for young people without access to professional counsellors
- Supporting skill development and employment readiness

---

## Disclaimer

Career recommendations are for informational purposes only. They do not guarantee employment,
represent a scientifically validated assessment, or constitute professional career advice.
Always verify requirements with real job postings and professional advisors.

---

## License

MIT — see [LICENSE](LICENSE) for details.
