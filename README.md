# Plotly Dash app template

Starter template for a **Plotly Dash** web app with authentication, user profile, and session management. Use it as a base to build dashboards and data apps without wiring auth and DB from scratch.

**Goals:**

- Ready-made auth (login, registration, sessions)
- Profile page with session management (view/terminate sessions)
- Clear split: Flask backend + Dash frontend (Mantine UI)
- Runs locally or in Docker

## Run locally

You need a PostgreSQL instance: local install, cloud (e.g. managed DB), or run only the database in Docker (`docker compose up db -d`). The app runs on your machine; only the DB can be in Docker or elsewhere.

1. **Requirements:** Python 3.14+, [uv](https://docs.astral.sh/uv/).

2. **Install deps and create `.env`:**

   ```bash
   uv sync
   ```

   Create a `.env` file in the project root (see variables below).

3. **Set in `.env`:**

   ```env
   POSTGRES_HOST=localhost
   POSTGRES_PORT=5432
   POSTGRES_USER=your_user
   POSTGRES_PASSWORD=your_password
   POSTGRES_DB=dash
   SECRET_KEY=your_secret_key
   ```

4. **Apply migrations and start:**

   ```bash
   uv run alembic upgrade head
   uv run main.py
   ```

   App: <http://localhost:8080>

## Run with Docker

When you run the full stack with Docker Compose, the **database starts automatically** (no separate Postgres setup).

```bash
# Create .env with POSTGRES_* and SECRET_KEY (see above)
docker compose up --build
```

App: <http://localhost:8080> · DB port: 6432 (mapped from 5432).
