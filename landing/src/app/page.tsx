"use client"

import { useState, useEffect } from "react"
import {
  Brain,
  Search,
  CalendarDays,
  ShieldCheck,
  Zap,
  FileText,
  BarChart3,
  Globe,
  LayoutDashboard,
  ChevronRight,
  Sparkles,
  Clock,
  Lock,
  Upload,
  MessageSquare,
  Lightbulb,
  TrendingUp,
  Users,
  Layers,
  ClipboardList,
  Hash,
  CheckCircle2,
  ArrowRight,
  Menu,
  X,
} from "lucide-react"
import { Button } from "@/components/ui/button"

/* ─── Reusable Feature Card ─── */
function FeatureCard({
  icon: Icon,
  title,
  description,
  tags,
}: {
  icon: React.ElementType
  title: string
  description: string
  tags: string[]
}) {
  return (
    <div className="group relative overflow-hidden rounded-2xl border border-slate-200 bg-white p-6 shadow-sm transition-all duration-300 hover:-translate-y-1 hover:shadow-xl hover:border-blue-200">
      <div className="mb-4 flex h-12 w-12 items-center justify-center rounded-xl bg-gradient-to-br from-blue-50 to-indigo-100 text-blue-600 transition-transform duration-300 group-hover:scale-110">
        <Icon className="h-6 w-6" />
      </div>
      <h3 className="mb-2 text-lg font-semibold text-slate-900">{title}</h3>
      <p className="mb-4 text-sm leading-relaxed text-slate-600">{description}</p>
      <div className="flex flex-wrap gap-2">
        {tags.map((t) => (
          <span
            key={t}
            className="rounded-full bg-slate-100 px-2.5 py-0.5 text-xs font-medium text-slate-700"
          >
            {t}
          </span>
        ))}
      </div>
    </div>
  )
}

/* ─── Step Item ─── */
function Step({
  number,
  title,
  description,
}: {
  number: string
  title: string
  description: string
}) {
  return (
    <div className="flex gap-4">
      <div className="flex h-10 w-10 shrink-0 items-center justify-center rounded-full bg-blue-600 text-sm font-bold text-white">
        {number}
      </div>
      <div>
        <h4 className="font-semibold text-slate-900">{title}</h4>
        <p className="text-sm text-slate-600">{description}</p>
      </div>
    </div>
  )
}

/* ─── Stat Card ─── */
function StatCard({ number, label }: { number: string; label: string }) {
  return (
    <div className="text-center">
      <div className="text-3xl font-bold text-blue-600 md:text-4xl">{number}</div>
      <div className="mt-1 text-sm text-slate-500">{label}</div>
    </div>
  )
}

/* ─── Main Landing Page ─── */
export default function LandingPage() {
  const [mobileOpen, setMobileOpen] = useState(false)
  const [scrolled, setScrolled] = useState(false)

  useEffect(() => {
    const onScroll = () => setScrolled(window.scrollY > 20)
    window.addEventListener("scroll", onScroll)
    return () => window.removeEventListener("scroll", onScroll)
  }, [])

  const scrollTo = (id: string) => {
    setMobileOpen(false)
    document.getElementById(id)?.scrollIntoView({ behavior: "smooth" })
  }

  return (
    <div className="min-h-screen bg-white">
      {/* ── Navigation ── */}
      <nav
        className={`fixed left-0 right-0 top-0 z-50 transition-all duration-300 ${
          scrolled
            ? "bg-white/80 shadow-sm backdrop-blur-md"
            : "bg-transparent"
        }`}
      >
        <div className="mx-auto flex max-w-7xl items-center justify-between px-4 py-4 md:px-6">
          <div className="flex items-center gap-2">
            <div className="flex h-9 w-9 items-center justify-center rounded-lg bg-blue-600 text-white">
              <Sparkles className="h-5 w-5" />
            </div>
            <span className="text-xl font-bold text-slate-900 tracking-tight">
              DClaw <span className="text-blue-600">Patent</span>
            </span>
          </div>

          {/* Desktop links */}
          <div className="hidden items-center gap-8 md:flex">
            {[
              ["Features", "features"],
              ["AI Engine", "ai-engine"],
              ["How It Works", "how-it-works"],
              ["Screens", "screens"],
              ["Security", "security"],
            ].map(([label, id]) => (
              <button
                key={id}
                onClick={() => scrollTo(id)}
                className="text-sm font-medium text-slate-600 transition-colors hover:text-blue-600"
              >
                {label}
              </button>
            ))}
          </div>

          <div className="hidden items-center gap-3 md:flex">
            <Button variant="ghost" size="sm">
              Sign In
            </Button>
            <Button size="sm">Get Started</Button>
          </div>

          {/* Mobile menu toggle */}
          <button
            className="md:hidden"
            onClick={() => setMobileOpen(!mobileOpen)}
          >
            {mobileOpen ? (
              <X className="h-6 w-6 text-slate-700" />
            ) : (
              <Menu className="h-6 w-6 text-slate-700" />
            )}
          </button>
        </div>

        {/* Mobile nav */}
        {mobileOpen && (
          <div className="border-t border-slate-100 bg-white px-4 pb-4 md:hidden">
            {[
              ["Features", "features"],
              ["AI Engine", "ai-engine"],
              ["How It Works", "how-it-works"],
              ["Screens", "screens"],
              ["Security", "security"],
            ].map(([label, id]) => (
              <button
                key={id}
                onClick={() => scrollTo(id)}
                className="block w-full py-3 text-left text-sm font-medium text-slate-700"
              >
                {label}
              </button>
            ))}
            <div className="mt-2 flex flex-col gap-2 border-t border-slate-100 pt-3">
              <Button variant="outline" className="w-full">
                Sign In
              </Button>
              <Button className="w-full">Get Started</Button>
            </div>
          </div>
        )}
      </nav>

      {/* ════════════════════════════════════════════
          HERO SECTION
          ════════════════════════════════════════════ */}
      <section className="relative overflow-hidden bg-gradient-to-br from-slate-50 via-white to-blue-50 pt-32 pb-20 md:pt-44 md:pb-32">
        {/* Decorative blobs */}
        <div className="pointer-events-none absolute -top-20 -right-20 h-96 w-96 rounded-full bg-blue-100/50 blur-3xl" />
        <div className="pointer-events-none absolute -bottom-20 -left-20 h-96 w-96 rounded-full bg-indigo-100/40 blur-3xl" />

        <div className="relative mx-auto max-w-7xl px-4 md:px-6">
          <div className="mx-auto max-w-4xl text-center">
            {/* Badge */}
            <div className="mb-6 inline-flex items-center gap-2 rounded-full border border-blue-200 bg-blue-50 px-4 py-1.5 text-sm font-medium text-blue-700 animate-fade-in">
              <Sparkles className="h-4 w-4" />
              AI-Powered Patent Management Platform
            </div>

            <h1 className="text-4xl font-extrabold tracking-tight text-slate-900 md:text-6xl lg:text-7xl animate-fade-up">
              Draft. Search. Track. <br />
              <span className="bg-gradient-to-r from-blue-600 to-indigo-600 bg-clip-text text-transparent">
                Protect Smarter.
              </span>
            </h1>

            <p className="mx-auto mt-6 max-w-2xl text-lg leading-relaxed text-slate-600 md:text-xl animate-fade-up [animation-delay:0.1s]">
              DClaw Patent is an AI-driven patent management and IP portfolio
              automation platform. Draft claims in minutes, search prior art with
              embeddings, track deadlines across jurisdictions, and manage your
              entire patent portfolio from a single dashboard.
            </p>

            <div className="mt-8 flex flex-col items-center justify-center gap-3 sm:flex-row animate-fade-up [animation-delay:0.2s]">
              <Button size="lg" className="gap-2 text-base px-8">
                Start Free Trial
                <ArrowRight className="h-4 w-4" />
              </Button>
              <Button variant="outline" size="lg" className="text-base px-8">
                View Demo
              </Button>
            </div>

            {/* Stats */}
            <div className="mx-auto mt-16 grid max-w-3xl grid-cols-2 gap-8 border-t border-slate-200 pt-8 md:grid-cols-4 animate-fade-up [animation-delay:0.3s]">
              <StatCard number="10min" label="To draft claims" />
              <StatCard number="99.5%" label="Uptime SLA" />
              <StatCard number="3" label="Patent offices" />
              <StatCard number="$13.4B" label="Market 2026" />
            </div>
          </div>
        </div>
      </section>

      {/* ════════════════════════════════════════════
          FEATURES GRID
          ════════════════════════════════════════════ */}
      <section id="features" className="py-20 md:py-28">
        <div className="mx-auto max-w-7xl px-4 md:px-6">
          <div className="mx-auto mb-16 max-w-2xl text-center">
            <h2 className="text-3xl font-bold tracking-tight text-slate-900 md:text-4xl">
              Everything You Need for IP Management
            </h2>
            <p className="mt-4 text-slate-600">
              From invention disclosure to patent grant — a complete end-to-end
              platform powered by AI.
            </p>
          </div>

          <div className="grid gap-6 sm:grid-cols-2 lg:grid-cols-3">
            <FeatureCard
              icon={Brain}
              title="AI Patent Copilot"
              description="Ask natural-language questions like “Find patents related to quantum error correction.” AI searches millions of patents, summarizes claims, and ranks results by relevance using vector embeddings."
              tags={["RAG Search", "Embeddings", "Claim Summaries"]}
            />
            <FeatureCard
              icon={FileText}
              title="AI Claim Drafting"
              description="Paste an invention disclosure and get a professionally structured claims draft + abstract in under 10 minutes. The LLM understands patent-specific language and suggests dependent claims automatically."
              tags={["LLM Generation", "Dependent Claims", "10-min MVP"]}
            />
            <FeatureCard
              icon={Search}
              title="Prior Art Search"
              description="Search USPTO, EPO, and WIPO databases with AI-powered relevance ranking. Side-by-side claim comparison, similarity badges, and saved search alerts keep you ahead of the competition."
              tags={["USPTO/EPO/WIPO", "Relevance Scores", "Alerts"]}
            />
            <FeatureCard
              icon={CalendarDays}
              title="Smart Docketing"
              description="Track filing deadlines, office actions, response windows, and maintenance fees across jurisdictions. Auto-calculated dates with color-coded urgency alerts — red for overdue, yellow for approaching."
              tags={["Auto-Calculation", "Multi-Jurisdiction", "Reminders"]}
            />
            <FeatureCard
              icon={LayoutDashboard}
              title="Portfolio Dashboard"
              description="A visual command center for your entire IP portfolio. Status breakdowns, technology clusters by IPC/CPC codes, geographic coverage maps, upcoming deadlines, and spend analysis — all in one view."
              tags={["Status Map", "Tech Clusters", "Spend Analysis"]}
            />
            <FeatureCard
              icon={Lightbulb}
              title="Invention Disclosure Workflow"
              description="Structured intake forms guide inventors through submission. AI auto-parses PDFs, generates abstracts and claims drafts, and routes disclosures to reviewers for approval before filing."
              tags={["PDF Parsing", "Review Workflow", "AI Assist"]}
            />
            <FeatureCard
              icon={BarChart3}
              title="Technology Landscape Mapping"
              description="Visualize patent landscapes by technology area. Identify white spaces, spot competitor activity, and discover collaboration opportunities with interactive bubble and treemap views."
              tags={["Clustering", "White-Space Detection", "Competitors"]}
            />
            <FeatureCard
              icon={ShieldCheck}
              title="Freedom-to-Operate (FTO) Analysis"
              description="Systematic FTO searches identify infringement risks before product launch. AI generates risk heatmaps by product area and flags blocking patents with claim overlap analysis."
              tags={["Risk Heatmap", "Claim Overlap", "Pre-Launch"]}
            />
            <FeatureCard
              icon={TrendingUp}
              title="Competitive Intelligence"
              description="Watch competitor filings in real time. Set alerts for new publications in your technology areas and view trend dashboards showing who is filing what, where, and when."
              tags={["Real-Time Alerts", "Trend Dashboards", "Watch Lists"]}
            />
            <FeatureCard
              icon={Zap}
              title="AI Patent Valuation"
              description="Estimate patent value based on citation count, family size, licensing history, and market data. Compare against industry benchmarks and prioritize renewals with data-backed ROI."
              tags={["Citation Analysis", "Family Size", "ROI Scoring"]}
            />
            <FeatureCard
              icon={MessageSquare}
              title="Team Collaboration"
              description="Add comments, annotations, and internal notes directly on patents and docket entries. Tag team members, thread discussions, and maintain a complete audit trail of every decision."
              tags={["Comments", "Mentions", "Audit Trail"]}
            />
            <FeatureCard
              icon={Globe}
              title="Multi-Jurisdiction Support"
              description="Manage patents across US, Europe, and WIPO systems. Jurisdiction-specific deadline rules, form templates, and filing requirements are built in and auto-updated."
              tags={["US/EU/WO", "Auto-Rules", "Form Templates"]}
            />
          </div>
        </div>
      </section>

      {/* ════════════════════════════════════════════
          AI ENGINE DEEP DIVE
          ════════════════════════════════════════════ */}
      <section
        id="ai-engine"
        className="relative overflow-hidden bg-slate-900 py-20 text-white md:py-28"
      >
        <div className="pointer-events-none absolute inset-0 opacity-[0.04]" style={{
          backgroundImage: `radial-gradient(circle at 1px 1px, white 1px, transparent 0)`,
          backgroundSize: '32px 32px'
        }} />
        <div className="relative mx-auto max-w-7xl px-4 md:px-6">
          <div className="mb-16 text-center">
            <div className="mb-3 inline-flex items-center gap-2 rounded-full border border-blue-500/30 bg-blue-500/10 px-3 py-1 text-xs font-medium text-blue-300">
              <Sparkles className="h-3.5 w-3.5" />
              The AI Engine
            </div>
            <h2 className="text-3xl font-bold md:text-4xl">
              How Our AI Works
            </h2>
            <p className="mx-auto mt-4 max-w-2xl text-slate-400">
              Every AI feature is built on a modern ML stack with patent-specific
              fine-tuning, vector search, and RAG pipelines.
            </p>
          </div>

          <div className="grid gap-8 md:grid-cols-3">
            {[
              {
                icon: Hash,
                title: "Vector Embeddings (pgvector)",
                desc: "Every patent is converted into a high-dimensional embedding using fine-tuned sentence transformers. Stored in PostgreSQL with the pgvector extension for fast similarity search.",
              },
              {
                icon: Layers,
                title: "RAG Pipeline",
                desc: "Retrieval-Augmented Generation fetches the most relevant patent documents from the vector store, then feeds them into an LLM to generate accurate, grounded summaries and claims.",
              },
              {
                icon: ClipboardList,
                title: "Patent-Specific Prompting",
                desc: "Our LLM prompts are engineered for patent law syntax — independent/dependent claim structures, prior art citations, IPC/CPC codes, and jurisdiction-specific language.",
              },
            ].map((item, i) => (
              <div
                key={i}
                className="rounded-2xl border border-slate-700 bg-slate-800/50 p-6 backdrop-blur-sm"
              >
                <div className="mb-4 flex h-12 w-12 items-center justify-center rounded-xl bg-blue-500/10 text-blue-400">
                  <item.icon className="h-6 w-6" />
                </div>
                <h3 className="mb-2 text-lg font-semibold">{item.title}</h3>
                <p className="text-sm leading-relaxed text-slate-400">
                  {item.desc}
                </p>
              </div>
            ))}
          </div>

          {/* Latency/Performance bar */}
          <div className="mx-auto mt-12 grid max-w-4xl grid-cols-1 gap-4 rounded-2xl border border-slate-700 bg-slate-800/50 p-6 md:grid-cols-3">
            {[
              ["Patent Search", "< 200ms", "p95 latency"],
              ["Claim Draft", "< 10 min", "full generation"],
              ["Embedding Update", "< 500ms", "per patent"],
            ].map(([a, b, c]) => (
              <div key={a} className="text-center">
                <div className="text-2xl font-bold text-blue-400">{b}</div>
                <div className="mt-1 text-sm font-medium text-slate-300">
                  {a}
                </div>
                <div className="text-xs text-slate-500">{c}</div>
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* ════════════════════════════════════════════
          HOW IT WORKS
          ════════════════════════════════════════════ */}
      <section id="how-it-works" className="py-20 md:py-28 bg-slate-50">
        <div className="mx-auto max-w-7xl px-4 md:px-6">
          <div className="mb-16 text-center">
            <h2 className="text-3xl font-bold text-slate-900 md:text-4xl">
              From Invention to Grant — Simplified
            </h2>
            <p className="mx-auto mt-4 max-w-2xl text-slate-600">
              DClaw Patent streamlines the entire patent lifecycle with AI at
              every step.
            </p>
          </div>

          <div className="mx-auto grid max-w-3xl gap-8">
            {[
              {
                num: "1",
                title: "Submit Invention Disclosure",
                desc: "Inventors fill a structured form or upload a PDF. AI auto-parses documents, extracts key fields, and generates a preliminary abstract.",
              },
              {
                num: "2",
                title: "AI Drafts Claims & Abstract",
                desc: "Click “Generate Claims Draft” and get a professionally structured independent + dependent claims set in under 10 minutes. Iterate with AI suggestions.",
              },
              {
                num: "3",
                title: "Prior Art & FTO Search",
                desc: "Run embedding-based prior art search across USPTO, EPO, and WIPO. Get relevance-ranked results with side-by-side claim comparison and FTO risk scoring.",
              },
              {
                num: "4",
                title: "Review & Approve",
                desc: "Patent committee reviews the disclosure, claims, and prior art report in the collaboration workspace. Approve, request changes, or reject with comments.",
              },
              {
                num: "5",
                title: "File & Track",
                desc: "Once approved, file the application. Docket auto-calculates all deadlines by jurisdiction and sends reminders. Track prosecution status in real time.",
              },
              {
                num: "6",
                title: "Portfolio Analytics",
                desc: "Monitor your entire IP portfolio from the dashboard. Track technology landscapes, competitor filings, maintenance fee schedules, and valuation trends.",
              },
            ].map((step) => (
              <Step
                key={step.num}
                number={step.num}
                title={step.title}
                description={step.desc}
              />
            ))}
          </div>
        </div>
      </section>

      {/* ════════════════════════════════════════════
          SCREEN-BY-SCREEN BREAKDOWN
          ════════════════════════════════════════════ */}
      <section id="screens" className="py-20 md:py-28">
        <div className="mx-auto max-w-7xl px-4 md:px-6">
          <div className="mb-16 text-center">
            <h2 className="text-3xl font-bold text-slate-900 md:text-4xl">
              Every Screen, Purpose-Built
            </h2>
            <p className="mx-auto mt-4 max-w-2xl text-slate-600">
              Six core screens cover the full patent lifecycle — each designed for
              speed, clarity, and collaboration.
            </p>
          </div>

          <div className="grid gap-10 md:grid-cols-2 lg:grid-cols-3">
            {[
              {
                icon: LayoutDashboard,
                title: "Dashboard",
                desc: "Portfolio health at a glance. Patents by status, upcoming deadlines (30/60/90 days), overdue alerts, technology distribution (IPC breakdown), and quick-action buttons for new disclosures and searches.",
                color: "text-emerald-600",
                bg: "bg-emerald-50",
              },
              {
                icon: Layers,
                title: "Patent Portfolio",
                desc: "Sortable, filterable table of every patent in your portfolio. Filter by title, status, technology class, jurisdiction, or assignee. Bulk archive, export, or mass-tag with one click.",
                color: "text-blue-600",
                bg: "bg-blue-50",
              },
              {
                icon: FileText,
                title: "Patent Detail",
                desc: "Full patent view with claims, abstract, and drawing placeholders. Side panel shows AI Copilot suggestions (similar patents, sentiment analysis). Threaded comments for team discussion.",
                color: "text-violet-600",
                bg: "bg-violet-50",
              },
              {
                icon: Lightbulb,
                title: "Invention Disclosure",
                desc: "Structured wizard: title, description, attachments. AI generates claims draft and abstract on demand. Review workflow routes to the patent committee with approval/reject/comment actions.",
                color: "text-amber-600",
                bg: "bg-amber-50",
              },
              {
                icon: Search,
                title: "Prior Art Search",
                desc: "Keyword, technology class, or patent number search. Results show title, relevance score, publication date, and similarity badge. Side-by-side claim comparison and saved search alerts.",
                color: "text-rose-600",
                bg: "bg-rose-50",
              },
              {
                icon: CalendarDays,
                title: "Docket Calendar",
                desc: "Calendar + list views of all deadlines by jurisdiction. Color-coded urgency: red (<30 days), yellow (30-60), green (60+). Mark complete, update status, or set auto-reminders via email and in-app.",
                color: "text-cyan-600",
                bg: "bg-cyan-50",
              },
            ].map((screen) => (
              <div
                key={screen.title}
                className="rounded-2xl border border-slate-200 bg-white p-6 transition-shadow hover:shadow-lg"
              >
                <div
                  className={`mb-4 flex h-12 w-12 items-center justify-center rounded-xl ${screen.bg} ${screen.color}`}
                >
                  <screen.icon className="h-6 w-6" />
                </div>
                <h3 className="mb-2 text-lg font-semibold text-slate-900">
                  {screen.title}
                </h3>
                <p className="text-sm leading-relaxed text-slate-600">
                  {screen.desc}
                </p>
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* ════════════════════════════════════════════
          SECURITY & COMPLIANCE
          ════════════════════════════════════════════ */}
      <section
        id="security"
        className="relative overflow-hidden bg-gradient-to-br from-slate-50 to-blue-50 py-20 md:py-28"
      >
        <div className="mx-auto max-w-7xl px-4 md:px-6">
          <div className="mb-16 text-center">
            <h2 className="text-3xl font-bold text-slate-900 md:text-4xl">
              Enterprise-Grade Security
            </h2>
            <p className="mx-auto mt-4 max-w-2xl text-slate-600">
              Your IP data is your most valuable asset. We protect it with
              defense-in-depth security, encryption, and compliance controls.
            </p>
          </div>

          <div className="grid gap-6 sm:grid-cols-2 lg:grid-cols-4">
            {[
              {
                icon: Lock,
                title: "AES-256 Encryption",
                desc: "All patent data encrypted at rest and in transit with TLS 1.3. Keys managed by a dedicated HSM layer.",
              },
              {
                icon: Users,
                title: "OAuth 2.0 / SAML SSO",
                desc: "Enterprise single sign-on with SAML 2.0 and OAuth 2.0. Role-based access control (RBAC) for teams.",
              },
              {
                icon: Clock,
                title: "Audit Trail",
                desc: "Every change to a patent, docket entry, or disclosure is logged with user ID, timestamp, and diff. Immutable history.",
              },
              {
                icon: ShieldCheck,
                title: "SOC 2 / HIPAA Ready",
                desc: "SOC 2 Type II compliance roadmap for v1.3. HIPAA-ready architecture with BAAs available for enterprise accounts.",
              },
            ].map((item) => (
              <div
                key={item.title}
                className="rounded-2xl border border-slate-200 bg-white p-6 text-center shadow-sm"
              >
                <div className="mx-auto mb-4 flex h-12 w-12 items-center justify-center rounded-xl bg-blue-50 text-blue-600">
                  <item.icon className="h-6 w-6" />
                </div>
                <h3 className="mb-2 text-base font-semibold text-slate-900">
                  {item.title}
                </h3>
                <p className="text-sm text-slate-600">{item.desc}</p>
              </div>
            ))}
          </div>

          {/* Rate limits */}
          <div className="mx-auto mt-12 flex max-w-2xl flex-col items-center justify-center gap-4 rounded-2xl border border-blue-200 bg-white p-6 shadow-sm sm:flex-row sm:gap-8">
            <div className="text-center">
              <div className="text-2xl font-bold text-blue-600">100/min</div>
              <div className="text-xs text-slate-500">Free Tier API Limit</div>
            </div>
            <div className="hidden h-10 w-px bg-slate-200 sm:block" />
            <div className="text-center">
              <div className="text-2xl font-bold text-blue-600">1,000/min</div>
              <div className="text-xs text-slate-500">Pro Tier API Limit</div>
            </div>
            <div className="hidden h-10 w-px bg-slate-200 sm:block" />
            <div className="text-center">
              <div className="text-2xl font-bold text-blue-600">99.9%</div>
              <div className="text-xs text-slate-500">Paid Tier SLA</div>
            </div>
          </div>
        </div>
      </section>

      {/* ════════════════════════════════════════════
          TECH STACK
          ════════════════════════════════════════════ */}
      <section className="py-16 md:py-20 bg-white">
        <div className="mx-auto max-w-7xl px-4 md:px-6">
          <div className="mb-10 text-center">
            <h2 className="text-2xl font-bold text-slate-900 md:text-3xl">
              Built on the DClaw Stack
            </h2>
            <p className="mt-2 text-slate-600">
              Modern, scalable, and AI-ready architecture.
            </p>
          </div>
          <div className="flex flex-wrap items-center justify-center gap-4">
            {[
              "FastAPI",
              "SQLAlchemy 2.0",
              "Pydantic v2",
              "PostgreSQL + pgvector",
              "Redis",
              "Celery",
              "Next.js 14",
              "Tailwind CSS",
              "Docker",
              "Kubernetes",
              "OpenAI / LLMs",
              "Sentence Transformers",
            ].map((tag) => (
              <span
                key={tag}
                className="rounded-full border border-slate-200 bg-slate-50 px-4 py-2 text-sm font-medium text-slate-700"
              >
                {tag}
              </span>
            ))}
          </div>
        </div>
      </section>

      {/* ════════════════════════════════════════════
          CTA
          ════════════════════════════════════════════ */}
      <section className="bg-slate-900 py-20 text-white">
        <div className="mx-auto max-w-4xl px-4 text-center md:px-6">
          <h2 className="text-3xl font-bold md:text-4xl">
            Ready to Protect Your Innovations?
          </h2>
          <p className="mx-auto mt-4 max-w-xl text-slate-400">
            Join IP teams using DClaw Patent to draft faster, search deeper, and
            manage smarter. Start free — no credit card required.
          </p>
          <div className="mt-8 flex flex-col items-center justify-center gap-3 sm:flex-row">
            <Button
              size="lg"
              className="gap-2 bg-blue-600 text-white hover:bg-blue-500 text-base px-8"
            >
              Start Free Trial
              <ArrowRight className="h-4 w-4" />
            </Button>
            <Button
              variant="outline"
              size="lg"
              className="border-slate-600 text-slate-300 hover:bg-slate-800 hover:text-white text-base px-8"
            >
              Contact Sales
            </Button>
          </div>
          <p className="mt-6 text-xs text-slate-500">
            Free forever for individuals. Team plans start at $49/user/month.
          </p>
        </div>
      </section>

      {/* ════════════════════════════════════════════
          FOOTER
          ════════════════════════════════════════════ */}
      <footer className="border-t border-slate-200 bg-white py-12">
        <div className="mx-auto max-w-7xl px-4 md:px-6">
          <div className="flex flex-col items-center justify-between gap-6 md:flex-row">
            <div className="flex items-center gap-2">
              <div className="flex h-8 w-8 items-center justify-center rounded-md bg-blue-600 text-white">
                <Sparkles className="h-4 w-4" />
              </div>
              <span className="text-lg font-bold text-slate-900">
                DClaw <span className="text-blue-600">Patent</span>
              </span>
            </div>
            <div className="flex gap-6 text-sm text-slate-500">
              <span>© 2026 DClaw Patent</span>
              <span className="hidden sm:inline">·</span>
              <a href="#" className="hover:text-blue-600">Privacy</a>
              <a href="#" className="hover:text-blue-600">Terms</a>
              <a href="#" className="hover:text-blue-600">Security</a>
            </div>
          </div>
          <div className="mt-6 text-center text-xs text-slate-400">
            Built by Udai Kiran — udai.kiran@oneconvergence.com
          </div>
        </div>
      </footer>
    </div>
  )
}
