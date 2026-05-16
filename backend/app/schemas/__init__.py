from app.schemas.patent import PatentCreate, PatentRead, PatentUpdate, PatentList
from app.schemas.docket import DocketEventCreate, DocketEventRead, DocketEventUpdate, DocketEventList, DocketAlerts
from app.schemas.prior_art import PriorArtCreate, PriorArtRead, PriorArtUpdate, PriorArtList
from app.schemas.ai import (
    PatentSearchRequest,
    PatentSearchResponse,
    PatentSearchResult,
    SimilarPatentsResponse,
    DraftClaimsRequest,
    DraftClaimsResponse,
    DraftedClaim,
    ExaminerPredictionRequest,
    ExaminerPredictionResponse,
)
from app.schemas.competitor_watch import CompetitorWatchCreate, CompetitorWatchRead, CompetitorWatchUpdate, CompetitorWatchList

__all__ = [
    "PatentCreate",
    "PatentRead",
    "PatentUpdate",
    "PatentList",
    "DocketEventCreate",
    "DocketEventRead",
    "DocketEventUpdate",
    "DocketEventList",
    "DocketAlerts",
    "PriorArtCreate",
    "PriorArtRead",
    "PriorArtUpdate",
    "PriorArtList",
    "PatentSearchRequest",
    "PatentSearchResponse",
    "PatentSearchResult",
    "SimilarPatentsResponse",
    "DraftClaimsRequest",
    "DraftClaimsResponse",
    "DraftedClaim",
    "ExaminerPredictionRequest",
    "ExaminerPredictionResponse",
    "CompetitorWatchCreate",
    "CompetitorWatchRead",
    "CompetitorWatchUpdate",
    "CompetitorWatchList",
]
