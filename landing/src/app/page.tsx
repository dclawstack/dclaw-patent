"use client"

import { useState, useEffect, useRef } from "react"
import { motion, useScroll, useSpring } from "framer-motion"
import {
  Brain, Search, CalendarDays, ShieldCheck, Zap, FileText,
  BarChart3, Globe, LayoutDashboard, Sparkles, Clock, Lock,
  MessageSquare, Lightbulb, TrendingUp, Users, Layers, Hash,
  ArrowRight, Menu, X, Play, Star,
  CheckCircle2, Mail, Github, Twitter,
} from "lucide-react"
import { Button } from "@/components/ui/button"

/* ════════════════════════════════════════════
   ANIMATION VARIANTS
   ════════════════════════════════════════════ */
const fadeUp = {
  initial: { opacity: 0, y: 40 },
  whileInView: { opacity: 1, y: 0 },
  viewport: { once: true, margin: "-80px" },
  transition: { duration: 0.6, ease: "easeOut" as const },
}

const fadeIn = {
  initial: { opacity: 0 },
  whileInView: { opacity: 1 },
  viewport: { once: true },
  transition: { duration: 0.8 },
}

const staggerContainer = {
  initial: {},
  whileInView: { transition: { staggerChildren: 0.1 } },
  viewport: { once: true, margin: "-50px" },
}

const scaleIn = {
  initial: { opacity: 0, scale: 0.9 },
  whileInView: { opacity: 1, scale: 1 },
  viewport: { once: true },
  transition: { duration: 0.5, ease: "easeOut" as const },
}

/* ════════════════════════════════════════════
   HERO PARTICLE / GRADIENT MESH COMPONENTS
   ════════════════════════════════════════════ */
function FloatingOrb({
  className,
  delay = 0,
}: {
  className?: string
  delay?: number
}) {
  return (
    <motion.div
      className={`absolute rounded-full blur-3xl ${className}`}
      animate={{
        x: [0, 30, -20, 0],
        y: [0, -40, 20, 0],
        scale: [1, 1.2, 0.9, 1],
      }}
      transition={{
        duration: 8,
        repeat: Infinity,
        ease: "easeInOut",
        delay,
      }}
    />
  )
}

/* ════════════════════════════════════════════
   KINETIC TEXT COMPONENT
   ════════════════════════════════════════════ */
function KineticHeadline({
  children,
  className = "",
  delay = 0,
}: {
  children: React.ReactNode
  className?: string
  delay?: number
}) {
  return (
    <motion.h1
      initial={{ opacity: 0, y: 50, rotateX: -20 }}
      animate={{ opacity: 1, y: 0, rotateX: 0 }}
      transition={{
        duration: 0.8,
        delay,
        ease: "easeOut",
      }}
      className={`${className}`}
      style={{ perspective: 1000 }}
    >
      {children}
    </motion.h1>
  )
}

/* ════════════════════════════════════════════
   GRADIENT TEXT — KINETIC
   ════════════════════════════════════════════ */
function GradientText({
  children,
  className = "",
}: {
  children: React.ReactNode
  className?: string
}) {
  return (
    <span
      className={`bg-[conic-gradient(at_top_left,_var(--tw-gradient-stops))] from-blue-600 via-indigo-600 via-violet-500 to-fuchsia-500 bg-clip-text text-transparent animate-gradient-xy ${className}`}
    >
      {children}
    </span>
  )
}

/* ════════════════════════════════════════════
   GLASS CARD
   ════════════════════════════════════════════ */
function GlassCard({
  children,
  className = "",
  hover = true,
}: {
  children: React.ReactNode
  className?: string
  hover?: boolean
}) {
  return (
    <motion.div
      className={`relative overflow-hidden rounded-2xl border border-white/20 bg-white/60 backdrop-blur-xl shadow-lg dark:bg-white/5 ${
        hover ? "hover:bg-white/80 dark:hover:bg-white/10 transition-colors duration-300" : ""
      } ${className}`}
      whileHover={hover ? { y: -4, boxShadow: "0 25px 50px -12px rgba(0,0,0,0.15)" } : {}}
      transition={{ duration: 0.3 }}
    >
      {/* Shine effect */}
      <div className="absolute inset-0 bg-gradient-to-br from-white/40 via-transparent to-transparent pointer-events-none" />
      <div className="relative">{children}</div>
    </motion.div>
  )
}

/* ════════════════════════════════════════════
   DASHBOARD MOCKUP — ULTRA MODERN
   ════════════════════════════════════════════ */
function DashboardMockup() {
  return (
    <motion.div
      className="mx-auto mt-12 max-w-5xl"
      {...fadeUp}
      transition={{ ...fadeUp.transition, delay: 0.4 }}
    >
      <div className="relative">
        {/* Glow behind */}
        <div className="absolute -inset-1 rounded-2xl bg-gradient-to-r from-blue-500/20 via-indigo-500/20 to-violet-500/20 blur-xl" />

        <div className="relative overflow-hidden rounded-2xl border border-slate-200/80 bg-white shadow-2xl">
          {/* Browser chrome */}
          <div className="flex items-center gap-2 border-b border-slate-100 bg-slate-50/80 px-5 py-3">
            <div className="flex gap-2">
              <div className="h-3.5 w-3.5 rounded-full bg-red-400/80" />
              <div className="h-3.5 w-3.5 rounded-full bg-amber-400/80" />
              <div className="h-3.5 w-3.5 rounded-full bg-emerald-400/80" />
            </div>
            <div className="mx-auto flex w-full max-w-md items-center gap-2 rounded-xl bg-white px-4 py-1.5 text-xs text-slate-400 border border-slate-200/60 shadow-sm">
              <Lock className="h-3 w-3 text-emerald-500" />
              dclawpatent.app/dashboard
            </div>
          </div>

          {/* App content */}
          <div className="grid grid-cols-12 gap-0">
            {/* Sidebar */}
            <div className="col-span-3 border-r border-slate-100 bg-gradient-to-b from-slate-50/80 to-white p-4">
              <div className="flex items-center gap-2 mb-6 px-1">
                <div className="flex h-8 w-8 items-center justify-center rounded-lg bg-gradient-to-br from-blue-600 to-indigo-600 text-white shadow-lg shadow-blue-500/25">
                  <Sparkles className="h-4 w-4" />
                </div>
                <span className="text-sm font-bold text-slate-800">DClaw</span>
              </div>
              {[
                { label: "Dashboard", active: true, icon: LayoutDashboard },
                { label: "Portfolio", icon: Layers },
                { label: "Prior Art", icon: Search },
                { label: "Docket", icon: CalendarDays },
                { label: "Disclosures", icon: Lightbulb },
                { label: "Analytics", icon: BarChart3 },
              ].map((item) => (
                <div
                  key={item.label}
                  className={`mb-1 flex items-center gap-3 rounded-xl px-3 py-2.5 text-xs font-medium transition-all ${
                    item.active
                      ? "bg-gradient-to-r from-blue-600 to-indigo-600 text-white shadow-lg shadow-blue-500/25"
                      : "text-slate-500 hover:bg-slate-100"
                  }`}
                >
                  <item.icon className="h-3.5 w-3.5" />
                  {item.label}
                </div>
              ))}
            </div>

            {/* Main */}
            <div className="col-span-9 p-5">
              {/* Header */}
              <div className="flex items-center justify-between mb-5">
                <div>
                  <h2 className="text-lg font-bold text-slate-900">Patent Portfolio</h2>
                  <p className="text-xs text-slate-400">247 patents across 12 jurisdictions</p>
                </div>
                <div className="flex items-center gap-3">
                  <div className="flex items-center gap-1.5 rounded-full border border-slate-200 bg-white px-3 py-1.5 text-xs text-slate-500 shadow-sm">
                    <Search className="h-3 w-3" /> Search...
                  </div>
                  <div className="flex h-8 w-8 items-center justify-center rounded-full bg-gradient-to-br from-slate-100 to-slate-200 text-xs font-bold text-slate-700">UK</div>
                </div>
              </div>

              {/* Stats cards with gradients */}
              <div className="mb-5 grid grid-cols-4 gap-3">
                {[
                  { label: "Total Patents", val: "247", trend: "+12", color: "from-blue-500/10 to-indigo-500/10", accent: "text-blue-600", border: "border-blue-200/60" },
                  { label: "Pending Review", val: "18", trend: "3 urgent", color: "from-amber-500/10 to-orange-500/10", accent: "text-amber-600", border: "border-amber-200/60" },
                  { label: "Upcoming Deadlines", val: "7", trend: "Next: 5d", color: "from-rose-500/10 to-red-500/10", accent: "text-rose-600", border: "border-rose-200/60" },
                  { label: "AI Searches", val: "1,432", trend: "+89 today", color: "from-emerald-500/10 to-green-500/10", accent: "text-emerald-600", border: "border-emerald-200/60" },
                ].map((s) => (
                  <div key={s.label} className={`relative overflow-hidden rounded-xl border ${s.border} bg-gradient-to-br ${s.color} p-3`}>
                    <div className="text-[10px] font-medium text-slate-500">{s.label}</div>
                    <div className={`text-xl font-extrabold ${s.accent}`}>{s.val}</div>
                    <div className={`text-[10px] font-medium ${s.accent}/70`}>{s.trend}</div>
                  </div>
                ))}
              </div>

              {/* Table */}
              <div className="overflow-hidden rounded-xl border border-slate-200/80 bg-white shadow-sm">
                <div className="flex items-center justify-between border-b border-slate-100 px-4 py-2.5 bg-slate-50/50">
                  <span className="text-xs font-semibold text-slate-700">Recent Patents</span>
                  <div className="flex gap-2">
                    {["Filter", "Export", "+ New"].map((a) => (
                      <span key={a} className="rounded-lg border border-slate-200 bg-white px-2.5 py-1 text-[10px] font-medium text-slate-500 shadow-sm hover:border-blue-300 hover:text-blue-600 transition-colors cursor-pointer">{a}</span>
                    ))}
                  </div>
                </div>
                <div className="divide-y divide-slate-50">
                  {[
                    { title: "Quantum Error Correction Protocol", status: "Prosecution", class: "H01L", date: "2026-05-12", pct: "78%" },
                    { title: "Neural Network Compression Method", status: "Issued", class: "G06N", date: "2026-04-28", pct: "100%" },
                    { title: "Solid-State Battery Electrode", status: "Filed", class: "H01M", date: "2026-04-15", pct: "45%" },
                    { title: "Optical Fiber Amplifier Design", status: "Draft", class: "H01S", date: "2026-04-03", pct: "12%" },
                  ].map((p, i) => (
                    <div key={i} className="flex items-center justify-between px-4 py-2.5 hover:bg-slate-50/50 transition-colors">
                      <div className="flex items-center gap-3">
                        <div className={`h-2 w-2 rounded-full ${
                          p.status === "Issued" ? "bg-emerald-500" :
                          p.status === "Prosecution" ? "bg-blue-500" :
                          p.status === "Filed" ? "bg-violet-500" : "bg-slate-300"
                        }`} />
                        <div>
                          <div className="text-xs font-semibold text-slate-700">{p.title}</div>
                          <div className="text-[10px] text-slate-400">{p.class} · USPTO · {p.date}</div>
                        </div>
                      </div>
                      <div className="flex items-center gap-3">
                        <div className="w-16">
                          <div className="h-1.5 rounded-full bg-slate-100 overflow-hidden">
                            <div className={`h-full rounded-full ${
                              parseInt(p.pct) > 80 ? "bg-emerald-500" :
                              parseInt(p.pct) > 40 ? "bg-blue-500" : "bg-slate-300"
                            }`} style={{ width: p.pct }} />
                          </div>
                        </div>
                        <span className={`rounded-full px-2.5 py-0.5 text-[10px] font-bold ${
                          p.status === "Issued" ? "bg-emerald-50 text-emerald-700 border border-emerald-200" :
                          p.status === "Prosecution" ? "bg-blue-50 text-blue-700 border border-blue-200" :
                          p.status === "Filed" ? "bg-violet-50 text-violet-700 border border-violet-200" :
                          "bg-slate-100 text-slate-500 border border-slate-200"
                        }`}>{p.status}</span>
                      </div>
                    </div>
                  ))}
                </div>
              </div>

              {/* Alert strip */}
              <motion.div
                className="mt-3 flex items-center gap-3 rounded-xl border border-amber-200/80 bg-gradient-to-r from-amber-50/80 to-orange-50/80 px-4 py-2.5"
                animate={{ opacity: [0.7, 1, 0.7] }}
                transition={{ duration: 3, repeat: Infinity }}
              >
                <div className="flex h-6 w-6 items-center justify-center rounded-full bg-amber-500/20">
                  <div className="h-2 w-2 rounded-full bg-amber-500" />
                </div>
                <span className="text-[11px] text-slate-600"><strong className="text-amber-700">Office Action</strong> response due for <em>Quantum Error Correction</em> — <strong className="text-amber-700">5 days remaining</strong></span>
                <span className="ml-auto rounded-lg bg-gradient-to-r from-blue-600 to-indigo-600 px-3 py-1 text-[10px] font-bold text-white shadow-lg shadow-blue-500/25 cursor-pointer hover:shadow-blue-500/40 transition-shadow">Respond Now</span>
              </motion.div>
            </div>
          </div>
        </div>
      </div>
    </motion.div>
  )
}

/* ════════════════════════════════════════════
   ANIMATED COUNTER
   ════════════════════════════════════════════ */
function AnimatedCounter({ target, suffix = "" }: { target: number; suffix?: string }) {
  const [count, setCount] = useState(0)
  const ref = useRef<HTMLDivElement>(null)
  const [hasAnimated, setHasAnimated] = useState(false)

  useEffect(() => {
    const observer = new IntersectionObserver(
      ([entry]) => {
        if (entry.isIntersecting && !hasAnimated) {
          setHasAnimated(true)
          const duration = 2000
          const steps = 60
          const stepTime = duration / steps
          let current = 0
          const ticker = setInterval(() => {
            current += target / steps
            if (current >= target) {
              setCount(target)
              clearInterval(ticker)
            } else {
              setCount(Math.floor(current))
            }
          }, stepTime)
        }
      },
      { threshold: 0.5 }
    )
    if (ref.current) observer.observe(ref.current)
    return () => observer.disconnect()
  }, [target, hasAnimated])

  return (
    <div ref={ref} className="text-4xl md:text-5xl font-black text-slate-900">
      {count.toLocaleString()}{suffix}
    </div>
  )
}

/* ════════════════════════════════════════════
   FEATURE CARD — MOTION
   ════════════════════════════════════════════ */
function FeatureCard({
  icon: Icon,
  title,
  description,
  tags,
  index,
}: {
  icon: React.ElementType
  title: string
  description: string
  tags: string[]
  index: number
}) {
  return (
    <motion.div
      initial={{ opacity: 0, y: 30 }}
      whileInView={{ opacity: 1, y: 0 }}
      viewport={{ once: true, margin: "-50px" }}
      transition={{ duration: 0.5, delay: index * 0.08, ease: "easeOut" }}
      whileHover={{ y: -6, transition: { duration: 0.2 } }}
      className="group relative overflow-hidden rounded-2xl border border-slate-200/60 bg-white p-6 shadow-sm transition-shadow duration-300 hover:shadow-2xl hover:shadow-blue-900/5 hover:border-blue-300/50"
    >
      {/* Gradient blob on hover */}
      <div className="absolute -top-20 -right-20 h-40 w-40 rounded-full bg-gradient-to-br from-blue-500/10 to-indigo-500/10 blur-2xl opacity-0 transition-opacity duration-500 group-hover:opacity-100" />

      <div className="relative">
        <div className="mb-5 flex h-14 w-14 items-center justify-center rounded-2xl bg-gradient-to-br from-blue-50 to-indigo-100 text-blue-600 shadow-sm transition-all duration-300 group-hover:scale-110 group-hover:shadow-lg group-hover:shadow-blue-500/10 group-hover:from-blue-500 group-hover:to-indigo-600 group-hover:text-white">
          <Icon className="h-6 w-6" />
        </div>
        <h3 className="mb-3 text-lg font-bold text-slate-900 group-hover:text-blue-700 transition-colors">{title}</h3>
        <p className="mb-5 text-sm leading-relaxed text-slate-500">{description}</p>
        <div className="flex flex-wrap gap-2">
          {tags.map((t) => (
            <span key={t} className="rounded-full bg-gradient-to-r from-slate-50 to-slate-100 border border-slate-200/60 px-3 py-1 text-[11px] font-semibold text-slate-600 group-hover:bg-blue-50 group-hover:text-blue-600 group-hover:border-blue-200/60 transition-colors">
              {t}
            </span>
          ))}
        </div>
      </div>
    </motion.div>
  )
}

/* ════════════════════════════════════════════
   MARQUEE BANNER
   ════════════════════════════════════════════ */
function MarqueeBanner() {
  const items = [
    "AI-Powered Claim Drafting",
    "Vector Embeddings Search",
    "Multi-Jurisdiction Docketing",
    "Prior Art Analysis",
    "FTO Risk Assessment",
    "Patent Valuation",
    "Competitive Intelligence",
    "Technology Landscapes",
  ]
  return (
    <div className="relative overflow-hidden bg-gradient-to-r from-blue-600 via-indigo-600 to-violet-600 py-4">
      <div className="absolute inset-0 bg-[url('data:image/svg+xml;base64,PHN2ZyB3aWR0aD0iNDAiIGhlaWdodD0iNDAiIHhtbG5zPSJodHRwOi8vd3d3LnczLm9yZy8yMDAwL3N2ZyI+PGNpcmNsZSBjeD0iMTAiIGN5PSIxMCIgcj0iMSIgZmlsbD0id2hpdGUiIG9wYWNpdHk9IjAuMSIvPjwvc3ZnPg==')] opacity-30" />
      <motion.div
        className="flex gap-8 whitespace-nowrap"
        animate={{ x: ["0%", "-50%"] }}
        transition={{ duration: 30, repeat: Infinity, ease: "linear" }}
      >
        {[...items, ...items, ...items, ...items].map((item, i) => (
          <span key={i} className="flex items-center gap-3 text-sm font-bold text-white/90">
            <Star className="h-3.5 w-3.5 text-yellow-300" />
            {item}
          </span>
        ))}
      </motion.div>
    </div>
  )
}

/* ═════════════════════════════════════════════
   MAIN PAGE
   ════════════════════════════════════════════ */
export default function LandingPage() {
  const [mobileOpen, setMobileOpen] = useState(false)
  const [scrolled, setScrolled] = useState(false)
  const { scrollYProgress } = useScroll()
  const scaleX = useSpring(scrollYProgress, { stiffness: 100, damping: 30 })

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
    <div className="min-h-screen bg-white overflow-x-hidden">
      {/* Scroll progress bar */}
      <motion.div className="fixed top-0 left-0 right-0 z-[60] h-1 origin-left bg-gradient-to-r from-blue-600 via-indigo-500 to-violet-500" style={{ scaleX }} />

      {/* ── Navigation ── */}
      <motion.nav
        className={`fixed left-0 right-0 top-0 z-50 transition-all duration-500 ${scrolled ? "bg-white/70 shadow-lg shadow-blue-900/5 backdrop-blur-xl" : "bg-transparent"}`}
        initial={{ y: -100 }}
        animate={{ y: 0 }}
        transition={{ duration: 0.6, ease: "easeOut" }}
      >
        <div className="mx-auto flex max-w-7xl items-center justify-between px-4 py-4 md:px-6">
          <div className="flex items-center gap-2.5">
            <div className="flex h-9 w-9 items-center justify-center rounded-xl bg-gradient-to-br from-blue-600 to-indigo-600 text-white shadow-lg shadow-blue-500/25">
              <Sparkles className="h-5 w-5" />
            </div>
            <span className="text-xl font-black text-slate-900 tracking-tight">
              DClaw <span className="bg-gradient-to-r from-blue-600 to-indigo-600 bg-clip-text text-transparent">Patent</span>
            </span>
          </div>

          <div className="hidden items-center gap-8 md:flex">
            {[["Features", "features"], ["AI Engine", "ai-engine"], ["Screens", "screens"], ["Security", "security"]].map(([label, id]) => (
              <button key={id} onClick={() => scrollTo(id)} className="relative text-sm font-semibold text-slate-600 transition-colors hover:text-blue-600 group">
                {label}
                <span className="absolute -bottom-1 left-0 h-0.5 w-0 bg-gradient-to-r from-blue-600 to-indigo-600 transition-all duration-300 group-hover:w-full" />
              </button>
            ))}
          </div>

          <div className="hidden items-center gap-3 md:flex">
            <Button variant="ghost" size="sm" className="font-semibold text-slate-600 hover:text-blue-600">Sign In</Button>
            <Button size="sm" className="bg-gradient-to-r from-blue-600 to-indigo-600 text-white font-semibold shadow-lg shadow-blue-500/25 hover:shadow-blue-500/40 transition-shadow">Get Started</Button>
          </div>

          <button className="md:hidden" onClick={() => setMobileOpen(!mobileOpen)}>
            {mobileOpen ? <X className="h-6 w-6 text-slate-700" /> : <Menu className="h-6 w-6 text-slate-700" />}
          </button>
        </div>

        {mobileOpen && (
          <motion.div initial={{ opacity: 0, height: 0 }} animate={{ opacity: 1, height: "auto" }} className="border-t border-slate-100 bg-white/90 backdrop-blur-xl px-4 pb-4 md:hidden">
            {[["Features", "features"], ["AI Engine", "ai-engine"], ["Screens", "screens"], ["Security", "security"]].map(([label, id]) => (
              <button key={id} onClick={() => scrollTo(id)} className="block w-full py-3 text-left text-sm font-bold text-slate-700">{label}</button>
            ))}
            <div className="mt-2 flex flex-col gap-2 pt-3 border-t border-slate-100">
              <Button variant="outline" className="w-full font-semibold">Sign In</Button>
              <Button className="w-full bg-gradient-to-r from-blue-600 to-indigo-600 text-white font-semibold">Get Started</Button>
            </div>
          </motion.div>
        )}
      </motion.nav>

      {/* ════════════════════════════════════════════
          HERO SECTION — KINETIC PARALLAX
          ════════════════════════════════════════════ */}
      <section className="relative min-h-screen overflow-hidden bg-gradient-to-br from-slate-50 via-blue-50/30 to-indigo-50/20 pt-32 pb-16">
        {/* Animated gradient orbs */}
        <FloatingOrb className="-top-40 -right-40 h-[600px] w-[600px] bg-gradient-to-br from-blue-400/30 to-indigo-400/20" delay={0} />
        <FloatingOrb className="-bottom-60 -left-40 h-[500px] w-[500px] bg-gradient-to-br from-violet-400/25 to-fuchsia-400/15" delay={2} />
        <FloatingOrb className="top-1/3 right-1/4 h-[300px] w-[300px] bg-gradient-to-br from-cyan-400/20 to-blue-400/20" delay={4} />

        {/* Grid overlay */}
        <div className="pointer-events-none absolute inset-0 bg-[linear-gradient(rgba(99,102,241,0.03)_1px,transparent_1px),linear-gradient(90deg,rgba(99,102,241,0.03)_1px,transparent_1px)] bg-[size:64px_64px]" />

        <div className="relative mx-auto max-w-7xl px-4 md:px-6">
          <div className="mx-auto max-w-4xl text-center">
            {/* Badge */}
            <motion.div
              initial={{ opacity: 0, y: 20, scale: 0.9 }}
              animate={{ opacity: 1, y: 0, scale: 1 }}
              transition={{ duration: 0.5 }}
              className="mb-8 inline-flex items-center gap-2.5 rounded-full border border-blue-200/80 bg-white/80 backdrop-blur-sm px-5 py-2 text-sm font-bold text-blue-700 shadow-sm shadow-blue-500/5"
            >
              <span className="relative flex h-2.5 w-2.5">
                <span className="absolute inline-flex h-full w-full animate-ping rounded-full bg-blue-400 opacity-75" />
                <span className="relative inline-flex h-2.5 w-2.5 rounded-full bg-gradient-to-br from-blue-500 to-indigo-500" />
              </span>
              AI-Powered Patent Management Platform
            </motion.div>

            {/* Kinetic headline */}
            <KineticHeadline className="text-5xl font-black tracking-tight text-slate-900 sm:text-6xl md:text-7xl lg:text-8xl" delay={0.15}>
              Draft. Search. Track.
            </KineticHeadline>
            <KineticHeadline className="text-5xl font-black tracking-tight sm:text-6xl md:text-7xl lg:text-8xl mt-2" delay={0.3}>
              <GradientText>Protect Smarter.</GradientText>
            </KineticHeadline>

            <motion.p
              className="mx-auto mt-8 max-w-2xl text-lg leading-relaxed text-slate-500 md:text-xl"
              initial={{ opacity: 0 }}
              animate={{ opacity: 1 }}
              transition={{ delay: 0.5, duration: 0.8 }}
            >
              The first AI-native patent management platform. Draft claims in minutes, search prior art with
              <span className="font-bold text-slate-700"> vector embeddings</span>, and track deadlines across
              <span className="font-bold text-slate-700"> 150+ jurisdictions</span> — all from one intelligent dashboard.
            </motion.p>

            <motion.div
              className="mt-10 flex flex-col items-center justify-center gap-4 sm:flex-row"
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ delay: 0.65, duration: 0.5 }}
            >
              <Button size="lg" className="group gap-3 bg-gradient-to-r from-blue-600 to-indigo-600 text-white text-base font-bold px-8 py-6 shadow-xl shadow-blue-500/25 hover:shadow-blue-500/40 transition-all hover:scale-[1.02]">
                Start Free Trial
                <ArrowRight className="h-4 w-4 transition-transform group-hover:translate-x-1" />
              </Button>
              <Button variant="outline" size="lg" className="group gap-2 text-base font-bold px-8 py-6 border-2 border-slate-200 hover:border-blue-300 hover:text-blue-600 transition-all">
                <Play className="h-4 w-4" /> Watch Demo
              </Button>
            </motion.div>

            {/* Social proof */}
            <motion.div
              className="mt-10 flex items-center justify-center gap-6 text-sm text-slate-400"
              initial={{ opacity: 0 }}
              animate={{ opacity: 1 }}
              transition={{ delay: 0.8 }}
            >
              <div className="flex -space-x-3">
                {[1,2,3,4].map((i) => (
                  <div key={i} className={`flex h-10 w-10 items-center justify-center rounded-full border-2 border-white text-xs font-bold text-white shadow-md ${
                    i === 1 ? "bg-gradient-to-br from-blue-500 to-indigo-500" :
                    i === 2 ? "bg-gradient-to-br from-violet-500 to-purple-500" :
                    i === 3 ? "bg-gradient-to-br from-rose-500 to-pink-500" :
                    "bg-gradient-to-br from-emerald-500 to-teal-500"
                  }`}>
                    {["JD", "AK", "SR", "ML"][i-1]}
                  </div>
                ))}
              </div>
              <div className="text-left">
                <div className="flex gap-0.5">
                  {[1,2,3,4,5].map(i => <Star key={i} className="h-4 w-4 fill-amber-400 text-amber-400" />)}
                </div>
                <p className="text-xs">Trusted by 500+ IP teams worldwide</p>
              </div>
            </motion.div>
          </div>

          <DashboardMockup />
        </div>
      </section>

      {/* Marquee banner */}
      <MarqueeBanner />

      {/* ════════════════════════════════════════════
          STATS SECTION — ANIMATED COUNTERS
          ════════════════════════════════════════════ */}
      <section className="relative bg-gradient-to-br from-slate-900 to-slate-800 py-24 text-white">
        <div className="pointer-events-none absolute inset-0 bg-[url('data:image/svg+xml;base64,PHN2ZyB3aWR0aD0iNjQiIGhlaWdodD0iNjQiIHhtbG5zPSJodHRwOi8vd3d3LnczLm9yZy8yMDAwL3N2ZyI+PGNpcmNsZSBjeD0iMiIgY3k9IjIiIHI9IjEiIGZpbGw9IndoaXRlIiBvcGFjaXR5PSIwLjAzIi8+PC9zdmc+')]" />
        <div className="relative mx-auto max-w-7xl px-4 md:px-6">
          <motion.div className="grid grid-cols-2 gap-12 md:grid-cols-4" {...staggerContainer}>
            {[
              { val: 247, suffix: "+", label: "Patents Managed" },
              { val: 10, suffix: "min", label: "Avg. Claim Draft" },
              { val: 150, suffix: "+", label: "Jurisdictions" },
              { val: 99, suffix: "%", label: "Satisfaction Rate" },
            ].map((s) => (
              <motion.div key={s.label} className="text-center" {...scaleIn}>
                <AnimatedCounter target={s.val} suffix={s.suffix} />
                <div className="mt-2 text-sm font-semibold text-slate-400">{s.label}</div>
              </motion.div>
            ))}
          </motion.div>
        </div>
      </section>

      {/* ════════════════════════════════════════════
          FEATURES — BENTO GRID + GLASSMORPHISM
          ════════════════════════════════════════════ */}
      <section id="features" className="relative py-28 bg-gradient-to-b from-white via-slate-50/50 to-white">
        <div className="pointer-events-none absolute inset-0 bg-[radial-gradient(ellipse_80%_80%_at_50%_-20%,rgba(59,130,246,0.07),transparent)]" />
        <div className="relative mx-auto max-w-7xl px-4 md:px-6">
          <motion.div className="mx-auto mb-20 max-w-2xl text-center" {...fadeUp}>
            <span className="mb-4 inline-block rounded-full bg-blue-50 border border-blue-200 px-4 py-1.5 text-xs font-bold text-blue-700">FEATURES</span>
            <h2 className="text-4xl font-black tracking-tight text-slate-900 md:text-5xl lg:text-6xl">
              Everything You Need for <br />
              <GradientText>IP Management</GradientText>
            </h2>
            <p className="mt-6 text-lg text-slate-500">
              From invention disclosure to patent grant — a complete end-to-end platform powered by AI at every step.
            </p>
          </motion.div>

          <div className="grid gap-6 md:grid-cols-2 lg:grid-cols-3">
            {[
              { icon: Brain, title: "AI Patent Copilot", desc: "Ask natural-language questions. AI searches millions of patents with vector embeddings and ranks results by relevance.", tags: ["RAG Search", "Embeddings", "Summaries"], color: "from-blue-500/20 to-indigo-500/20", iconColor: "from-blue-500 to-indigo-600", border: "group-hover:border-blue-400/50" },
              { icon: FileText, title: "AI Claim Drafting", desc: "Paste an invention disclosure and get professionally structured independent + dependent claims in under 10 minutes.", tags: ["LLM Generation", "Patent Syntax", "10-min MVP"], color: "from-violet-500/20 to-purple-500/20", iconColor: "from-violet-500 to-purple-600", border: "group-hover:border-violet-400/50" },
              { icon: Search, title: "Prior Art Search", desc: "Search USPTO, EPO, WIPO with AI-powered relevance ranking. Side-by-side claim comparison and saved alerts.", tags: ["3 Offices", "Relevance Scores", "Alerts"], color: "from-emerald-500/20 to-teal-500/20", iconColor: "from-emerald-500 to-teal-600", border: "group-hover:border-emerald-400/50" },
              { icon: CalendarDays, title: "Smart Docketing", desc: "Track deadlines across jurisdictions with auto-calculation. Color-coded urgency alerts with email & in-app reminders.", tags: ["Auto-Calc", "Multi-Jurisdiction", "Reminders"], color: "from-amber-500/20 to-orange-500/20", iconColor: "from-amber-500 to-orange-600", border: "group-hover:border-amber-400/50" },
              { icon: LayoutDashboard, title: "Portfolio Dashboard", desc: "Visual command center with status breakdowns, technology clusters, geographic coverage, and spend analysis.", tags: ["IPC/CPC", "Tech Clusters", "Spend"], color: "from-rose-500/20 to-pink-500/20", iconColor: "from-rose-500 to-pink-600", border: "group-hover:border-rose-400/50" },
              { icon: Lightbulb, title: "Invention Disclosure", desc: "Structured intake with AI PDF parsing, auto-generated abstracts & claims, and review routing to patent committees.", tags: ["PDF Parsing", "Review Flow", "AI Assist"], color: "from-cyan-500/20 to-sky-500/20", iconColor: "from-cyan-500 to-sky-600", border: "group-hover:border-cyan-400/50" },
            ].map((f, i) => (
              <FeatureCard key={f.title} icon={f.icon} title={f.title} description={f.desc} tags={f.tags} index={i} />
            ))}
          </div>
        </div>
      </section>

      {/* ════════════════════════════════════════════
          WIDE BANNER — AI ENGINE
          ════════════════════════════════════════════ */}
      <section id="ai-engine" className="relative overflow-hidden bg-slate-900 py-28 text-white">
        <FloatingOrb className="top-0 right-0 h-[400px] w-[400px] bg-blue-500/10" delay={1} />
        <FloatingOrb className="bottom-0 left-0 h-[300px] w-[300px] bg-indigo-500/10" delay={3} />
        <div className="pointer-events-none absolute inset-0 bg-[radial-gradient(ellipse_60%_60%_at_50%_50%,rgba(59,130,246,0.08),transparent)]" />
        <div className="relative mx-auto max-w-7xl px-4 md:px-6">
          <motion.div className="mb-20 text-center" {...fadeUp}>
            <span className="mb-4 inline-block rounded-full border border-blue-500/30 bg-blue-500/10 px-4 py-1.5 text-xs font-bold text-blue-400">HOW IT WORKS</span>
            <h2 className="text-4xl font-black md:text-5xl lg:text-6xl">
              The <GradientText>AI Engine</GradientText>
            </h2>
            <p className="mx-auto mt-6 max-w-2xl text-lg text-slate-400">
              Every AI feature is built on a modern ML stack with patent-specific fine-tuning, vector search, and RAG pipelines.
            </p>
          </motion.div>

          <div className="grid gap-8 md:grid-cols-3">
            {[
              { step: "01", icon: Hash, title: "Vector Embeddings", desc: "Patents are converted into high-dimensional embeddings using fine-tuned sentence transformers, stored in PostgreSQL with pgvector for lightning-fast similarity search.", color: "blue" },
              { step: "02", icon: Layers, title: "RAG Pipeline", desc: "Retrieval-Augmented Generation fetches the most relevant patent documents from the vector store, then feeds them into an LLM for accurate, grounded outputs.", color: "indigo" },
              { step: "03", icon: FileText, title: "Patent Prompting", desc: "LLM prompts are engineered for patent law syntax — independent/dependent claims, prior art citations, IPC/CPC codes, and jurisdiction-specific language.", color: "violet" },
            ].map((item, i) => (
              <motion.div
                key={i}
                initial={{ opacity: 0, y: 40 }}
                whileInView={{ opacity: 1, y: 0 }}
                viewport={{ once: true }}
                transition={{ delay: i * 0.15, duration: 0.6 }}
                className="group relative rounded-2xl border border-slate-700/50 bg-gradient-to-b from-slate-800/80 to-slate-800/40 p-8 backdrop-blur-sm"
              >
                <div className="mb-6 text-6xl font-black text-slate-700/50 group-hover:text-blue-500/30 transition-colors">
                  {item.step}
                </div>
                <div className={`mb-5 flex h-14 w-14 items-center justify-center rounded-2xl bg-gradient-to-br from-${item.color}-500/20 to-${item.color}-600/20 text-${item.color}-400 border border-${item.color}-500/30`}>
                  <item.icon className="h-7 w-7" />
                </div>
                <h3 className="mb-3 text-xl font-bold text-white">{item.title}</h3>
                <p className="text-sm leading-relaxed text-slate-400">{item.desc}</p>
                <div className="absolute bottom-0 left-0 right-0 h-1 bg-gradient-to-r from-blue-500 via-indigo-500 to-violet-500 rounded-b-2xl opacity-0 group-hover:opacity-100 transition-opacity" />
              </motion.div>
            ))}
          </div>
        </div>
      </section>

      {/* ════════════════════════════════════════════
          SCREEN SHOWCASE — KINETIC
          ════════════════════════════════════════════ */}
      <section id="screens" className="relative overflow-hidden py-28 bg-white">
        <div className="pointer-events-none absolute inset-0 bg-[radial-gradient(ellipse_80%_50%_at_50%_100%,rgba(99,102,241,0.05),transparent)]" />
        <div className="relative mx-auto max-w-7xl px-4 md:px-6">
          <motion.div className="mb-20 text-center" {...fadeUp}>
            <span className="mb-4 inline-block rounded-full bg-indigo-50 border border-indigo-200 px-4 py-1.5 text-xs font-bold text-indigo-700">INTERFACE</span>
            <h2 className="text-4xl font-black text-slate-900 md:text-5xl">Every Screen, <br /><GradientText>Purpose-Built</GradientText></h2>
          </motion.div>

          <div className="grid gap-8 md:grid-cols-2">
            {[
              {
                title: "Dashboard",
                subtitle: "Portfolio health at a glance",
                icon: LayoutDashboard,
                color: "from-emerald-500 to-teal-500",
                bg: "from-emerald-50 to-teal-50",
                features: ["Real-time patent counts by status", "Upcoming deadlines with urgency colors", "IPC/CPC technology distribution", "AI search activity tracking"],
              },
              {
                title: "Prior Art Search",
                subtitle: "AI-powered multi-office search",
                icon: Search,
                color: "from-blue-500 to-indigo-500",
                bg: "from-blue-50 to-indigo-50",
                features: ["USPTO, EPO, WIPO unified search", "Embedding-based relevance ranking", "Side-by-side claim comparison", "Saved searches with email alerts"],
              },
              {
                title: "Docket Calendar",
                subtitle: "Never miss another deadline",
                icon: CalendarDays,
                color: "from-amber-500 to-orange-500",
                bg: "from-amber-50 to-orange-50",
                features: ["Multi-jurisdiction deadline auto-calc", "Color-coded urgency (red/yellow/green)", "Email & in-app auto-reminders", "Calendar + list views"],
              },
              {
                title: "Invention Disclosure",
                subtitle: "From idea to claims in 10 minutes",
                icon: Lightbulb,
                color: "from-violet-500 to-purple-500",
                bg: "from-violet-50 to-purple-50",
                features: ["Structured intake wizard with PDF upload", "AI auto-generates claims + abstract", "Patent committee review workflow", "One-click approval to filing"],
              },
            ].map((screen, i) => (
              <motion.div
                key={screen.title}
                initial={{ opacity: 0, x: i % 2 === 0 ? -40 : 40 }}
                whileInView={{ opacity: 1, x: 0 }}
                viewport={{ once: true }}
                transition={{ duration: 0.6, ease: "easeOut" }}
                className="group relative overflow-hidden rounded-3xl border border-slate-200/60 bg-white p-8 shadow-lg shadow-slate-900/5 transition-shadow hover:shadow-2xl hover:shadow-blue-900/5"
              >
                <div className={`absolute top-0 right-0 h-40 w-40 rounded-full bg-gradient-to-br ${screen.bg} blur-3xl opacity-50 transition-opacity group-hover:opacity-80`} />
                <div className="relative">
                  <div className={`mb-6 flex h-16 w-16 items-center justify-center rounded-2xl bg-gradient-to-br ${screen.color} text-white shadow-lg`}>
                    <screen.icon className="h-8 w-8" />
                  </div>
                  <h3 className="mb-1 text-2xl font-black text-slate-900">{screen.title}</h3>
                  <p className="mb-6 text-sm font-medium text-slate-400">{screen.subtitle}</p>
                  <ul className="space-y-3">
                    {screen.features.map((f) => (
                      <li key={f} className="flex items-start gap-3 text-sm text-slate-600">
                        <CheckCircle2 className="mt-0.5 h-4 w-4 shrink-0 text-emerald-500" />
                        {f}
                      </li>
                    ))}
                  </ul>
                </div>
              </motion.div>
            ))}
          </div>
        </div>
      </section>

      {/* ════════════════════════════════════════════
          TESTIMONIAL / SOCIAL PROOF BANNER
          ════════════════════════════════════════════ */}
      <section className="relative overflow-hidden bg-gradient-to-r from-slate-900 via-indigo-950 to-slate-900 py-20">
        <div className="pointer-events-none absolute inset-0 bg-[url('data:image/svg+xml;base64,PHN2ZyB3aWR0aD0iNDAiIGhlaWdodD0iNDAiIHhtbG5zPSJodHRwOi8vd3d3LnczLm9yZy8yMDAwL3N2ZyI+PGNpcmNsZSBjeD0iMTAiIGN5PSIxMCIgcj0iMSIgZmlsbD0id2hpdGUiIG9wYWNpdHk9IjAuMDUiLz48L3N2Zz4=')]" />
        <div className="relative mx-auto max-w-4xl px-4 text-center">
          <motion.div
            initial={{ opacity: 0, y: 30 }}
            whileInView={{ opacity: 1, y: 0 }}
            viewport={{ once: true }}
            transition={{ duration: 0.6 }}
          >
            <div className="mb-6 flex justify-center">
              <div className="rounded-full bg-white/10 backdrop-blur-sm border border-white/20 px-6 py-2 text-sm font-bold text-white">Loved by IP teams</div>
            </div>
            <blockquote className="text-2xl font-light italic text-white/90 md:text-3xl leading-relaxed">
              "DClaw Patent reduced our claim drafting time from <span className="font-bold text-white">6 hours to 12 minutes</span>. The AI prior art search alone saved us weeks of manual work."
            </blockquote>
            <div className="mt-8 flex items-center justify-center gap-4">
              <div className="flex h-12 w-12 items-center justify-center rounded-full bg-gradient-to-br from-blue-400 to-indigo-500 text-white font-bold">AK</div>
              <div className="text-left">
                <div className="font-bold text-white">Alex Kim</div>
                <div className="text-sm text-white/60">Chief IP Counsel, TechCorp International</div>
              </div>
            </div>
          </motion.div>
        </div>
      </section>

      {/* ════════════════════════════════════════════
          SECURITY
          ════════════════════════════════════════════ */}
      <section id="security" className="relative py-28 overflow-hidden">
        <div className="absolute inset-0 bg-gradient-to-br from-slate-900 to-slate-800" />
        <div className="pointer-events-none absolute inset-0 bg-[radial-gradient(ellipse_60%_60%_at_70%_30%,rgba(59,130,246,0.1),transparent)]" />
        <div className="relative mx-auto max-w-7xl px-4 md:px-6">
          <motion.div className="mb-16 text-center" {...fadeUp}>
            <span className="mb-4 inline-block rounded-full border border-emerald-500/30 bg-emerald-500/10 px-4 py-1.5 text-xs font-bold text-emerald-400">SECURITY</span>
            <h2 className="text-4xl font-black text-white md:text-5xl">Enterprise-Grade <br /><span className="bg-gradient-to-r from-emerald-400 to-teal-400 bg-clip-text text-transparent">Security</span></h2>
          </motion.div>

          <div className="grid gap-6 sm:grid-cols-2 lg:grid-cols-4">
            {[
              { icon: Lock, title: "AES-256 Encryption", desc: "Data encrypted at rest and in transit with TLS 1.3. HSM-managed keys." },
              { icon: Users, title: "SAML / OAuth 2.0 SSO", desc: "Enterprise single sign-on with role-based access control." },
              { icon: Clock, title: "Immutable Audit Trail", desc: "Every change logged with user ID, timestamp, and diff. Tamper-proof." },
              { icon: ShieldCheck, title: "SOC 2 / HIPAA", desc: "Type II compliance roadmap with BAAs for enterprise accounts." },
            ].map((item, i) => (
              <motion.div
                key={item.title}
                initial={{ opacity: 0, y: 30 }}
                whileInView={{ opacity: 1, y: 0 }}
                viewport={{ once: true }}
                transition={{ delay: i * 0.1, duration: 0.5 }}
                whileHover={{ y: -4 }}
                className="group rounded-2xl border border-slate-700/50 bg-slate-800/50 p-6 text-center backdrop-blur-sm hover:bg-slate-700/50 transition-colors"
              >
                <div className="mx-auto mb-5 flex h-14 w-14 items-center justify-center rounded-2xl bg-gradient-to-br from-emerald-500/20 to-teal-500/20 text-emerald-400 border border-emerald-500/20 group-hover:from-emerald-500 group-hover:to-teal-500 group-hover:text-white transition-all duration-300">
                  <item.icon className="h-7 w-7" />
                </div>
                <h3 className="mb-2 text-base font-bold text-white">{item.title}</h3>
                <p className="text-sm text-slate-400">{item.desc}</p>
              </motion.div>
            ))}
          </div>
        </div>
      </section>

      {/* ════════════════════════════════════════════
          TECH STACK + PRICING
          ════════════════════════════════════════════ */}
      <section className="py-24 bg-gradient-to-b from-white to-slate-50">
        <div className="mx-auto max-w-7xl px-4 md:px-6">
          <motion.div className="mb-16 text-center" {...fadeUp}>
            <h2 className="text-3xl font-black text-slate-900">Built on the <GradientText>DClaw Stack</GradientText></h2>
          </motion.div>
          <div className="flex flex-wrap items-center justify-center gap-3">
            {["FastAPI", "SQLAlchemy 2.0", "Pydantic v2", "PostgreSQL + pgvector", "Redis", "Celery", "Next.js 14", "Tailwind CSS", "Framer Motion", "Docker", "Kubernetes", "OpenAI / LLMs"].map((tag, i) => (
              <motion.span
                key={tag}
                initial={{ opacity: 0, scale: 0.8 }}
                whileInView={{ opacity: 1, scale: 1 }}
                viewport={{ once: true }}
                transition={{ delay: i * 0.05 }}
                whileHover={{ scale: 1.05, y: -2 }}
                className="rounded-xl border border-slate-200/80 bg-white px-5 py-2.5 text-sm font-bold text-slate-700 shadow-sm hover:border-blue-300 hover:text-blue-600 hover:shadow-md transition-all cursor-default"
              >
                {tag}
              </motion.span>
            ))}
          </div>
        </div>
      </section>

      {/* ════════════════════════════════════════════
          CTA — KINETIC
          ════════════════════════════════════════════ */}
      <section className="relative overflow-hidden bg-gradient-to-br from-slate-900 via-indigo-950 to-slate-900 py-28 text-white">
        <FloatingOrb className="top-0 left-1/4 h-[500px] w-[500px] bg-blue-500/10" delay={0} />
        <FloatingOrb className="bottom-0 right-1/4 h-[400px] w-[400px] bg-violet-500/10" delay={3} />
        <div className="pointer-events-none absolute inset-0 bg-[radial-gradient(ellipse_60%_50%_at_50%_50%,rgba(59,130,246,0.12),transparent)]" />

        <div className="relative mx-auto max-w-4xl px-4 text-center">
          <motion.div
            initial={{ opacity: 0, y: 30 }}
            whileInView={{ opacity: 1, y: 0 }}
            viewport={{ once: true }}
            transition={{ duration: 0.6 }}
          >
            <h2 className="text-4xl font-black md:text-5xl lg:text-6xl">
              Ready to Protect<br />
              <span className="bg-gradient-to-r from-blue-400 via-indigo-400 to-violet-400 bg-clip-text text-transparent">Your Innovations?</span>
            </h2>
            <p className="mx-auto mt-6 max-w-xl text-lg text-slate-400">
              Join 500+ IP teams using DClaw Patent. Start free — no credit card required.
            </p>
            <div className="mt-10 flex flex-col items-center justify-center gap-4 sm:flex-row">
              <Button size="lg" className="gap-3 bg-gradient-to-r from-blue-600 to-indigo-600 text-white text-lg font-bold px-10 py-7 shadow-2xl shadow-blue-500/30 hover:shadow-blue-500/50 transition-all hover:scale-[1.02]">
                Start Free Trial <ArrowRight className="h-5 w-5" />
              </Button>
              <Button variant="outline" size="lg" className="text-lg font-bold px-10 py-7 border-2 border-slate-600 text-slate-300 hover:border-white hover:text-white hover:bg-white/5 transition-all">
                Talk to Sales
              </Button>
            </div>
            <div className="mt-6 text-sm text-slate-500">
              Free for individuals · Team plans from $49/user/month
            </div>
          </motion.div>
        </div>
      </section>

      {/* ════════════════════════════════════════════
          FOOTER
          ════════════════════════════════════════════ */}
      <footer className="border-t border-slate-200/80 bg-white pb-8 pt-16">
        <div className="mx-auto max-w-7xl px-4 md:px-6">
          <div className="grid gap-12 md:grid-cols-4 mb-12">
            <div>
              <div className="flex items-center gap-2.5 mb-4">
                <div className="flex h-8 w-8 items-center justify-center rounded-lg bg-gradient-to-br from-blue-600 to-indigo-600 text-white">
                  <Sparkles className="h-4 w-4" />
                </div>
                <span className="text-lg font-black text-slate-900">DClaw <span className="text-blue-600">Patent</span></span>
              </div>
              <p className="text-sm text-slate-500 leading-relaxed">
                AI-powered patent management and IP portfolio automation for modern legal teams.
              </p>
            </div>
            <div>
              <h4 className="font-bold text-slate-900 mb-4">Product</h4>
              <ul className="space-y-2.5 text-sm text-slate-500">
                {["Features", "Pricing", "Security", "API Docs", "Changelog"].map((l) => (
                  <li key={l}><a href="#" className="hover:text-blue-600 transition-colors">{l}</a></li>
                ))}
              </ul>
            </div>
            <div>
              <h4 className="font-bold text-slate-900 mb-4">Company</h4>
              <ul className="space-y-2.5 text-sm text-slate-500">
                {["About", "Blog", "Careers", "Contact", "Press"].map((l) => (
                  <li key={l}><a href="#" className="hover:text-blue-600 transition-colors">{l}</a></li>
                ))}
              </ul>
            </div>
            <div>
              <h4 className="font-bold text-slate-900 mb-4">Legal</h4>
              <ul className="space-y-2.5 text-sm text-slate-500">
                {["Privacy Policy", "Terms of Service", "Cookie Policy", "GDPR"].map((l) => (
                  <li key={l}><a href="#" className="hover:text-blue-600 transition-colors">{l}</a></li>
                ))}
              </ul>
            </div>
          </div>
          <div className="flex flex-col md:flex-row items-center justify-between gap-4 border-t border-slate-100 pt-8">
            <div className="text-sm text-slate-400">
              © 2026 DClaw Patent. Built by Udai Kiran — udai.kiran@oneconvergence.com
            </div>
            <div className="flex gap-4">
              <a href="#" className="rounded-full bg-slate-100 p-2 text-slate-400 hover:bg-blue-50 hover:text-blue-600 transition-colors"><Github className="h-4 w-4" /></a>
              <a href="#" className="rounded-full bg-slate-100 p-2 text-slate-400 hover:bg-blue-50 hover:text-blue-600 transition-colors"><Twitter className="h-4 w-4" /></a>
              <a href="#" className="rounded-full bg-slate-100 p-2 text-slate-400 hover:bg-blue-50 hover:text-blue-600 transition-colors"><Mail className="h-4 w-4" /></a>
            </div>
          </div>
        </div>
      </footer>
    </div>
  )
}
