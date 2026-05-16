# DClaw Patent — v1.3 Comprehensive Roadmap

**Date:** 2026-05-16  
**Objective:** Ship Y Combinator-ready product with AI differentiation in 12 weeks  
**Target Metrics:** $10K+ MRR, 50%+ MoM growth, <$1K CAC

---

## Strategic Context

This roadmap reflects findings from **GAP-ANALYSIS-YC.md**. Key pivots from v1.2:

1. ✅ **Accelerate AI Claim Drafting** → P0 (not P1) — Ship in v1.0
2. ✅ **Add Legal Automation** → USPTO/EPO integration in docketing (not manual)
3. ✅ **Prioritize Freemium + Viral Growth** → Competitive watch as free feature
4. ✅ **Shift to 12-week YC timeline** → MVP in Week 4, public beta in Week 8

---

## Executive Summary of Feature Tiers

### P0 — Must Ship v1.0 (Weeks 1-4)
- Portfolio CRUD + search
- Docketing with deadline calculation (country-specific rules)
- **NEW:** AI Patent Copilot (basic search + summarize)
- **NEW:** AI Claim Drafting (disclosure → claims in 10 min)
- Prior Art Search (USPTO + EPO APIs)
- Dashboard (portfolio health, deadlines)
- **NEW:** Legal automation (auto-docket from USPTO/EPO responses)

### P1 — Must Ship v1.1-1.2 (Weeks 5-8)
- Real-time collaboration (comments, @mentions)
- Freedom-to-Operate (FTO) analysis + heatmap
- Competitive Patent Watch (alerts, free-tier feature for viral growth)
- Technology Landscape Mapping (visualization)
- Invention Disclosure Workflow (intake + review routing)
- Claim Quality Scoring (AI evaluation)

### P2 — v1.3+ (Weeks 9-12 and beyond)
- Patent Valuation (citations, licensing)
- Auto-Generated Patent Drawings
- Licensing Marketplace
- Advanced Analytics (ROI, cost of ownership)
- Mobile app (iOS/Android)

---

## Detailed 12-Week Roadmap

### **Phase 1: MVP Defensibility (Weeks 1-4)**

#### Week 1-2: Foundation + AI Copilot MVP

**Backend:**
- [ ] Patent CRUD API with full-text search
- [ ] Patent status enum + filtering (draft, filed, prosecution, issued, abandoned)
- [ ] Docketing table + deadline calculation engine (country-specific: US 12-month rule, EP 31-month rule, etc.)
- [ ] Vector store setup (PostgreSQL pgvector extension)
- [ ] Patent embedding generation (Claude or open-source BERT)
- [ ] Prior Art API integration: PatentsView (USPTO), EPO Open Patent Services
- [ ] `POST /api/v1/ai/patent-search` endpoint (simple keyword + embedding search)
- [ ] `POST /api/v1/ai/similar-patents` endpoint (find N most similar by embedding)
- [ ] Async job queue (Celery) for long-running AI tasks
- [ ] 70% test coverage: CRUD, search, deadline calculations

**Frontend:**
- [ ] Patent portfolio table (columns: title, status, filing date, expiration, actions)
- [ ] Patent detail view (claims, abstract, docket list, AI copilot panel on right)
- [ ] Dashboard: portfolio health cards, overdue dockets (red/yellow/green), upcoming deadlines
- [ ] Search interface: keyword + filter by status/jurisdiction/tech class
- [ ] AI Copilot panel: "Find Similar Patents" button, results sidebar
- [ ] Basic styling (Tailwind), no animations yet

**Deployment:**
- [ ] Docker: backend + frontend + postgres + redis
- [ ] GitHub Actions CI: run tests, type-check on every push
- [ ] Staging environment setup

**Success Criteria:**
- ✓ Can upload/view 10+ patents
- ✓ Search returns results in <1s
- ✓ Similar patents rank correctly (manual review)
- ✓ Deadline calculations correct for 3 jurisdictions
- ✓ Tests passing, 70%+ coverage

---

#### Week 2-3: AI Claim Drafting (P0 Priority)

**Backend:**
- [ ] Invention Disclosure schema: title, description, attachments, inventor info
- [ ] PDF parser (pypdf or pdfplumber) to extract text from uploaded PDFs
- [ ] Claude API integration for claim generation:
  - Prompt: "You are a patent claim drafter. Given this invention, generate independent and dependent claims."
  - Handle: 3 claim variants, temperature=0.3 for consistency
  - Human review layer: score each variant 1-5
- [ ] `POST /api/v1/ai/draft-claims` endpoint (returns 3 draft options)
- [ ] `POST /api/v1/ai/draft-abstract` endpoint (one-liner)
- [ ] Store drafts in DB with version history (user can compare versions)
- [ ] Review workflow: mark draft as "approved" or "rejected" with feedback
- [ ] Tests: claim generation quality (manual spot-check of 20 examples)

**Frontend:**
- [ ] "New Invention Disclosure" form: title, description, attachment (drag-drop)
- [ ] AI Claim Drafting panel: "Generate Claims" button → shows 3 variants
- [ ] Claim editor: can copy, edit, rate each variant
- [ ] Abstract generator: one-button, shows result
- [ ] "Submit for Review" button → marks workflow as "under_review"
- [ ] Success animation: "Claims drafted in 2 min! 🎉"

**Quality Assurance:**
- [ ] Manual review: draft 10 real patents, rate claim quality
- [ ] Ensure no hallucinations (claims must reference disclosure)
- [ ] A/B test: users prefer variant A, B, or C?

**Success Criteria:**
- ✓ Generate claims in <2 min (most under 30s)
- ✓ Claims are coherent and reference disclosure
- ✓ Users can edit/iterate on draft
- ✓ <5% hallucination rate (measured manually)

---

#### Week 3-4: Legal Automation + Docketing Refinement

**Backend:**
- [ ] USPTO/EPO integration: webhook listeners for office actions, responses, maintenance fees
- [ ] Auto-parse office action documents (PDF) → extract dates, requirements, deadlines
- [ ] Auto-calculate response deadline (country-specific rules)
- [ ] Auto-create docket entries: "Office Action Response Required" + due date
- [ ] Deadline notifications: email 30/14/7 days before due
- [ ] Bulk docket operations: export to CSV, print calendar
- [ ] Maintenance fee schedule: auto-populate based on patent issue date + jurisdiction
- [ ] Tests: deadline calculation for 5+ jurisdictions (US, EU, JP, CN, IN)

**Frontend:**
- [ ] Docket calendar view: month/week view, color-coded urgency
- [ ] Docket list: filter by jurisdiction, type (office action, maintenance, publication)
- [ ] Mark complete: checkbox + timestamp
- [ ] Docket detail: show auto-generated fields + manual override option
- [ ] Export: CSV for Excel, iCal for calendar apps
- [ ] Alerts: in-app notification + email for upcoming deadlines

**Deployment:**
- [ ] Load test: 1000 patents, 5000 dockets, search <500ms
- [ ] Error handling: USPTO API rate limits, retries with exponential backoff

**Success Criteria:**
- ✓ Auto-docket 100+ office actions without manual entry
- ✓ Deadline calculations 100% accurate for 3 jurisdictions
- ✓ Users trust automated dates (survey: "Do you verify our deadlines?")
- ✓ <5% false positives in auto-parsing

---

#### Week 4: MVP Polish + Internal Dogfood

**Backend:**
- [ ] Fix bugs from internal testing
- [ ] Add missing error handling (API validation, edge cases)
- [ ] Performance: optimize slow queries (patent search should be <200ms)
- [ ] Security: input validation, SQL injection tests

**Frontend:**
- [ ] Responsive design: works on mobile (docket checks on mobile)
- [ ] Accessibility: keyboard navigation, screen reader support
- [ ] Bug fixes from dogfood testing
- [ ] Dark mode toggle (nice-to-have)

**Documentation:**
- [ ] API docs (OpenAPI/Swagger)
- [ ] Setup guide for deployment
- [ ] Internal runbook for bug reports

**Internal Dogfood:**
- [ ] 5 internal users test for 1 week
- [ ] Measure: time to upload patent, time to draft claims, time to review dockets
- [ ] Collect NPS / feedback
- [ ] Fix critical issues only; defer nice-to-haves to v1.1

**Success Criteria:**
- ✓ NPS >50 from internal users
- ✓ Zero critical bugs
- ✓ "I'd use this for real" from 80%+ of testers
- ✓ Deployment: 1-click `docker compose up`

---

### **Phase 2: Competitive Differentiation (Weeks 5-8)**

#### Week 5: Freemium Model + Competitive Watch (Launch Feature)

**Why Free Competitive Watch:**
- Freemium ≈ viral loop (users invite teammates to monitor competitors)
- Patent Watch (YC company) gets $20K+/year; we offer for free → acquisition wedge
- Solves "FOMO for patent teams": scared of missing competitor moves

**Backend:**
- [ ] Competitor Watch schema: watchlist (list of competitor names/assignees)
- [ ] Scheduled job (daily): query USPTO/EPO for new patents by competitors
- [ ] Alert generation: "Competitor X filed Y patents in Z area this week"
- [ ] Free tier: up to 3 competitor watchlists, 1 alert per week (batched)
- [ ] Paid tier: unlimited watchlists, real-time alerts, historical analysis
- [ ] `POST /api/v1/watch/competitor` endpoint
- [ ] `GET /api/v1/watch/alerts` endpoint

**Frontend:**
- [ ] "Add Competitor" modal: search USPTO by assignee name
- [ ] Watchlist dashboard: "Your competitors filed 5 new patents this week"
- [ ] Expandable alerts: see patents, technology areas, assignees
- [ ] Share alert: "Check this out 👉 [link]" → drives freemium signups

**Pricing Model:**
- [ ] Free tier: 5 patents, 3 watchlists, 1 docket, 1 alert/week → $0
- [ ] Pro tier: unlimited patents, 10 watchlists, alerts every 6h → $49/mo
- [ ] Enterprise: custom, contact sales → $500+/mo
- [ ] Implement stripe.com integration (charge cards)

**Launch Metrics:**
- [ ] 50+ signups via competitive watch feature (viral loop)
- [ ] NPS >60 from free users
- [ ] 10%+ free→paid conversion (hope for 20%)

**Success Criteria:**
- ✓ Free users can set up competitor watch in <2 min
- ✓ Alerts arrive daily (no missed competitors)
- ✓ <1% false positive rate (e.g., different company with same name)
- ✓ 10+ free-tier users actively using

---

#### Week 5-6: Real-Time Collaboration

**Context:** Anaqua's strength is team collaboration. We need it for enterprise sales.

**Backend:**
- [ ] Comments schema: patent_id, user_id, text, created_at, resolved (bool)
- [ ] `POST /api/v1/comments` endpoint (create comment)
- [ ] `GET /api/v1/patents/{id}/comments` endpoint (get all)
- [ ] WebSocket support (optional; can defer to v1.2)
- [ ] @mention parsing: "Check with @legal_team on this claim"
- [ ] Notifications: email when mentioned
- [ ] Audit log: track all changes (patent edit, docket update, comment)

**Frontend:**
- [ ] Comments panel on patent detail (right sidebar)
- [ ] Typeahead @mention: search team members
- [ ] "Resolve" button: mark comment as resolved (hide by default)
- [ ] Activity feed: "Alice edited claims, Bob commented" → shows history
- [ ] Thread view: replies to comments (sub-thread)

**Enterprise Features (v1.2):**
- [ ] Roles: Admin, Attorney, Reviewer, Inventor (read-only)
- [ ] Permissions: Inventor can only see own disclosures
- [ ] Review workflow: Disclosure → Attorney review → approved/rejected + feedback

**Success Criteria:**
- ✓ Team of 5 can collaborate on patent without leaving app
- ✓ No lost comments (all persisted)
- ✓ Mention notifications arrive <1 min

---

#### Week 6-7: Freedom-to-Operate (FTO) Analysis

**Why P1 (not P0):** Solves "Can we launch this product?" → used for launch planning

**Backend:**
- [ ] FTO search: product description → finds potentially blocking patents
- [ ] Infringement risk scoring: claims overlap + patent strength → risk score 1-10
- [ ] Generate FTO report: "2 medium-risk patents (score 6-8), 0 high-risk"
- [ ] Heatmap data: product areas × patent risks (visualization on frontend)
- [ ] `POST /api/v1/ai/fto-analysis` endpoint
- [ ] Comparison: our product claims vs. blocking patent claims

**Frontend:**
- [ ] FTO wizard: "Upload your product spec" → gets back risk assessment
- [ ] Heatmap: product areas (Y-axis) × risk level (color: green/yellow/red)
- [ ] Patent cards: showing blocking patents + overlap visualization
- [ ] Recommendation: "Redesign module X to avoid these claims" (if applicable)
- [ ] Export: FTO report (PDF) for legal review

**Quality Assurance:**
- [ ] Manual review: spot-check 10 FTO reports
- [ ] Compare vs. human patent attorney (if possible)
- [ ] Score accuracy: does a "high-risk" patent actually look risky?

**Success Criteria:**
- ✓ FTO analysis completes in <5 min
- ✓ Risk scores align with manual review (Spearman correlation >0.7)
- ✓ Users find results actionable ("This risk is real" 80%+)

---

#### Week 7-8: Technology Landscape + Disclosure Workflow

**Week 7: Technology Landscape Mapping**

**What it is:** Bubble map or treemap of patent landscape → find white spaces

**Backend:**
- [ ] Patent clustering: group by technology class (IPC codes)
- [ ] Competitive analysis: which assignees own which tech areas
- [ ] White-space detection: areas with <10 patents (less crowded)
- [ ] Trend analysis: which tech areas growing year-over-year
- [ ] `GET /api/v1/analytics/landscape` endpoint (returns graph data)

**Frontend:**
- [ ] Bubble chart: bubble size = # of patents, color = assignee, X/Y = tech class
- [ ] Interactive: hover → see top patents, click → go to patent detail
- [ ] Toggle view: bubble → treemap → force-directed graph
- [ ] Filters: date range, jurisdiction, assignee
- [ ] Insight: "Quantum computing (IPC H03F) has 200 patents; AI/ML has 5000" (crowded)

**Success Criteria:**
- ✓ Visualization loads in <2s
- ✓ Users can identify white-space areas (manual survey: "Did you learn something new? Y/N")
- ✓ Data is current (updated daily)

---

**Week 8: Invention Disclosure Workflow**

**What it is:** Structured intake for inventors → review routing → file as patent

**Backend:**
- [ ] Disclosure form builder: schema + validation
- [ ] Review routing: assign disclosure to attorney
- [ ] Workflow states: draft → submitted → under_review → approved → filed
- [ ] Comments in review process: attorney can add feedback
- [ ] File button: submit to USPTO (if integrated; else just mark as ready)
- [ ] `POST /api/v1/disclosures/{id}/submit` endpoint
- [ ] `POST /api/v1/disclosures/{id}/file` endpoint (USPTO integration)

**Frontend:**
- [ ] Disclosure form: wizard (step 1: basics, step 2: description, step 3: drawings)
- [ ] AI pre-fill: "Let us draft claims for you" (uses claims drafting AI)
- [ ] Submit flow: review checklist, then submit
- [ ] Review dashboard (for attorneys): queue of pending disclosures, comment interface
- [ ] Approval flow: approve/reject with feedback
- [ ] File button: ready to submit to USPTO (confirmation dialog)

**Integration (Deferred to v1.2):**
- [ ] USPTO ePAVE integration (automated filing)
- [ ] EPO filing (need legal review)

**Success Criteria:**
- ✓ Inventor can file disclosure in <10 min
- ✓ Attorney can review + approve in <5 min
- ✓ Feedback loop: inventor gets notification + can revise
- ✓ <2% disclosure abandonment (most get filed)

---

### **Phase 3: Scale & Enterprise (Weeks 9-12+)**

#### Week 9: Claim Quality Scoring (AI Evaluation)

**Backend:**
- [ ] LLM evaluation: score claim set on 5 dimensions
  1. Clarity: are claims written clearly? (1-5)
  2. Scope: are independent claims broad enough? (1-5)
  3. Validity: will these survive USPTO / EPO review? (1-5)
  4. Enforceability: will courts enforce these? (1-5)
  5. Novelty: how novel vs. prior art? (1-5)
- [ ] Return: overall score (1-5) + detailed feedback per dimension
- [ ] `POST /api/v1/ai/score-claims` endpoint

**Frontend:**
- [ ] Claims detail page: "Quality Score: 4.2/5"
- [ ] Breakdown: show radar chart of 5 dimensions
- [ ] Feedback: "Claims are clear but maybe too narrow. Consider adding dependent claims for breadth."
- [ ] Action: "Improve Score" button → AI suggestions for revision

**Success Criteria:**
- ✓ Scores correlate with examiner acceptance (measure in v1.2)
- ✓ Feedback is actionable ("too broad" → users understand why)

---

#### Week 10: Enterprise Features (Roles, Permissions, Audit)

**Backend:**
- [ ] User roles: Admin, Attorney, Inventor, Viewer
- [ ] Permission matrix: who can see/edit/approve what?
- [ ] Audit log: all changes (patent edit, docket update, comment) with user + timestamp
- [ ] Workspace: separate orgs (law firm A ≠ law firm B)
- [ ] Invitation system: admin invites users, auto-signup

**Frontend:**
- [ ] Admin settings: manage users, roles, audit log
- [ ] Role-based UI: Inventor doesn't see billing, doesn't see other's disclosures
- [ ] Audit trail: click on patent → see "Edit history" (who changed what, when)

**Success Criteria:**
- ✓ Law firm with 50 users can manage permissions safely
- ✓ Compliance team can export audit log for SOC 2 audit

---

#### Week 11: Analytics & ROI Dashboard

**Backend:**
- [ ] KPIs: # patents, total value (est.), maintenance costs, time saved (vs. manual)
- [ ] Trends: growth of portfolio over time
- [ ] Cost analysis: maintenance fee forecasting, cost per patent (annual)
- [ ] Efficiency: "You saved X hours this month via AI drafting"

**Frontend:**
- [ ] Executive dashboard: portfolio value, maintenance spend, team utilization
- [ ] Drill-down: which patents are most valuable? (by citations, licensing)
- [ ] ROI calculator: "DClaw paid for itself in X months"
- [ ] Benchmark: "Your portfolio is X% the size of competitor Y"

**Success Criteria:**
- ✓ CFO can use this to justify IP budget to board
- ✓ "DClaw saved us $50K this year" (measurable)

---

#### Week 12: Polish, Performance, Launch Prep

**Backend:**
- [ ] Load testing: 10K patents, 100K dockets, <500ms searches
- [ ] Security audit: penetration test, OWASP Top 10 scan
- [ ] Database optimization: indexes, query tuning, connection pooling
- [ ] Error handling: all edge cases covered
- [ ] Monitoring: error rates, API latency, database health

**Frontend:**
- [ ] Performance: Lighthouse >90, Core Web Vitals green
- [ ] Accessibility: WCAG 2.1 AA compliance
- [ ] Mobile: full responsive design, touch-friendly
- [ ] E2E tests: critical user flows (upload patent → draft claims → review docket)

**Documentation:**
- [ ] User guide: video tutorials for each feature
- [ ] API docs: OpenAPI v3.0
- [ ] Admin guide: setup, user management, billing
- [ ] Changelog: what's new in v1.0

**Launch Marketing:**
- [ ] Press release: "DClaw Patent: AI-Powered Patent Management"
- [ ] Product Hunt post: tagline, screenshots, demo video
- [ ] Beta email: notify 100 waitlist users
- [ ] Social: Twitter, LinkedIn, AngelList
- [ ] Pricing page: clear value prop, pricing tiers, FAQ

**Success Criteria:**
- ✓ 100+ beta signups in week 1
- ✓ NPS >70 from beta users
- ✓ 10+ paid conversions in month 1
- ✓ Website: clear, fast, converts

---

## Success Metrics by Phase

### Phase 1 (Week 4): MVP Validation
- ✅ Internal NPS >50
- ✅ Can draft claims in <2 min
- ✅ 70%+ test coverage
- ✅ Zero critical bugs

### Phase 2 (Week 8): Market Traction
- ✅ 50+ beta signups (freemium)
- ✅ $2K+ MRR from early paid users
- ✅ 50%+ MoM growth
- ✅ NPS >60

### Phase 3 (Week 12): Series A Readiness
- ✅ $10K+ MRR
- ✅ <$1K CAC (from freemium virality)
- ✅ 3+ enterprise pilots ($5K+/mo each)
- ✅ Public case study: "Law firm X saved Y hours with DClaw"

---

## Dependencies & Risks

### Critical Dependencies

| Task | Depends On | Risk Level |
|------|-----------|-----------|
| AI Claim Drafting | Claude API access, good prompts | 🟡 Medium (API reliability) |
| USPTO/EPO Integration | Patent office APIs stable | 🟡 Medium (rate limits, docs) |
| Legal Automation | Office action parsing (OCR) | 🔴 High (complex documents) |
| Competitive Watch | USPTO/EPO data freshness | 🟡 Medium (lag: 2-4 weeks) |
| FTO Analysis | Claims overlap detection | 🔴 High (legal accuracy critical) |

### Risk Mitigations

| Risk | Mitigation |
|------|-----------|
| Claude API hallucinations in claims | Human review layer, version history, compare with disclosure |
| USPTO rate limits / unavailability | Local patent cache, async queuing, fallback to static data |
| Office action parsing failures | Start with simple patterns, add OCR later, manual override |
| Legal liability (FTO accuracy) | Disclaimer: "For informational purposes; consult patent attorney", E&O insurance |
| Patent data licensing cost | Use free APIs (PatentView, EPO); negotiate enterprise deals later |

---

## Resource Allocation

### Recommended Team
- 1 Backend Lead (FastAPI, PostgreSQL, vector embeddings)
- 1 Full-Stack Engineer (Next.js, API integration, UI)
- 1 AI/ML Engineer (prompt engineering, embeddings, LLM fine-tuning)
- 1 QA / DevOps (testing, CI/CD, deployment, monitoring)
- (Optional) 1 Patent Domain Expert (contractor; advise on legal accuracy)

### Estimated Timeline (Solo/Pair)
- If 1 engineer: 16 weeks (overscoped)
- If 2 engineers: 10-12 weeks (recommended)
- If 4 engineers: 6-8 weeks (aggressive but doable)

---

## Appendix: Key Files to Create/Update

| File | Purpose | Priority |
|------|---------|----------|
| `backend/app/models/patent.py` | Patent ORM schema | P0 |
| `backend/app/models/docket.py` | Docket/deadline schema | P0 |
| `backend/app/models/disclosure.py` | Invention disclosure schema | P0 |
| `backend/app/services/patent_ai.py` | AI copilot + claim drafting | P0 |
| `backend/app/services/prior_art.py` | Patent search integration | P0 |
| `backend/app/services/docketing.py` | Deadline calculation engine | P0 |
| `backend/app/api/v1/patents.py` | Patent CRUD API | P0 |
| `backend/app/api/v1/ai.py` | AI feature endpoints | P0 |
| `frontend/src/app/portfolio/page.tsx` | Patent list view | P0 |
| `frontend/src/app/patent/[id]/page.tsx` | Patent detail + copilot | P0 |
| `frontend/src/app/dockets/page.tsx` | Docket calendar/list | P0 |
| `frontend/src/app/disclosure/page.tsx` | Invention disclosure form | P1 |
| `frontend/src/app/fto/page.tsx` | FTO analysis UI | P1 |
| `frontend/src/app/watch/page.tsx` | Competitive watch | P1 |
| `frontend/src/components/ai-copilot.tsx` | Reusable copilot component | P0 |
| `.github/workflows/ci.yml` | Run tests on every push | P0 |
| `docker-compose.yml` | Local dev environment | P0 |
| `helm/Chart.yaml` | Kubernetes deployment | P1 |

---

## Conclusion

This roadmap balances **speed** (ship MVP in 4 weeks) with **defensibility** (AI differentiation, legal automation). Success depends on:

1. **Nailing AI claim drafting** — if users love it, viral growth via competitors
2. **Executing legal automation** — saves real time, earns trust
3. **Freemium competitive watch** — acquisition wedge, network effects
4. **Staying laser-focused** — no feature creep; defer polish to v1.2

**YC Thesis:** "AI is making patent work 10x faster. We're building the platform."

---

*Last updated: 2026-05-16*

---
> **Document Owner:** Udai Kiran | **Email:** udai.kiran@oneconvergence.com
> **Last Modified:** 2026-05-16 | **Admin Tracking:** Active
