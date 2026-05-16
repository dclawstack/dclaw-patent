# DClaw Patent — Setup Guide

## Quick Start

### Prerequisites
- Docker & Docker Compose
- Python 3.11+
- Node.js 18+
- PostgreSQL 15+

### 1. Clone & Install

```bash
git clone <repo>
cd dclaw-patent-claude

# Backend
cd backend
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt

# Frontend
cd ../frontend
npm install
```

### 2. Environment Setup

**Backend** (`.env`):
```
DATABASE_URL=postgresql+asyncpg://user:password@localhost:5432/patent_db
ANTHROPIC_API_KEY=sk-...
REDIS_URL=redis://localhost:6379
```

**Frontend** (`.env.local`):
```
NEXT_PUBLIC_API_URL=http://localhost:8000/api/v1
```

### 3. Database

```bash
# Create database
createdb patent_db

# Run migrations
cd backend
alembic upgrade head
```

### 4. Start Services

**Option A: Docker Compose (Recommended)**
```bash
docker-compose up
```

**Option B: Manual**
```bash
# Terminal 1: Backend
cd backend
uvicorn app.api.main:app --reload --port 8000

# Terminal 2: Frontend
cd frontend
npm run dev

# Terminal 3: PostgreSQL
# (if not using system PostgreSQL)
docker run -e POSTGRES_PASSWORD=password \
  -e POSTGRES_DB=patent_db \
  -p 5432:5432 postgres:15
```

### 5. Verify Installation

```bash
# Backend health check
curl http://localhost:8000/health

# Frontend
open http://localhost:3000
```

---

## Development Workflow

### Add a New Model

1. Create in `backend/app/models/feature.py`
2. Create migration: `alembic revision --autogenerate -m "description"`
3. Run migration: `alembic upgrade head`
4. Add endpoints to `backend/app/api/v1/feature.py`
5. Wire router in `backend/app/api/main.py`

### Add Tests

```bash
cd backend
pytest tests/test_feature.py -v
```

### Frontend Development

```bash
cd frontend
npm run dev       # Start dev server
npm run build     # Production build
npm run lint      # Type check & format
```

---

## Production Deployment

### Docker Images

```bash
# Build images
docker build -t dclaw-patent-backend:1.0 ./backend
docker build -t dclaw-patent-frontend:1.0 ./frontend

# Tag for registry
docker tag dclaw-patent-backend:1.0 registry.example.com/dclaw-patent-backend:1.0
docker tag dclaw-patent-frontend:1.0 registry.example.com/dclaw-patent-frontend:1.0

# Push
docker push registry.example.com/dclaw-patent-backend:1.0
docker push registry.example.com/dclaw-patent-frontend:1.0
```

### Kubernetes Deployment

```bash
# Create namespace
kubectl create namespace patent

# Deploy database (PostgreSQL Helm chart)
helm repo add bitnami https://charts.bitnami.com/bitnami
helm install postgres bitnami/postgresql -n patent

# Deploy backend
kubectl apply -f k8s/backend.yaml -n patent

# Deploy frontend
kubectl apply -f k8s/frontend.yaml -n patent

# Verify
kubectl get pods -n patent
```

### Environment Variables

**Production Backend:**
- `DATABASE_URL`: PostgreSQL connection string (replicate)
- `ANTHROPIC_API_KEY`: Claude API key
- `REDIS_URL`: Redis connection string
- `CORS_ORIGINS`: Allowed frontend origins
- `LOG_LEVEL`: INFO or DEBUG

**Secrets (Kubernetes):**
```bash
kubectl create secret generic patent-secrets \
  --from-literal=anthropic-api-key=$ANTHROPIC_API_KEY \
  --from-literal=db-password=$DB_PASSWORD \
  -n patent
```

### Database Backups

```bash
# Daily backup
pg_dump patent_db > backup-$(date +%Y%m%d).sql

# Restore
psql patent_db < backup-20240115.sql
```

---

## Monitoring

### Logs

```bash
# Docker
docker-compose logs -f backend
docker-compose logs -f frontend

# Kubernetes
kubectl logs -f deployment/patent-backend -n patent
```

### Health Checks

```bash
# Backend API
curl http://localhost:8000/health

# Database connection
psql $DATABASE_URL -c "SELECT 1"

# Redis
redis-cli ping
```

### Metrics

Backend exposes Prometheus metrics at `/metrics`:
```
curl http://localhost:8000/metrics
```

---

## Troubleshooting

### Database Connection Error
```
Error: could not connect to server: Connection refused

Solution:
1. Verify PostgreSQL is running: psql -U postgres
2. Check DATABASE_URL environment variable
3. Run migrations: alembic upgrade head
```

### API Returns 500 Error

```bash
# Check backend logs
docker-compose logs backend

# Verify database migrations
alembic current
alembic upgrade head
```

### Frontend Can't Connect to Backend

```
Error: Failed to fetch from http://localhost:8000

Solution:
1. Verify backend is running: curl http://localhost:8000/health
2. Check NEXT_PUBLIC_API_URL in .env.local
3. Verify CORS_ORIGINS includes frontend URL
```

### Claude API Errors

```
Error: ANTHROPIC_API_KEY not set

Solution:
1. Generate API key: https://console.anthropic.com
2. Set in .env: ANTHROPIC_API_KEY=sk-...
3. Restart backend
```

---

## Configuration

### Database Pool Settings

```python
# backend/app/core/database.py
engine = create_async_engine(
    DATABASE_URL,
    echo=False,
    pool_size=20,
    max_overflow=10,
)
```

### API Rate Limiting

```python
# backend/app/api/main.py
app.add_middleware(
    RateLimitMiddleware,
    requests_per_minute=100,
)
```

### CORS

```python
app.add_middleware(
    CORSMiddleware,
    allow_origins=os.getenv("CORS_ORIGINS", "*").split(","),
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

---

## Testing

### Run All Tests

```bash
cd backend
pytest -v --cov=app tests/
```

### Run Specific Test Suite

```bash
pytest tests/test_legal_automation.py -v
pytest tests/test_docketing.py::TestDeadlineCalculator -v
```

### E2E Tests

```bash
cd frontend
npm run test:e2e
```

---

## Contributing

1. Create feature branch: `git checkout -b feat/feature-name`
2. Make changes, add tests
3. Run linter: `npm run lint` (frontend), `black .` (backend)
4. Commit: `git commit -m "feat: description"`
5. Push: `git push origin feat/feature-name`
6. Open PR and request review

---

## Support

For issues, questions, or feature requests:
1. Check [API.md](API.md) for endpoint documentation
2. Review test files for usage examples
3. File GitHub issue with reproduction steps

---

## License

Proprietary — All Rights Reserved
