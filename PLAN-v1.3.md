# DClaw Patent — v1.3 Strategic Product Roadmap & Implementation Plan

> **Date:** 2026-05-16
> **Status:** Draft → Implementation Phase
> **Goal:** Transform scaffold into YC-competitive patent management SaaS

---

## Phase 1: Environment Audit Results

### ✅ Git & Remote
- Remote origin: `https://github.com/dclawstack/dclaw-patent.git`
- User email/name configured: `udaikiran@outlook.com` / `udaikiran`
- Dry-run push successful — write permissions confirmed

### ⚠️ Knowledge Management
- **No Obsidian Vault or graphify knowledge graph found** in repository
- Recommendation: Create a `/docs/knowledge/` directory or integrate with external PKM for tracking architectural decisions and sprint progress

### 🔧 Infrastructure Fixes Required
| Issue | Current | Required | File |
|-------|---------|----------|------|
| Backend port | `8147` | `8065` | `docker-compose.yml`, `backend/Dockerfile` |
| Frontend port | `3061` | `3065` | `docker-compose.yml`, `frontend/Dockerfile`, `frontend/package.json` |
| Database name | `dclaw_patent` | ✅ Already correct | `docker-compose.yml` |
| API health path | `/health/` | ✅ Correct | `backend/app/api/main.py` |

---

## Phase 2: YC Gap Analysis Summary

### Current State (v0.0 Scaffold)
- **Backend:** FastAPI scaffold with zero models, zero routes, zero services
- **Frontend:** Next.js placeholder page with no patent-specific UI
- **Database:** PostgreSQL container, empty schema
- **Tests:** Only healthcheck test exists
- **AI/ML:** Non-existent
- **Competitive Position:** Not shippable

### Critical Gaps vs. YC Standard
| Gap | Why It Blocks YC | Priority |
|-----|------------------|----------|
| No patent CRUD | Cannot demonstrate core workflow | P0 |
| No docketing | Patent attorneys won't adopt without deadlines | P0 |
| No portfolio dashboard | Executives need visual KPIs | P0 |
| No prior art search | "Better Google Patents" value prop missing | P0 |
| No semantic search | AI-native claim missing | P1 |
| No examiner prediction | Only differentiation vs. incumbents | P2 |

### Competitive Moat Strategy
1. **Speed:** PostgreSQL + async FastAPI + Next.js = <1s page loads
2. **Price:** Target $500–$2k/mo vs. AnAqua $500k/yr
3. **UX:** Tailwind + pre-built shadcn components = fast, clean UI
4. **AI-Ready Architecture:** pgvector-ready schema, service layer stubbed for LLM integration

---

## Phase 3: Prioritized Feature Roadmap

### Complexity Legend
- **0 — Low / Foundation:** Scaffolding, CRUD, config fixes, basic pages
- **1 — Medium / Differentiator:** External APIs, search, dashboards, workflows
- **2 — High / AI-Native:** LLM integration, embeddings, ML predictions, multimodal

---

### P0 — Foundation (Week 1–2) — Complexity 0

#### [0.1] Infrastructure & Port Alignment
- Fix backend port to `8065`, frontend to `3065` across all config files
- Verify `docker-compose config` passes
- Add `ARG NEXT_PUBLIC_API_URL` before `RUN npm run build` in frontend Dockerfile ✅ (already present)

#### [0.2] Patent Core Data Model
- **Model:** `Patent` (UUID, patent_number, title, abstract, claims JSON, description, filing_date, issue_date, status enum, applicant, inventors JSON, technology_category, jurisdiction, created_at, updated_at)
- **Schema:** Pydantic v2 CRUD schemas with `ConfigDict(from_attributes=True)`
- **Repository:** `PatentRepository(BaseRepository[Patent])`
- **Router:** `/api/v1/patents` — full CRUD + list with filters
- **Tests:** Repository tests + router tests with `httpx.AsyncClient`
- **Alembic migration:** Auto-generate initial schema

#### [0.3] Docket & Deadline Tracking
- **Model:** `DocketEvent` (UUID, patent_id FK, event_type enum, due_date, description, status enum, assignee, created_at, updated_at)
- **Schema:** CRUD + alert/urgent endpoints
- **Repository:** `DocketRepository` with `get_overdue()` and `get_upcoming(days=30)`
- **Router:** `/api/v1/dockets` — CRUD + `/alerts` for urgent/upcoming
- **Tests:** Full coverage

#### [0.4] Prior Art Model (Storage)
- **Model:** `PriorArt` (UUID, patent_id FK, source_patent_number, source_title, relevance_score, claim_mapping JSON, analysis_notes, created_at, updated_at)
- **Schema:** CRUD schemas
- **Repository:** `PriorArtRepository`
- **Router:** `/api/v1/prior-art` — nested under patents
- **Tests:** Repository + router tests

#### [0.5] Frontend — Portfolio Dashboard
- **Page:** `/` → Portfolio overview
- **Components:** Summary cards (total patents, by status, by jurisdiction), patent table (sortable/filterable), quick-add patent button
- **API Integration:** Wire to `src/lib/api.ts` → `getPatents()`, `createPatent()`, etc.

#### [0.6] Frontend — Patent Detail & Docket View
- **Page:** `/patents/[id]` → Patent detail with tabs (Overview, Claims, Docket, Prior Art)
- **Components:** Patent info card, claims viewer (JSON-rendered), docket list with urgency badges, add/edit docket events

---

### P1 — Core Differentiators (Week 3–4) — Complexity 1

#### [1.1] Prior Art Search Integration (PatentsView API)
- **Service:** `backend/app/services/prior_art_search.py`
- **Endpoint:** `POST /api/v1/search/prior-art` — query PatentsView API, rank by text similarity (basic TF-IDF or keyword overlap)
- **Frontend:** Search bar on patent detail page, results with "Add to Prior Art" button
- **Value Prop:** "Find relevant prior art in 10 seconds vs. 3 days"

#### [1.2] Docketing Calendar View
- **Frontend:** `/docket` page with calendar grid + list view
- **Components:** Color-coded events (red=overdue, yellow=<7 days, green=ok)
- **API:** Wire to docket alerts endpoint

#### [1.3] Semantic Search Infrastructure (pgvector)
- **Backend:** Add `pgvector` to PostgreSQL, add `embeddings` vector column to `Patent`
- **Service:** `patent_embeddings.py` — OpenAI/HuggingFace embedding generation stub
- **Endpoint:** `POST /api/v1/search/semantic` — cosine similarity over patent embeddings
- **Note:** Full semantic search needs patent corpus ingestion (P2). This P1 task is schema + stub.

#### [1.4] Technology Category Auto-Tagging
- **Service:** Rule-based or lightweight LLM stub for auto-tagging patents by technology
- **Trigger:** On patent creation/update
- **Value:** Reduces manual data entry

---

### P2 — AI-Native Features (Week 5–8) — Complexity 2

#### [2.1] AI Patent Copilot (LLM-Powered Research Assistant)
- **Backend:** `/api/v1/ai/patent-search` — RAG over patent abstracts + claims
- **Integration:** OpenAI GPT-4o or Claude API for summarization + Q&A
- **Frontend:** Chat panel in patent detail page
- **Context:** Invention description → AI suggests relevant prior art, claim structures

#### [2.2] Examiner Prediction Stub
- **Model:** `ExaminerPrediction` (UUID, patent_id FK, predicted_allowance_probability, suggested_amendments JSON, confidence_factors JSON)
- **Service:** Rule-based heuristic + LLM prompt (not true ML yet — data scarcity)
- **Endpoint:** `POST /api/v1/predictions/allowance`
- **Frontend:** Probability badge + amendment suggestions panel

#### [2.3] Claim Mapping (AI-Assisted)
- **Service:** LLM-based claim-to-prior-art mapping
- **Input:** User patent claims + prior art claims
- **Output:** JSON mapping `{ user_claim_num: [source_claim_nums], risk_level: "high|medium|low" }`
- **Frontend:** Side-by-side claim comparison with risk highlights

#### [2.4] Competitive Intelligence (Watch Lists)
- **Model:** `CompetitorWatch` (UUID, company_name, technology_keywords JSON, last_scan_date)
- **Service:** Periodically query PatentsView for new filings by competitor
- **Endpoint:** `/api/v1/competitors` CRUD + `/api/v1/competitors/{id}/filings`
- **Frontend:** Watch list manager + recent filings feed

#### [2.5] PDF Report Generation
- **Service:** `report_generator.py` using `weasyprint` or `pdfkit`
- **Endpoints:**
  - `POST /api/v1/reports/prior-art` — Prior art analysis PDF
  - `POST /api/v1/reports/portfolio` — Portfolio summary PDF
- **Frontend:** "Download Report" buttons on detail + dashboard pages

---

## Success Metrics for YC Demo Day (v1.3 Target)

| Metric | Target | How Measured |
|--------|--------|--------------|
| **Patent CRUD** | 100% functional | Cypress / manual test |
| **Docket Alerts** | <30s to see urgent deadlines | UX timer test |
| **Prior Art Search** | <10s response | API latency test |
| **Portfolio Dashboard** | <2s load (100 patents) | Lighthouse / manual |
| **Test Coverage** | >70% backend | pytest coverage report |
| **Docker Compose** | `up -d` boots all services | CI test |

---

## Execution Order (Immediate)

1. **Today:** Write PLAN-v1.3.md, fix ports, create Patent model + migration
2. **Day 2:** Patent CRUD router + repository + tests
3. **Day 3:** Docket model + router + tests
4. **Day 4:** Prior Art model + router + tests
5. **Day 5:** Frontend portfolio dashboard + patent detail pages
6. **Day 6–7:** Frontend docket/calendar integration
7. **Week 2:** Prior Art Search API integration (PatentsView)
8. **Week 3:** Semantic search schema (pgvector) + embedding stubs
9. **Week 4:** AI Copilot integration (OpenAI/Claude)
10. **Week 5+:** Examiner prediction, claim mapping, competitive intel

---

## Files to Create/Modify

### Backend
```
backend/app/models/patent.py          ← NEW
backend/app/models/docket.py          ← NEW
backend/app/models/prior_art.py       ← NEW
backend/app/models/__init__.py        ← MODIFY
backend/app/schemas/patent.py         ← NEW
backend/app/schemas/docket.py         ← NEW
backend/app/schemas/prior_art.py      ← NEW
backend/app/schemas/__init__.py       ← MODIFY
backend/app/repositories/patent.py    ← NEW
backend/app/repositories/docket.py    ← NEW
backend/app/repositories/prior_art.py ← NEW
backend/app/api/v1/patents.py         ← NEW
backend/app/api/v1/dockets.py         ← NEW
backend/app/api/v1/prior_art.py       ← NEW
backend/app/api/v1/__init__.py        ← MODIFY
backend/app/api/main.py               ← MODIFY (wire routers)
backend/tests/test_patents.py         ← NEW
backend/tests/test_dockets.py         ← NEW
backend/tests/test_prior_art.py       ← NEW
backend/alembic/versions/...          ← NEW (auto-generate)
backend/requirements.txt              ← MODIFY (add pgvector, openai stubs)
```

### Frontend
```
frontend/src/lib/api.ts               ← MODIFY (add patent/docket/prior-art APIs)
frontend/src/app/page.tsx             ← MODIFY (portfolio dashboard)
frontend/src/app/patents/[id]/page.tsx ← NEW (patent detail)
frontend/src/app/docket/page.tsx      ← NEW (docket calendar)
frontend/src/components/portfolio/    ← NEW directory
frontend/src/components/patent/       ← NEW directory
frontend/src/components/docket/       ← NEW directory
```

### Infrastructure
```
docker-compose.yml                    ← MODIFY (ports 8065/3065)
backend/Dockerfile                    ← MODIFY (port 8065)
frontend/Dockerfile                   ← MODIFY (port 3065)
frontend/package.json                 ← MODIFY (port 3065)
```

---

## Anti-Patterns to Avoid (from AGENTS.md)
- ❌ No `declarative_base()` — use `from app.models.base import Base`
- ❌ No `default_factory=` in `mapped_column()` — use `default=`
- ❌ No mock data / in-memory dicts — all DB access via repositories
- ❌ No manual `get_db()` with `__anext__()` — use `Depends(get_db)`
- ❌ No hardcoded `localhost:PORT` — use `process.env.NEXT_PUBLIC_API_URL`
- ❌ No timezone-aware datetime in models — strip tzinfo
- ❌ No missing alembic migration for new models

---

## Risk Register

| Risk | Likelihood | Mitigation |
|------|------------|------------|
| PatentsView API rate limits | Medium | Cache results, implement backoff |
| pgvector not in CI postgres | Low | Use `pgvector/pgvector:pg16` image |
| LLM API costs during dev | Medium | Use stub responses in test env |
| Frontend build failures | Low | Verify `tailwindcss-animate` in deps |

---

## Next Action
Proceed to Phase 3: Begin autonomous implementation starting with **[0.1] Infrastructure Fix** + **[0.2] Patent Core Data Model**.
