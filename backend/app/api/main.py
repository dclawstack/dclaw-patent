from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.core.config import settings
from app.core.database import init_db
from app.api.routes import health


@asynccontextmanager
async def lifespan(app: FastAPI):
    await init_db()
    yield


app = FastAPI(
    title=settings.app_name,
    version="1.0.0",
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(health.router, prefix="/health", tags=["health"])

# Wire v1 routers
from app.api.v1 import patents, dockets, disclosures, ai

app.include_router(patents.router, prefix="/api/v1")
app.include_router(dockets.router, prefix="/api/v1")
app.include_router(disclosures.router, prefix="/api/v1")
app.include_router(ai.router, prefix="/api/v1")
