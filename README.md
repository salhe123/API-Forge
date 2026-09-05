# API Forge

Expert-level FastAPI workshop: a production-style API with versioned routes, SQLAlchemy, JWT auth, and Alembic migrations.

## What it does

- Health check and a hello route
- User **register** / **login** / **me** with JWT
- Item CRUD: list and get are public; create, update, and delete require the owner
- SQLite database at `api_forge.db`
- Schema changes tracked with Alembic
- Tests and GitHub Actions (Python 3.9–3.11)

## Setup

Python 3.9+ recommended.

```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
alembic upgrade head
uvicorn app.main:app --reload
```

Open:

- API docs: [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)
- Health: [http://127.0.0.1:8000/api/v1/health](http://127.0.0.1:8000/api/v1/health)

If the database already exists from an older `create_all` run, stamp it instead of recreating tables:

```bash
alembic stamp head
```

## Request flow

A request walks down the layers, then the response walks back up.

```
Client
  → route         app/api/v1/           HTTP only
  → deps          app/api/deps.py       DB session + current user
  → service       app/services/         business rules
  → repository    app/repositories/     SQLAlchemy queries
  → model + db    app/models/ + app/db  tables → api_forge.db
```

| Layer | Job |
|---|---|
| Schema (`app/schemas/`) | JSON in/out (Pydantic) |
| Route | URL, method, status codes |
| Deps | Who is calling, which DB session |
| Service | Allowed or not (`raise` → 401/403/404/409) |
| Repository | Save and load rows |
| Model | Table shape (SQLAlchemy ORM) |
| Alembic | Changelog for those tables |

**`return`** = success. **`raise`** = stop, FastAPI maps it to an HTTP error.

## Project layout

```
app/
  main.py                 App factory, error handlers, lifespan
  api/v1/                 HTTP routes (health, auth, items)
  api/deps.py             get_db, get_current_user
  core/                   Settings, security, exceptions
  schemas/                Request/response contracts
  services/               Business rules
  repositories/           Database access
  models/                 SQLAlchemy tables
  db/                     Engine, sessions, Alembic upgrade on startup
alembic/versions/         Migration files
tests/                    pytest
```

## Auth in /docs

Login uses **JSON**, same shape as register (`email` + `password`), not the old OAuth2 form.

1. `POST /api/v1/auth/register`
2. `POST /api/v1/auth/login` — copy `access_token`
3. Click **Authorize** and paste the token
4. Call `GET /api/v1/auth/me` or create items

`GET /me` without a token returns **401**. That is expected.

```bash
# register
curl -X POST 'http://127.0.0.1:8000/api/v1/auth/register' \
  -H 'Content-Type: application/json' \
  -d '{"email":"forge@example.com","password":"secret123"}'

# login
curl -X POST 'http://127.0.0.1:8000/api/v1/auth/login' \
  -H 'Content-Type: application/json' \
  -d '{"email":"forge@example.com","password":"secret123"}'

# current user (replace TOKEN)
curl 'http://127.0.0.1:8000/api/v1/auth/me' \
  -H 'Authorization: Bearer TOKEN'
```

## Endpoints

| Method | Path | Auth |
|---|---|---|
| `GET` | `/` | No |
| `GET` | `/api/v1/health` | No |
| `POST` | `/api/v1/auth/register` | No |
| `POST` | `/api/v1/auth/login` | No |
| `GET` | `/api/v1/auth/me` | Bearer token |
| `GET` | `/api/v1/items/` | No |
| `GET` | `/api/v1/items/{id}` | No |
| `POST` | `/api/v1/items/` | Owner |
| `PUT` | `/api/v1/items/{id}` | Owner |
| `DELETE` | `/api/v1/items/{id}` | Owner |

## Alembic

```bash
alembic upgrade head
alembic revision --autogenerate -m "describe the change"
alembic downgrade -1
alembic current
```

Startup runs `alembic upgrade head` (skipped in tests). Tests build tables in memory.

## Tests

```bash
source venv/bin/activate
pytest
```

CI runs flake8 and pytest on Python 3.9, 3.10, and 3.11. Do not commit `venv/` or `*.db`.
