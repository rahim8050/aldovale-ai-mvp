# API Documentation

The backend exposes RESTful endpoints under `/api/v1/`.

### Swagger UI
Available at: [`/api/v1/docs/swagger/`](/api/v1/docs/swagger/)

### Redoc
Available at: [`/api/v1/docs/redoc/`](/api/v1/docs/redoc/)

### Authentication
Supported methods:
- JWT Tokens
- DRF Token Authentication

Example:
```http
Authorization: Bearer <jwt_token>
