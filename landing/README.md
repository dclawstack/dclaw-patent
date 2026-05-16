# DClaw Patent — Landing Page

A standalone, Vercel-deployable landing page for **DClaw Patent** — the AI-powered patent management and IP portfolio automation platform.

## What's Included

- **Hero Section** — Animated gradient, stats bar, CTA buttons
- **12 Feature Cards** — Every core feature explained with tags
- **AI Engine Deep Dive** — How RAG, embeddings, and prompting work
- **How It Works** — 6-step visual pipeline (Invention → Grant)
- **Screen-by-Screen Breakdown** — Dashboard, Portfolio, Detail, Disclosure, Search, Docket
- **Enterprise Security** — Encryption, SSO, audit trail, compliance
- **Tech Stack Badges** — FastAPI, Next.js, pgvector, LLMs, etc.
- **CTA + Footer** — Sign-up + ownership attribution

## Deploy to Vercel

### Option 1: Vercel CLI (recommended)

```bash
cd landing
vercel
```

### Option 2: Vercel Git Integration

1. Push this repo to GitHub
2. Import the repo in [Vercel Dashboard](https://vercel.com/new)
3. Set **Root Directory** to `landing`
4. Deploy

### Option 3: Manual Build

```bash
cd landing
npm install
npm run build
# Static export goes to ./dist/
```

> **Note:** `next.config.js` is configured for static export (`output: "export"`) so Vercel serves pre-rendered HTML with zero runtime.

## Project Structure

```
landing/
├── src/
│   ├── app/
│   │   ├── layout.tsx      # Metadata + root layout
│   │   ├── page.tsx        # Full landing page (all sections)
│   │   └── globals.css     # Tailwind + base styles
│   ├── components/
│   │   └── ui/
│   │       └── button.tsx  # Reusable Button component
│   └── lib/
│       └── utils.ts        # cn() helper
├── package.json
├── tailwind.config.ts
├── tsconfig.json
└── next.config.js          # Static export config
```

## Owner

**Udai Kiran** — udai.kiran@oneconvergence.com

---
> **Document Owner:** Udai Kiran | **Email:** udai.kiran@oneconvergence.com
> **Last Modified:** 2026-05-16 | **Admin Tracking:** Active
