# TalentAI API Gateway (`apps/api-gateway`)

Production-Grade FastAPI Modular Monolith API Gateway for the TalentAI platform. Built with Python 3.13+, FastAPI, Pydantic Settings v2, PostgreSQL, Redis, and multi-stage Docker builds.

---

## 🚀 Key Features & Architecture

- **Modular Monolith**: Enterprise layered architecture (`app/routers/`, `app/schemas/`, `app/services/`, `app/repositories/`, `app/models/`, `app/auth/`, `app/integrations/`).
- **Pydantic Settings v2**: Type-safe, modular application configuration reading from environment variables.
- **Production Logging**: Structured rotating log files (`logs/app.log`, `logs/error.log`, `logs/access.log`) with ANSI color console formatting for development.
- **Request Tracing**: Automated correlation `X-Request-ID` header generation and propagation.
- **Multi-Stage Docker**: Containerized with Python 3.13-slim, `/opt/venv` caching, and non-root execution (`appuser:10001`).

---

## 🛠️ Environment Configuration

Environment variables are managed via `.env` files. Templates are provided for all deployment environments:

| File | Purpose |
| :--- | :--- |
| `.env.example` | Master template containing all configuration variables |
| `.env.development` | Local development default overrides |
| `.env.production` | Production deployment template |

To configure local environment:
```bash
cp .env.example .env
```

### Key Environment Variables

```ini
# Application
APP_NAME="TalentAI API Gateway"
APP_ENV=development
APP_VERSION=0.1.0
DEBUG=true
SECRET_KEY=your_secure_secret_key
LOG_LEVEL=INFO

# Server
HOST=0.0.0.0
PORT=8000
API_PREFIX=/api/v1
ALLOWED_HOSTS=http://localhost:3000,http://127.0.0.1:3000

# Database & Redis
DATABASE_URL=postgresql+asyncpg://postgres:postgres_password@localhost:5432/talentai
REDIS_URL=redis://localhost:6379/0

# JWT Authentication
JWT_SECRET=your_jwt_secret_key
JWT_ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=60
REFRESH_TOKEN_EXPIRE_DAYS=7

# Email & Storage & AI
RESEND_API_KEY=re_your_resend_key
CLOUDINARY_CLOUD_NAME=your_cloudinary_cloud
OPENAI_API_KEY=sk-your_openai_key
GEMINI_API_KEY=AIza_your_gemini_key
```

---

## 💻 Running Locally

### Prerequisites
- Python 3.13+
- Virtualenv (`python -m venv .venv`)

### Setup & Execution
1. Activate virtual environment:
   ```bash
   python -m venv .venv
   # Windows PowerShell
   .venv\Scripts\Activate.ps1
   ```
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Run the Uvicorn development server:
   ```bash
   uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
   ```
4. Access Interactive API Docs:
   - **Swagger UI**: [http://localhost:8000/docs](http://localhost:8000/docs)
   - **ReDoc**: [http://localhost:8000/redoc](http://localhost:8000/redoc)
   - **Health Check**: [http://localhost:8000/health](http://localhost:8000/health)

---

## 🐳 Docker Deployment

### Multi-Stage Build
Build the production Docker image:
```bash
docker build -t talentai-api-gateway .
```

Run the container:
```bash
docker run -d \
  --name talentai-backend \
  -p 8000:8000 \
  --env-file .env \
  talentai-api-gateway
```

---

## 📦 Docker Compose Infrastructure

Run the entire backend stack (FastAPI Backend, PostgreSQL 16, Redis 7, pgAdmin 4) from the repository root:

```bash
docker-compose up -d --build
```

### Stack Services & Interfaces

- **Backend API Gateway**: [http://localhost:8000](http://localhost:8000)
- **API Health Check**: [http://localhost:8000/health](http://localhost:8000/health)
- **PostgreSQL Database**: `localhost:5432` (database: `talentai`, user: `postgres`)
- **Redis Cache & Broker**: `localhost:6379`
- **pgAdmin Web Console**: [http://localhost:5050](http://localhost:5050) (User: `admin@talentai.com`, Password: `admin_password_secure`)

To stop the container stack:
```bash
docker-compose down
```

---

## 📝 Logging System

Logs are output to `sys.stdout` and stored in rotating log files under `logs/`:

- `logs/app.log`: Application log records (rotated at 10MB, 5 backup retains).
- `logs/error.log`: Error and critical level log records.
- `logs/access.log`: HTTP access logs with execution time in milliseconds and request correlation IDs.
