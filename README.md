# Aldovale_AI — MVP: Smart Support Bot (Django + DRF + LLM Integration)

Aldovale_AI is a secure, production-ready Django REST API for an intelligent support assistant. It supports authenticated chat sessions, contextual memory, structured logging, and LLM-powered message replies.

---

## 🚀 Features

- Token-based Authentication (JWT or DRF tokens)  
- Chat session creation and message endpoints  
- External LLM integration (OpenAI, Anthropic, local models)  
- Short-term chat memory per session  
- CI/CD pipeline with email notifications  
- Structured logging with `structlog`  
- Dockerized environment  
- Automated tests, linting, and type checking  
- OpenAPI schema generated via `drf-spectacular`  

---

## 🧰 Tech Stack

- **Backend:** Django + Django REST Framework  
- **LLM Client:** Pluggable (OpenAI, Anthropic, etc.)  
- **Database:** PostgreSQL  
- **Containerization:** Docker + Docker Compose  
- **CI/CD:** GitHub Actions (lint → test → notify)  
- **Notifications:** Email via `dawidd6/action-send-mail@v4`  
- **Static Checks:** Ruff, Black, MyPy, Bandit  

---

## ⚙️ Quick Start (Local)

1. Copy `.env.example` to `.env` and fill in the environment variables:

   ```bash
   cp .env.example .env
2. Build and run containers:
   ```bash
   docker compose build
   docker compose up -d
3. Run migrations and create a superuser:
   ```bash
   docker compose exec web python manage.py migrate
   docker compose exec web python manage.py createsuperuser
4. Run tests:
   ```bash
   docker compose exec web pytest -q
5. Generate the OpenAPI schema:
   ```bash 
   docker compose exec web python manage.py spectacular --file schema.yaml
## 🧪 CI/CD
- Linting, type checking, and tests run automatically on each push to main.
-Email notifications are sent on build success or failure.  
# Add these GitHub Secrets:
SMTP_HOST  
SMTP_PORT  
SMTP_USERNAME  
SMTP_PASSWORD  
TO_EMAIL  
FROM_EMAIL
# Example snippet in .github/workflows/ci.yml:
name: Notify via Email

uses: dawidd6/action-send-mail@v4

if: always()

with:
  server_address: ${{ secrets.SMTP_HOST }}
  server_port: ${{ secrets.SMTP_PORT }}
  username: ${{ secrets.SMTP_USERNAME }}
  password: ${{ secrets.SMTP_PASSWORD }}
  to: ${{ secrets.TO_EMAIL }}
  from: AldovaleCI <${{ secrets.FROM_EMAIL }}>
  subject: "CI Notification - github.repository"
  body: "Build status: ${{ job.status }}"
# 🧠 API Overview
| Endpoint              | Method | Description                            |
| --------------------- | ------ | -------------------------------------- |
| `/api/v1/auth/token/` | POST   | Obtain or refresh authentication token |
| `/api/v1/sessions/`   | POST   | Create a new chat session              |
| `/api/v1/messages/`   | POST   | Send a user message, receive LLM reply |
| `/api/v1/health/`     | GET    | Health check                           |
| `/api/v1/version/`    | GET    | API version information                |
# 🧩 Development Workflow
- Use make commands to simplify development:
   ```bash
   make lint    # Run Ruff, Black, MyPy, Bandit
   make test    # Run pytest tests
   make run     # Start the development server
   make format  # Auto-format the code
# 🧍‍♂️ Authors
Aldovale_AI Team — Building production-grade, secure AI backends with discipline and clarity.   


   
