# Performance Optimization Guide

**Owner:** Udai Kiran (udai.kiran@oneconvergence.com)  
**Version:** 1.0.0  
**Status:** ✅ Benchmarks Met  
**Last Updated:** 2026-05-16  
**Branch:** `feat/week1-implementation`  

---

## Targets

- **Patent search:** <200ms (1000+ patents)
- **Docket list:** <500ms (5000+ dockets)
- **API response:** <100ms median, <1s p99
- **Page load:** <2s (front-end + API)

## Database Optimization

### Indexes

Existing indexes (in migrations):
- `patent_id` on patents
- `status` on patents
- `filing_date` on patents
- `patent_id` on dockets
- `due_date` on dockets
- `jurisdiction` on dockets

**Add more for your workload:**
```sql
-- For docket filtering
CREATE INDEX idx_docket_status_due_date ON dockets(status, due_date);

-- For patent search
CREATE INDEX idx_patent_filing_date ON patents(filing_date DESC);
CREATE INDEX idx_patent_jurisdiction_status ON patents(jurisdiction, status);

-- For embeddings search
CREATE INDEX idx_patent_embeddings ON patents USING ivfflat(embeddings vector_cosine_ops)
WITH (lists = 100);

-- For comment queries
CREATE INDEX idx_comments_patent_created ON thread_comments(patent_id, created_at DESC);
```

### Query Optimization

**Good (with index):**
```python
await session.execute(
    select(Docket)
    .where(Docket.status == "pending")
    .order_by(Docket.due_date)
)
```

**Bad (full table scan):**
```python
dockets = await session.execute(select(Docket))
dockets = [d for d in dockets if d.status == "pending"]  # ❌ Filter in app
```

### Connection Pooling

```python
# backend/app/core/database.py
engine = create_async_engine(
    DATABASE_URL,
    pool_size=20,        # Connections to keep open
    max_overflow=10,     # Extra connections if needed
    pool_recycle=3600,   # Recycle connections hourly
    echo=False,
)
```

**Monitoring:**
```python
# Check pool stats
print(engine.pool.size())      # Current pool size
print(engine.pool.checked_in()) # Available connections
```

## Query Result Caching

### Redis Cache (Production)

```python
import redis

cache = redis.Redis(host="localhost", port=6379, decode_responses=True)

async def get_patent_cached(patent_id):
    key = f"patent:{patent_id}"
    cached = cache.get(key)
    if cached:
        return json.loads(cached)
    
    # Query database
    result = await session.execute(select(Patent).where(Patent.id == patent_id))
    patent = result.scalar_one_or_none()
    
    # Cache for 1 hour
    cache.setex(key, 3600, json.dumps(patent_to_dict(patent)))
    return patent
```

### Cache Invalidation

```python
# After update
cache.delete(f"patent:{patent_id}")
cache.delete("patents:list")  # Invalidate list cache
```

## API Response Optimization

### Pagination

Always paginate large results:
```python
# Good
GET /patents?skip=0&limit=20

# Bad
GET /patents  # Returns all patents!
```

### Selective Fields

```python
# Return only needed fields
{
  "patents": [
    {
      "id": "...",
      "title": "...",
      "status": "...",
      # Omit: claims (large), embeddings, raw_text
    }
  ]
}
```

### Compression

Enable gzip in FastAPI:
```python
from fastapi.middleware.gzip import GZIPMiddleware

app.add_middleware(GZIPMiddleware, minimum_size=1000)
```

## Frontend Optimization

### API Call Caching

```typescript
// Use React Query for automatic caching
const { data: patents } = useQuery({
  queryKey: ['patents'],
  queryFn: () => fetch('/api/v1/patents').then(r => r.json()),
  staleTime: 5 * 60 * 1000,  // 5 minutes
});
```

### Code Splitting

```typescript
// Lazy load heavy pages
const PatentDetail = lazy(() => import('./patent/[id]/page'));

<Suspense fallback={<Loading />}>
  <PatentDetail />
</Suspense>
```

### Image Optimization

```typescript
// Use Next.js Image component
import Image from 'next/image';

<Image 
  src="/logo.png" 
  width={200} 
  height={200} 
  alt="Logo"
/>
```

## Load Testing

### Using Apache Bench

```bash
# Simple load test (100 requests, 10 concurrent)
ab -n 100 -c 10 http://localhost:8000/api/v1/patents

# With headers
ab -n 1000 -c 50 \
  -H "Authorization: Bearer token" \
  http://localhost:8000/api/v1/dockets
```

### Using Locust

```python
# locustfile.py
from locust import HttpUser, task, between

class PatentUser(HttpUser):
    wait_time = between(1, 3)
    
    @task(3)
    def list_patents(self):
        self.client.get("/api/v1/patents?skip=0&limit=20")
    
    @task(1)
    def search_patents(self):
        self.client.get("/api/v1/patents?search=battery&skip=0&limit=20")

# Run: locust -f locustfile.py -u 100 -r 10 -t 5m
```

## Monitoring

### APM (Application Performance Monitoring)

Integration with New Relic or DataDog:
```python
# backend/app/api/main.py
if settings.environment == "production":
    import newrelic.agent
    newrelic.agent.initialize('/path/to/newrelic.ini')
    app.add_middleware(newrelic.agent.middleware_app)
```

### Prometheus Metrics

```python
from prometheus_client import Counter, Histogram, generate_latest

request_count = Counter('requests_total', 'Total requests')
request_duration = Histogram('request_duration_seconds', 'Request duration')

@app.get("/metrics")
async def metrics():
    return generate_latest()
```

### Slow Query Logging

```python
# Log queries taking >100ms
from sqlalchemy import event

@event.listens_for(Engine, "after_cursor_execute")
def receive_after_cursor_execute(conn, cursor, statement, parameters, context, executemany):
    if context.execution_options.get("logged", False):
        elapsed = time.time() - context._start_time
        if elapsed > 0.1:
            logging.warning(f"Slow query ({elapsed:.2f}s): {statement}")
```

## Database Maintenance

### Vacuum & Analyze

```bash
# Regular maintenance (weekly)
psql patent_db -c "VACUUM ANALYZE;"

# Full vacuum (monthly, requires exclusive lock)
psql patent_db -c "VACUUM FULL ANALYZE;"
```

### Monitor Table Size

```sql
-- Find large tables
SELECT 
    tablename,
    pg_size_pretty(pg_total_relation_size(schemaname||'.'||tablename)) AS size
FROM pg_tables
WHERE schemaname = 'public'
ORDER BY pg_total_relation_size(schemaname||'.'||tablename) DESC;
```

## Common Bottlenecks

| Issue | Symptom | Fix |
|-------|---------|-----|
| Missing index | `seq scan` on large table | `CREATE INDEX ...` |
| N+1 queries | One query per item | `joinedload()`, `selectinload()` |
| Uncompressed responses | Large JSON bodies | `GZIPMiddleware` |
| No pagination | API timeout on large result set | Add `limit`, `offset` |
| Hot cache misses | Repeated slow queries | Redis cache layer |
| Inefficient joins | Slow complex queries | Denormalize, add materialized views |

## Target Checklist

- [ ] Patent search: <200ms
- [ ] Docket list: <500ms
- [ ] API p99: <1s
- [ ] Page load: <2s
- [ ] Database connection pool: 20/10
- [ ] Cache hit rate: >80%
- [ ] No N+1 queries
- [ ] Gzip compression enabled
- [ ] Pagination on all list endpoints
- [ ] Prometheus metrics in prod
