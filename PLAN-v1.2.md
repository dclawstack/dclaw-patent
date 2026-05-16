# DClaw Patent — v1.2 Feature Roadmap

> 📘 **REVISED PRD v2.3 available:** See `REVISED-PRD.md` for complete gap analysis, current state, and full feature roadmap.


> Based on: Y Combinator vertical SaaS principles, trending GitHub repos (patent-analysis-tools), AI product research (Anaqua, CPA Global, PatSnap, Cipher)

## Pre-Flight Checklist

- [ ] `frontend/package-lock.json` committed after any `npm install` / dependency change
- [ ] `frontend/next-env.d.ts` exists and is committed
- [ ] `docker-compose.yml` healthchecks correct
- [ ] `frontend/Dockerfile` declares `ARG NEXT_PUBLIC_API_URL` before `RUN npm run build`

## v1.0 Feature Inventory (Current)

- [ ] Patent portfolio CRUD
- [ ] Docketing & deadline tracking
- [ ] Prior art search
- [ ] Document management
- [ ] Real backend CRUD (no mocks)
- [ ] Docker + Helm deployment
- [ ] Alembic migrations
- [ ] Backend tests

---

## v1.2 Roadmap

### P0 — Must Have (Ship in v1.0, demo-ready)

#### 1. AI Patent Copilot (Research Assistant)
**Description:** AI assistant that searches patent databases, summarizes claims, and identifies similar patents. "Find me patents related to quantum computing error correction."
- **AI Angle:** RAG over patent corpora. Claim summarization. Similarity search (embeddings).
- **Backend:** `/api/v1/ai/patent-search` endpoint. Vector store for patent embeddings.
- **Frontend:** AI research panel with patent cards and similarity scores.
- **Files:** `backend/app/services/patent_ai.py`, `frontend/src/components/patent-copilot.tsx`

#### 2. Prior Art Search & Analysis
**Description:** Search USPTO, EPO, WIPO databases. AI ranks results by relevance to your invention.
- **Backend:** Patent API integration (PatentsView, EPO Open Patent Services).
- **Frontend:** Search results with relevance badges. Side-by-side claim comparison.
- **Files:** `backend/app/services/prior_art.py`

#### 3. Docketing & Deadline Management
**Description:** Track filing deadlines, response deadlines, maintenance fee due dates. Auto-reminders.
- **Backend:** Deadline calculation engine (country-specific rules). Alert system.
- **Frontend:** Docket calendar. Deadline list with urgency colors.
- **Files:** `backend/app/services/docketing.py`

#### 4. Patent Portfolio Dashboard
**Description:** Visual overview of all patents: status map, technology clusters, geographic coverage, spend analysis.
- **Backend:** Portfolio aggregation API.
- **Frontend:** Interactive dashboard with maps, charts, and filterable grids.
- **Files:** `frontend/src/app/portfolio/dashboard.tsx`

### P1 — Should Have (v1.1–1.2)

#### 5. AI Claim Drafting Assistant
**Description:** AI helps draft patent claims from invention disclosure. Suggests claim structures and dependent claims.
- **AI Angle:** LLM claim generation with patent-specific prompting.
- **Backend:** `/api/v1/ai/draft-claims` endpoint.
- **Frontend:** Claim editor with AI suggest buttons.

#### 6. Technology Landscape Mapping
**Description:** Visual map of patent landscapes by technology area. Identify white spaces and competitor activity.
- **Backend:** Patent clustering + visualization data.
- **Frontend:** Interactive landscape map (bubble/treemap).

#### 7. Invention Disclosure Workflow
**Description:** Structured intake form for inventors. Review workflow for patent committee.
- **Backend:** Disclosure form builder. Review routing.
- **Frontend:** Disclosure submission wizard. Review queue.

#### 8. Competitive Intelligence
**Description:** Monitor competitor patent filings. Alert on new publications in your technology areas.
- **Backend:** Competitor watch lists. New patent alert engine.
- **Frontend:** Competitor dashboard. Alert inbox.

### P2 — Could Have (v1.3+)

#### 9. AI Patent Valuation
**Description:** Estimate patent value based on citations, family size, licensing history, and market data.

#### 10. Freedom-to-Operate Analysis
**Description:** Systematic FTO search with risk heatmap for product launches.

#### 11. Patent Licensing Marketplace
**Description:** List available patents for licensing. Match with potential licensees.

#### 12. Auto-Generated Patent Drawings
**Description:** AI-generated technical drawings from invention descriptions.

---

## Implementation Priority

1. **Week 1–2:** AI Patent Copilot (P0.1) + Prior Art Search (P0.2)
2. **Week 3–4:** Docketing (P0.3) + Portfolio Dashboard (P0.4)
3. **Week 5–6:** Claim Drafting AI (P1.5) + Landscape Mapping (P1.6)
4. **Week 7–8:** Disclosure Workflow (P1.7) + Competitive Intel (P1.8)

---
> **Document Owner:** Udai Kiran | **Email:** udai.kiran@oneconvergence.com
> **Last Modified:** 2026-05-16 | **Admin Tracking:** Active
