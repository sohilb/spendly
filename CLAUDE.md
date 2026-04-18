# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Commands

```bash
# Install dependencies
uv sync

# Run the dev server (port 5001)
uv run python app.py

# Run tests
uv run pytest

# Run a single test file
uv run pytest tests/test_db.py

# Run a single test
uv run pytest tests/test_db.py::test_get_db
```

## Architecture

This is **Spendly**, a Flask + SQLite expense-tracking web app structured as a step-by-step student project. Each numbered step adds a feature; stubs for future steps are already present in `app.py` and `database/db.py`.

**Entry point:** `app.py` — defines the Flask app and all routes. Run directly (`python app.py`) or via `uv run`.

**Database layer:** `database/db.py` — students implement three functions here:
- `get_db()` — returns a SQLite connection with `row_factory = sqlite3.Row` and `PRAGMA foreign_keys = ON`
- `init_db()` — creates tables using `CREATE TABLE IF NOT EXISTS`
- `seed_db()` — inserts sample data for development

**Templating:** Jinja2 templates in `templates/`. All pages extend `base.html`, which provides the navbar, footer, and links to `static/css/style.css` and `static/js/main.js`.

**Step roadmap** (reflected in placeholder routes in `app.py`):
1. Database setup (`database/db.py`)
2. Auth — register / login
3. Auth — logout / sessions
4. Profile page
5–6. Expense listing / dashboard
7. Add expense
8. Edit expense
9. Delete expense

## Key conventions

- SQLite database file will live in `database/` once `init_db()` is implemented.
- `werkzeug.security` is the intended library for password hashing (already a dependency).
- Placeholder routes return plain strings; replace them with `render_template(...)` calls as each step is completed.
