# PRODUCT-SPEC: DClaw Patent Management System

## Overview

**App Name:** DClaw Patent  
**Domain:** Patent Management & IP Analytics  
**Target Users:** SME in-house counsel, startup founders, boutique patent law firms  
**Primary Use Case:** Semantic patent search, prior art analysis, prosecution tracking  
**Market Position:** 10x faster, 10x cheaper than AnAqua/PatSnap/CPA Global

---

## Core Entities & Data Model

### Patent
```
Patent
├── id: UUID (PK)
├── patent_number: str (unique, required)
├── title: str (required)
├── abstract: str (required)
├── claims: JSON (required) — full claim text
├── description: str (required)
├── filing_date: date (required)
├── issue_date: date (optional)
├── status: enum ["drafted", "filed", "prosecution", "issued", "abandoned", "lapsed"] (default: "filed")
├── applicant: str (required)
├── inventors: JSON (array of strings)
├── technology_category: str (optional) — e.g., "software", "mechanical", "biotech"
├── jurisdiction: str (required) — e.g., "US", "EU", "JP"
├── embeddings: vector (pgvector) — semantic search index
├── created_at: datetime
├── updated_at: datetime
└── metadata: JSON (optional) — family ID, citations, etc.
```

### PriorArt
```
PriorArt
├── id: UUID (PK)
├── patent_id: UUID (FK → Patent)
├── source_patent_number: str (required)
├── source_title: str (required)
├── relevance_score: float (0–1, AI-generated)
├── claim_mapping: JSON (optional) — which claims match which source claims
├── analysis_notes: str (optional)
├── created_at: datetime
└── updated_at: datetime
```

### ExaminerPrediction
```
ExaminerPrediction
├── id: UUID (PK)
├── patent_id: UUID (FK → Patent)
├── predicted_allowance_probability: float (0–1, ML model)
├── suggested_claim_amendments: JSON (array of suggestions)
├── examiner_likelihood: float (0–1) — confidence in prediction
├── confidence_factors: JSON — what drove the prediction
├── created_at: datetime
└── updated_at: datetime
```

### Docket
```
Docket
├── id: UUID (PK)
├── patent_id: UUID (FK → Patent)
├── event_type: enum ["filing", "response_due", "maintenance_fee", "prosecution_update", "custom"] (required)
├── due_date: date (required)
├── deadline_description: str (required)
├── status: enum ["pending", "completed", "overdue"] (default: "pending")
├── assignee: str (optional) — responsible person/firm
├── created_at: datetime
└── updated_at: datetime
```

### CompetitorWatch
```
CompetitorWatch
├── id: UUID (PK)
├── company_name: str (required)
├── technology_keywords: JSON (array)
├── recent_filings: JSON (patent list, auto-updated)
├── last_scan_date: datetime
└── created_at: datetime
```

---

## User Stories & Core Screens

### Screen 1: Patent Search (Dashboard)
- **Semantic search bar:** "Machine learning image classification with edge processing"
- **Results:** Patents ranked by relevance (embedding similarity)
- **Quick actions:** Add to portfolio, create prior art analysis, compare claims
- **Filters:** Technology, jurisdiction, date range, patent status

**Core Workflow:**
1. User types natural language query
2. System converts to embeddings
3. Returns top 20 relevant patents (not keyword matches)
4. User clicks "Create Prior Art Analysis" → moves to Screen 3

### Screen 2: My Patents (Portfolio Dashboard)
- **Summary cards:** Total patents, by status (issued/pending/abandoned), geographic coverage, tech distribution
- **Status timeline:** Visual map of filing/issue/expiration dates
- **Patent list table:** Sortable, filterable grid with all patents
- **Quick actions:** Add patent, view details, export portfolio

**Data Shown:**
- Patent number, title, status, filing date, issue date
- Technology category (auto-tagged)
- Upcoming docket events (red flag if deadline in <30 days)

### Screen 3: Patent Detail & Prior Art Analysis
- **Patent info card:** Number, title, claims, abstract, dates
- **AI Predictions:** Allowance probability, suggested amendments (P0.3)
- **Prior Art Section:** Auto-linked prior art with relevance scores
- **Claim Chart:** Side-by-side comparison of claims vs. prior art (P1 feature)
- **Docket/Deadlines:** Upcoming filing dates, response deadlines
- **Timeline:** History of this patent's prosecution

**Core Actions:**
- Edit patent metadata
- Regenerate prior art analysis
- Download prior art report
- Create FTO analysis (P1)

### Screen 4: Prior Art Analysis
- **Uploaded patent:** Full text + claims
- **Search results:** Ranked prior art (with relevance %)
- **Claim mapping:** AI auto-marks which claims are anticipated/obviousness risks
- **Report generation:** Export analysis as PDF (prior art chart, risk assessment)
- **Custom notes:** User can add markup

### Screen 5: Docking Calendar
- **Monthly calendar:** All deadlines color-coded (red=urgent, yellow=upcoming)
- **Deadline list:** Sortable by date, type (filing, maintenance, response)
- **Auto-alerts:** Email reminders at 30/7/1 day before
- **Bulk actions:** Export calendar, assign to firm

### Screen 6: Competitive Intelligence (P1)
- **Watch list:** Companies to monitor
- **Recent filings:** Auto-updated list of competitor patents
- **Technology alerts:** New filings in your tech areas
- **Report:** Monthly competitive snapshot

---

## API Endpoints (v1.0–1.3)

### Patents (CRUD)
```
GET    /api/v1/patents                    → List user's patents
POST   /api/v1/patents                    → Upload/create patent
GET    /api/v1/patents/{id}               → Get patent details
PUT    /api/v1/patents/{id}               → Update patent metadata
DELETE /api/v1/patents/{id}               → Delete patent
```

### Semantic Search (AI)
```
POST   /api/v1/search/semantic            → Search by natural language
  Request: { query: "string" }
  Response: [{ patent_id, title, relevance_score, ... }]

POST   /api/v1/search/prior-art           → Find prior art for a patent
  Request: { patent_id: "uuid" }
  Response: { patent, prior_art: [{ source_patent, relevance, claim_mapping }] }
```

### Predictions (ML)
```
POST   /api/v1/predictions/allowance      → Predict grant likelihood
  Request: { patent_id: "uuid" }
  Response: { probability, confidence, suggested_amendments }

POST   /api/v1/predictions/claim-amendments → Suggest claim improvements
  Request: { patent_id: "uuid" }
  Response: { suggestions: [{ claim_num, amendment, rationale }] }
```

### Docketing
```
GET    /api/v1/dockets                    → List all deadlines
POST   /api/v1/dockets                    → Create deadline
PUT    /api/v1/dockets/{id}               → Update deadline status
DELETE /api/v1/dockets/{id}               → Delete deadline

POST   /api/v1/dockets/alerts             → Get urgent alerts
  Response: { urgent: [...], upcoming: [...] }
```

### Reporting & Export
```
POST   /api/v1/reports/prior-art          → Generate prior art report
  Request: { patent_id: "uuid" }
  Response: PDF blob

POST   /api/v1/reports/portfolio          → Generate portfolio summary
  Response: PDF blob (status, tech distribution, geographic spread)
```

### Competitive Intelligence (P1)
```
GET    /api/v1/competitors                → List watch list
POST   /api/v1/competitors                → Add company to watch
GET    /api/v1/competitors/{id}/filings   → Competitor's recent patents
```

---

## AI/ML Components

### 1. Semantic Search (P0, Week 1–3)
- **Model:** Fine-tuned embeddings on patent abstracts + claims (Hugging Face / OpenAI)
- **Index:** PostgreSQL pgvector
- **Goal:** Achieve >85% relevant results (vs. 60% for Google Patents keyword search)
- **Evaluation:** Test on known prior art scenarios

### 2. Examiner Prediction (P0, Week 5–6)
- **Training Data:** USPTO PAIR (examination history, office actions, grants)
- **Model:** Lightweight LLM fine-tuned on claim patterns + technology area + examiner history
- **Output:** Allowance probability + top 3 suggested claim amendments
- **Accuracy Target:** >80% on test set

### 3. Claim Mapping (P0, Week 4)
- **Task:** Given user patent and prior art, auto-map which claims are anticipated
- **Method:** Semantic similarity between claim sentences + manual review rules
- **Output:** JSON mapping { user_claim_num → source_claim_nums }

### 4. Claim Chart Generation (P1, Week 9–10)
- **Input:** User patent + prior art list
- **Output:** Traditional claim chart (elements matrix)
- **Method:** LLM to extract claim elements, then fuzzy-match to prior art

---

## Non-Functional Requirements

### Performance
- Patent search: <1 sec response (embedding lookup)
- Prior art analysis: <10 sec (batch embedding + relevance ranking)
- Portfolio load: <2 sec (100 patents)

### Availability
- 99.5% uptime (SLA)
- Auto-backup every 6 hours
- Hot standby for database

### Security
- OAuth 2.0 login (Google, GitHub)
- Role-based access control (owner, attorney, paralegal)
- Encrypted storage for sensitive data (at-rest + in-transit)
- GDPR/CCPA compliance (data deletion on request)

### Data
- Backend tests: 70%+ coverage
- All data persisted to PostgreSQL
- Automated Alembic migrations for schema changes
- No mock data in production

### Frontend
- Responsive design (mobile, tablet, desktop)
- Tailwind CSS + shadcn/ui components
- Dark mode support
- Keyboard navigation (accessibility)

### Deployment
- Docker Compose for local dev + CI
- Helm chart for Kubernetes
- GitHub Actions CI/CD (run tests on every push)
- Zero-downtime deployments

---

## Success Metrics (v1.0 Demo Day)

| Metric | Target | Why |
|--------|--------|-----|
| **User Onboarding** | <2 min to first search | UX simplicity vs. incumbents |
| **Search Accuracy** | >85% relevant results | Core differentiation |
| **Time Saved** | 10x faster than manual (3 days → 2 hours) | Value proposition |
| **Retention** | 70%+ MRR in first 3 months | Product-market fit signal |
| **Pricing** | $500–$2k/mo (vs. $50k/mo incumbents) | Competitive advantage |

---

## Competitive Positioning

**vs. AnAqua:** Full-featured but expensive ($500k+/yr), enterprise-focused  
→ DClaw: Start with search + predictions, 100x cheaper, SME-focused

**vs. PatSnap:** Strong analytics, but steep learning curve  
→ DClaw: Simpler UX, faster onboarding, focus on in-house counsel

**vs. Google Patents:** Free but no AI, keyword-only search  
→ DClaw: Semantic search, predictions, docketing (all in one)

---

## Out of Scope (v1.0)

- Patent valuation estimates
- Auto-generated technical drawings
- Multimodal search (images, diagrams) — P2
- License marketplace
- Disclosure workflow (too enterprise, too slow to build)
- Integration with law firm case management systems (v2)

---

## Links & References

- [Gap Analysis](./GAP-ANALYSIS.md)
- [Feature Roadmap v1.2–v1.3](./PLAN-v1.3.md)
- [Backend Architecture](./backend/README.md)
- [Frontend Component Library](./frontend/README.md)
