# Architecture

## Overview

DClaw Patent follows the standard DClaw app architecture:

```
┌─────────────┐     ┌─────────────┐     ┌─────────────┐
│  Frontend   │────▶│   Backend   │────▶│  Database   │
│  (Next.js)  │     │  (FastAPI)  │     │ (PostgreSQL)│
└─────────────┘     └─────────────┘     └─────────────┘
```

## Components

### Frontend

- **Framework:** Next.js 14.2.28
- **Styling:** Tailwind CSS
- **UI Components:** Custom design system
- **State:** React hooks + Context

### Backend

- **Framework:** FastAPI
- **ORM:** SQLAlchemy 2.0
- **Database:** PostgreSQL + asyncpg
- **Settings:** pydantic-settings

### Infrastructure

- **Container:** Docker
- **Orchestration:** Kubernetes via DClaw Operator
- **Database:** CloudNativePG
- **Ingress:** nginx-ingress + cert-manager

---
> **Document Owner:** Udai Kiran | **Email:** udai.kiran@oneconvergence.com
> **Last Modified:** 2026-05-16 | **Admin Tracking:** Active
