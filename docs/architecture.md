
---

### 🧩 `architecture.md`
```markdown
# System Architecture

The Aldovale AI MVP follows a clean, layered architecture focused on scalability and maintainability.

## Layers
1. **Presentation Layer** — API endpoints (Django REST Framework)
2. **Domain Layer** — Business logic, serializers, validators
3. **Data Layer** — ORM-based models with secure query patterns

## Key Components
- **Django REST Framework (DRF)** for API design
- **PostgreSQL** as primary database
- **Redis** for caching and async task queuing
- **Celery** for background tasks
- **Docker + Compose** for containerized deployment

## Security
- ORM-safe queries only
- HTTPS enforced
- Environment-based secrets
- Rate limiting and CORS policies applied
