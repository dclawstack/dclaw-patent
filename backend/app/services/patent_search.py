import os
import uuid
from typing import Optional, List
import httpx
import numpy as np
from sqlalchemy import select, text
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.patent import Patent

PATENTSVIEW_BASE = "https://api.patentsview.org/patents/query"
DEFAULT_EMBEDDING_DIM = 768


def _generate_stub_embedding(text: str, dim: int = DEFAULT_EMBEDDING_DIM) -> List[float]:
    """Deterministic stub embedding for dev/testing."""
    rng = np.random.default_rng(abs(hash(text)) % (2**32))
    vec = rng.random(dim).astype(np.float32)
    vec = vec / np.linalg.norm(vec)
    return vec.tolist()


async def _generate_openai_embedding(text: str, dim: int = DEFAULT_EMBEDDING_DIM) -> Optional[List[float]]:
    api_key = os.environ.get("OPENAI_API_KEY")
    if not api_key:
        return None
    try:
        async with httpx.AsyncClient(timeout=30) as client:
            resp = await client.post(
                "https://api.openai.com/v1/embeddings",
                headers={"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"},
                json={"model": "text-embedding-3-large", "dimensions": dim, "input": text[:8000]},
            )
            resp.raise_for_status()
            data = resp.json()
            return data["data"][0]["embedding"]
    except Exception:
        return None


async def generate_embedding(text: str, dim: int = DEFAULT_EMBEDDING_DIM) -> List[float]:
    openai_emb = await _generate_openai_embedding(text, dim)
    if openai_emb:
        return openai_emb
    return _generate_stub_embedding(text, dim)


async def search_patentsview(query: str, limit: int = 20) -> List[dict]:
    """Search USPTO PatentsView API for relevant patents."""
    try:
        async with httpx.AsyncClient(timeout=30) as client:
            payload = {
                "q": {"_or": [{"patent_title": {"_like": f"%{query}%"}}, {"patent_abstract": {"_like": f"%{query}%"}}]},
                "f": ["patent_number", "patent_title", "patent_abstract", "patent_date", "patent_type"],
                "o": {"per_page": limit},
            }
            resp = await client.post(PATENTSVIEW_BASE, json=payload)
            resp.raise_for_status()
            data = resp.json()
            results = []
            for item in data.get("patents", []):
                results.append({
                    "source_patent_number": item.get("patent_number"),
                    "source_title": item.get("patent_title"),
                    "abstract": item.get("patent_abstract"),
                    "date": item.get("patent_date"),
                    "type": item.get("patent_type"),
                    "source": "patentsview",
                })
            return results
    except Exception as e:
        # Return empty on failure so UI doesn't break
        print(f"PatentsView search failed: {e}")
        return []


async def semantic_search_patents(db: AsyncSession, query: str, limit: int = 20) -> List[dict]:
    """Semantic search over local patent embeddings via pgvector."""
    query_embedding = await generate_embedding(query)
    sql = text(
        """
        SELECT id, patent_number, title, abstract, status, jurisdiction,
               embedding <=> :embedding AS distance
        FROM patents
        ORDER BY embedding <=> :embedding
        LIMIT :limit
        """
    )
    result = await db.execute(sql, {"embedding": str(query_embedding), "limit": limit})
    rows = result.mappings().all()
    return [
        {
            "id": str(row["id"]),
            "patent_number": row["patent_number"],
            "title": row["title"],
            "abstract": row["abstract"],
            "status": row["status"],
            "jurisdiction": row["jurisdiction"],
            "distance": float(row["distance"]),
            "source": "semantic",
        }
        for row in rows
    ]


async def find_similar_patents(db: AsyncSession, patent_id: uuid.UUID, limit: int = 10) -> List[dict]:
    """Find patents most similar to a given patent by embedding."""
    result = await db.execute(
        select(Patent.embedding).where(Patent.id == patent_id)
    )
    row = result.scalar_one_or_none()
    if not row:
        return []
    embedding = row if isinstance(row, list) else list(row)
    sql = text(
        """
        SELECT id, patent_number, title, abstract, status, jurisdiction,
               embedding <=> :embedding AS distance
        FROM patents
        WHERE id != :patent_id
        ORDER BY embedding <=> :embedding
        LIMIT :limit
        """
    )
    result = await db.execute(sql, {"embedding": str(embedding), "patent_id": str(patent_id), "limit": limit})
    rows = result.mappings().all()
    return [
        {
            "id": str(row["id"]),
            "patent_number": row["patent_number"],
            "title": row["title"],
            "abstract": row["abstract"],
            "status": row["status"],
            "jurisdiction": row["jurisdiction"],
            "distance": float(row["distance"]),
            "source": "similar",
        }
        for row in rows
    ]
