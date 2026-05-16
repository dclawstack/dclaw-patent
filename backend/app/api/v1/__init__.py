from app.api.v1.patents import router as patents_router
from app.api.v1.dockets import router as dockets_router
from app.api.v1.prior_art import router as prior_art_router
from app.api.v1.competitors import router as competitors_router

__all__ = ["patents_router", "dockets_router", "prior_art_router", "competitors_router"]
