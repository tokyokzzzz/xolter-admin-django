# Holter Django — Supervisor Auth API

Django REST API for Holter Monitor supervisor management.
Handles registration, approval workflow, JWT authentication, and token verification for FastAPI integration.

## Endpoints

| Method | URL | Auth | Description |
|--------|-----|------|-------------|
| POST | `/api/register/` | No | Register supervisor (status: PENDING) |
| POST | `/api/login/` | No | Login and receive JWT tokens |
| GET | `/api/status/` | Bearer | Current user status |
| POST | `/api/verify-token/` | No | Validate JWT (used by FastAPI) |
| GET/POST | `/admin/` | Session | Django admin panel |

## Deploy with Docker

```bash
git clone https://github.com/<your-username>/holter-django.git
cd holter-django

# Copy and configure environment
cp .env.example .env   # edit SECRET_KEY

# Build and start
docker compose up -d --build

# Run migrations
docker compose exec django-api python manage.py migrate

# Create admin superuser
docker compose exec django-api python manage.py createsuperuser
```

## Local Development

```bash
python -m venv venv
source venv/bin/activate      # Windows: venv\Scripts\activate
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver 0.0.0.0:8001
```

## Environment Variables

| Variable | Description |
|----------|-------------|
| `SECRET_KEY` | Django secret key |
| `DEBUG` | `True` for dev, `False` for prod |
| `ALLOWED_HOSTS` | Comma-separated hosts |

## Supervisor Approval Flow

1. Supervisor registers → status `PENDING`
2. Admin approves in `/admin/` → status `APPROVED`
3. Supervisor logs in → receives JWT
4. FastAPI calls `/api/verify-token/` to validate each request
# xolter-admin-django
