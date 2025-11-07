# Aldovale_AI — MVP: Smart Support Bot (Django + DRF + LLM Integration)

Aldovale_AI is a **secure, production-ready Django REST API** for an intelligent support assistant.
It handles authenticated chat sessions, contextual memory, structured logging, and LLM-powered message replies.

---

## 🚀 Features
- Token-based Authentication (JWT or DRF tokens)
- Chat session creation and message endpoints
- External LLM (OpenAI/Anthropic/local) integration
- Short-term chat memory per session
- CI/CD pipeline with email notifications
- Structured logging with `structlog`
- Dockerized environment
- Automated tests, linting, and type checking
- OpenAPI schema via `drf-spectacular`

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

1. Copy `.env.example` to `.env` and fill values:
   ```bash
   cp .env.example .env
Build & run:

bash
Copy code
docker compose build
docker compose up -d
docker compose exec web python manage.py migrate
docker compose exec web python manage.py createsuperuser
Run tests:

bash
Copy code
docker compose exec web pytest -q
Generate API schema:

bash
Copy code
docker compose exec web python manage.py spectacular --file schema.yaml
🧪 CI/CD
Lint, type, and test steps run automatically on each push to main.

On success/failure, an email notification is sent to the configured recipients.

Add the following GitHub Secrets:

nginx
Copy code
SMTP_HOST
SMTP_PORT
SMTP_USERNAME
SMTP_PASSWORD
TO_EMAIL
FROM_EMAIL
Example snippet in .github/workflows/ci.yml:

yaml
Copy code
- name: Notify via Email
  uses: dawidd6/action-send-mail@v4
  if: always()
  with:
    server_address: ${{ secrets.SMTP_HOST }}
    server_port: ${{ secrets.SMTP_PORT }}
    username: ${{ secrets.SMTP_USERNAME }}
    password: ${{ secrets.SMTP_PASSWORD }}
    to: ${{ secrets.TO_EMAIL }}
    from: Aldovale CI <${{ secrets.FROM_EMAIL }}>
    subject: "CI Notification - ${{ github.repository }}"
    body: "Build status: ${{ job.status }}"
🧠 API Overview
Endpoint	Method	Description
/api/v1/auth/token/	POST	Obtain or refresh token
/api/v1/sessions/	POST	Create a new chat session
/api/v1/messages/	POST	Send a user message, receive LLM reply
/api/v1/health/	GET	Health check
/api/v1/version/	GET	API version info

🧩 Development Workflow
bash
Copy code
make lint     # Ruff + Black + MyPy + Bandit
make test     # Run pytest
make run      # Run dev server
make format   # Auto-format code
🧍‍♂️ Authors
Aldovale_AI Team — Building production-grade, secure AI backends with discipline and clarity.

