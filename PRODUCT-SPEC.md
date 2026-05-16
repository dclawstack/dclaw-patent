# PRODUCT-SPEC: DClaw Patent

## Overview

**App Name:** DClaw Patent  
**Domain:** AI-Powered Patent Management & IP Portfolio Automation  
**Target User:** In-house IP teams (50-500 people), solo patent practitioners, small law firms  
**Market Opportunity:** $13.48B (2026) → $41.63B (2035)  
**Competitive Positioning:** Faster, cheaper AI claim drafting + legal automation vs. PatSnap/Anaqua

## Core Entities

### Patent
```
Patent
├── id: UUID (PK)
├── external_id: str (USPTO/EPO/WIPO reference, unique)
├── title: str (required)
├── abstract: str (optional)
├── claims: text (full claim text)
├── status: enum ["draft", "filed", "prosecution", "issued", "abandoned", "expired"] (default: "draft")
├── filing_date: date (optional)
├── publication_date: date (optional)
├── issue_date: date (optional)
├── expiration_date: date (optional)
├── inventor_ids: list[UUID] (FK → Inventor)
├── assignee: str (required)
├── technology_class: str (IPC/CPC code, optional)
├── created_at: datetime
├── updated_at: datetime
└── ai_generated: bool (default false)
```

### Docket (Deadline/Event Tracker)
```
Docket
├── id: UUID (PK)
├── patent_id: UUID (FK → Patent, ondelete=CASCADE)
├── event_type: enum ["office_action", "response_deadline", "maintenance_fee", "publication", "issuance", "appeal", "custom"] (required)
├── due_date: date (required)
├── jurisdiction: str (US, EP, WO, etc.)
├── description: str (optional)
├── status: enum ["pending", "completed", "overdue"] (default: "pending")
├── auto_generated: bool (default true)
├── created_at: datetime
└── updated_at: datetime
```

### InventionDisclosure
```
InventionDisclosure
├── id: UUID (PK)
├── title: str (required)
├── description: text (required)
├── inventor_id: UUID (FK → User)
├── summary: str (AI-generated abstract)
├── claims_draft: text (AI-generated claims)
├── status: enum ["draft", "submitted", "under_review", "approved", "filed"] (default: "draft")
├── ai_assist_used: bool (default false)
├── created_at: datetime
└── updated_at: datetime
```

### Inventor
```
Inventor
├── id: UUID (PK)
├── name: str (required)
├── email: str (unique, required)
├── organization: str (optional)
├── created_at: datetime
└── updated_at: datetime
```

## User Stories / Screens

### Screen 1: Dashboard
- Portfolio health: patents by status, upcoming deadlines (red/yellow/green)
- Active maintenance fees and filing deadlines (next 30/60/90 days)
- Docket overview: overdue items highlighted
- Quick actions: "New Invention Disclosure", "Upload Patent", "Search Prior Art"
- Technology distribution (IPC code breakdown)

### Screen 2: Patent Portfolio
- Table view: all patents with status, filing date, expiration date
- Search/filter by: title, status, technology class, jurisdiction
- Bulk actions: archive, export, mass-tag
- Add patent form (manual or USPTO/EPO lookup)

### Screen 3: Patent Detail
- Patent info (claims, abstract, drawings)
- Docket timeline (all deadlines and events)
- AI Copilot panel (similar patents, sentiment analysis)
- Inventor/assignee info
- Collaboration comments (internal notes, team discussion)

### Screen 4: Invention Disclosure (NEW)
- Structured intake form: invention title, description, drawings/attachments
- AI claim drafting: "Generate Claims Draft" button
- AI abstract generation
- Review workflow: submit for review, reviewer dashboard
- Auto-parse PDFs to populate fields

### Screen 5: Prior Art Search
- Search interface (keyword, technology class, patent number)
- Results table: title, relevance score, publication date, similarity badge
- Side-by-side claim comparison
- Save searches / set up alerts

### Screen 6: Docket Calendar
- Calendar view of all deadlines by jurisdiction
- List view with filters (office action, response, maintenance fee)
- Color-coded urgency (red: <30 days, yellow: 30-60, green: 60+)
- Mark complete / update status
- Auto-reminders (email, in-app)

## AI Features (Differentiator)

### P0 — MVP (v1.0)
- **AI Patent Copilot:** Search patent databases, summarize claims, identify similar patents ("Find patents like mine")
- **AI Claim Drafting:** Parse invention disclosure → auto-generate claims draft + abstract (10-min MVP)
- **Prior Art Similarity:** Embeddings-based search + relevance ranking (vs. exact keyword match)

### P1 — Differentiation (v1.1-1.2)
- **FTO (Freedom-to-Operate) Analysis:** Identify infringement risk, heatmap by product area
- **Competitive Patent Watch:** Alert on competitor filings in target technology areas
- **Claim Quality Scoring:** LLM evaluation of claim structure, scope, enforceability

### P2 — Enterprise (v1.3+)
- **Patent Valuation:** Estimate value based on citations, family size, licensing history
- **Technology Landscape:** Auto-clustering + white-space detection (bubble map)
- **Office Action Auto-Response:** AI drafts response to office actions (with human review)

## API Endpoints (v1.0)

### Patent Management
```
GET    /api/v1/patents              → List patents (with pagination, filters)
POST   /api/v1/patents              → Create patent (manual or import)
GET    /api/v1/patents/{id}         → Get patent detail
PUT    /api/v1/patents/{id}         → Update patent
DELETE /api/v1/patents/{id}         → Delete patent
POST   /api/v1/patents/import       → Bulk import from USPTO/EPO
```

### Docketing & Deadlines
```
GET    /api/v1/dockets              → List dockets (filtered by jurisdiction, urgency)
POST   /api/v1/dockets              → Create docket entry
PUT    /api/v1/dockets/{id}         → Update docket (mark complete, etc.)
DELETE /api/v1/dockets/{id}         → Delete docket
GET    /api/v1/dockets/overdue      → Get overdue items (red alerts)
POST   /api/v1/dockets/calculate    → Calculate deadlines by jurisdiction
```

### Invention Disclosure
```
GET    /api/v1/disclosures          → List invention disclosures
POST   /api/v1/disclosures          → Create new disclosure
GET    /api/v1/disclosures/{id}     → Get disclosure detail
PUT    /api/v1/disclosures/{id}     → Update disclosure
POST   /api/v1/disclosures/{id}/submit → Submit for review
POST   /api/v1/disclosures/{id}/file   → File as patent application
```

### AI Features
```
POST   /api/v1/ai/patent-search     → Search patents (keyword, embedding-based)
POST   /api/v1/ai/draft-claims      → Generate claims from disclosure
POST   /api/v1/ai/draft-abstract    → Generate abstract from description
POST   /api/v1/ai/similar-patents   → Find similar patents (embedding search)
POST   /api/v1/ai/fto-analysis      → Freedom-to-Operate analysis
GET    /api/v1/ai/patent-scores     → Get quality/enforceability scores
```

### Prior Art Search
```
POST   /api/v1/prior-art/search     → Search USPTO/EPO/WIPO databases
GET    /api/v1/prior-art/results/{id} → Get search result detail
POST   /api/v1/prior-art/compare    → Side-by-side claim comparison
```

### Dashboard & Analytics
```
GET    /api/v1/dashboard            → Dashboard stats (portfolio health, deadlines)
GET    /api/v1/analytics/by-status  → Patents by status breakdown
GET    /api/v1/analytics/by-class   → Patents by technology class (IPC)
GET    /api/v1/analytics/expiring   → Patents expiring in next N months
```

### Collaboration
```
POST   /api/v1/comments             → Add comment to patent/docket
GET    /api/v1/patents/{id}/comments → Get all comments
DELETE /api/v1/comments/{id}        → Delete comment
```

## Non-Functional Requirements

### Performance & Reliability
- Backend tests: 70%+ coverage
- API latency: <200ms for 95th percentile (patent search: <500ms due to DB lookups)
- Database: PostgreSQL with vector store extension (pgvector) for embeddings
- Caching: Redis for patent embeddings, search results
- Uptime: 99.5% SLA for free tier, 99.9% for paid

### Security & Compliance
- OAuth 2.0 / SAML for enterprise SSO
- Data encryption at rest (AES-256) and in transit (TLS 1.3)
- HIPAA/SOC 2 compliance roadmap for v1.3
- Audit logs: All patent/docket changes tracked with user + timestamp
- Rate limiting: 100 API calls/min for free tier, 1000/min for paid

### Frontend & UX
- Responsive design (mobile-friendly for docket checks)
- Tailwind + shadcn/ui components
- Accessibility: WCAG 2.1 AA compliance
- Dark mode support

### Integration & Scaling
- Docker: All services start with `docker compose up -d`
- Kubernetes-ready Helm charts
- Patent API integrations: USPTO PatentsView, EPO Open Patent Services, WIPO
- Async jobs for long-running AI tasks (Celery + Redis)
- No mock data — everything persisted to PostgreSQL + vector store

---
> **Document Owner:** Udai Kiran | **Email:** udai.kiran@oneconvergence.com
> **Last Modified:** 2026-05-16 | **Admin Tracking:** Active
