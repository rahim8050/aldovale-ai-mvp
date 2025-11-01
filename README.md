# Aldovale — MVP: Smart Support Bot (Django + DRF scaffold)

This repository is a **public template** scaffold for the Aldovale MVP: a secure, production-minded Django + DRF project
that implements Week‑1 endpoints (auth token exchange, chat session creation, chat message endpoint), pre-commit hooks,
Docker, and GitHub Actions. The CI contains a placeholder for a `RAILWAY_TOKEN` secret — add it in your repo Settings -> Secrets.

## Quick start (local)

1. Copy `.env.example` to `.env` and fill values.
2. Build & run with docker-compose:
   ```bash
   docker compose build
   docker compose up -d
   docker compose exec web python manage.py migrate
   docker compose exec web python manage.py createsuperuser
   ```
3. Run tests:
   ```bash
   docker compose exec web pytest -q
   ```

## Deployment
- CI will run lint, tests, build docker image, and attempt to deploy to Railway when `main` receives a merge.
- Add `RAILWAY_TOKEN` and `RAILWAY_PROJECT_ID` to GitHub Secrets to enable automatic deploys.

---
