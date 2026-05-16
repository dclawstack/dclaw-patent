import pytest
from datetime import datetime, timezone
from httpx import AsyncClient


@pytest.mark.asyncio
async def test_create_prior_art(client: AsyncClient):
    patent_payload = {
        "patent_number": "US-PA-01",
        "title": "Prior Art Patent",
        "abstract": "Abstract.",
        "claims": ["Claim 1"],
        "filing_date": datetime(2024, 1, 15, tzinfo=timezone.utc).isoformat(),
        "status": "filed",
        "applicant": "PA Corp",
        "jurisdiction": "US",
    }
    patent_resp = await client.post("/api/v1/patents", json=patent_payload)
    patent_id = patent_resp.json()["id"]

    pa_payload = {
        "patent_id": str(patent_id),
        "source_patent_number": "US-5555555",
        "source_title": "Similar Quantum Device",
        "relevance_score": 0.85,
        "claim_mapping": {"1": ["1", "2"], "2": ["3"]},
        "analysis_notes": "Strong overlap in claims 1-2",
    }
    response = await client.post("/api/v1/prior-art", json=pa_payload)
    assert response.status_code == 201
    data = response.json()
    assert data["source_patent_number"] == "US-5555555"
    assert data["relevance_score"] == 0.85
    assert data["patent_id"] == str(patent_id)


@pytest.mark.asyncio
async def test_list_prior_art_by_patent(client: AsyncClient):
    patent_payload = {
        "patent_number": "US-PA-02",
        "title": "Prior Art Patent 2",
        "abstract": "Abstract.",
        "claims": ["Claim 1"],
        "filing_date": datetime(2024, 1, 15, tzinfo=timezone.utc).isoformat(),
        "status": "filed",
        "applicant": "PA Corp 2",
        "jurisdiction": "US",
    }
    patent_resp = await client.post("/api/v1/patents", json=patent_payload)
    patent_id = patent_resp.json()["id"]

    for i in range(3):
        pa_payload = {
            "patent_id": str(patent_id),
            "source_patent_number": f"US-600000{i}",
            "source_title": f"Prior Art {i}",
            "relevance_score": 0.5 + i * 0.1,
        }
        await client.post("/api/v1/prior-art", json=pa_payload)

    response = await client.get(f"/api/v1/prior-art?patent_id={patent_id}")
    assert response.status_code == 200
    data = response.json()
    assert data["total"] == 3


@pytest.mark.asyncio
async def test_update_prior_art(client: AsyncClient):
    patent_payload = {
        "patent_number": "US-PA-03",
        "title": "Prior Art Patent 3",
        "abstract": "Abstract.",
        "claims": ["Claim 1"],
        "filing_date": datetime(2024, 1, 15, tzinfo=timezone.utc).isoformat(),
        "status": "filed",
        "applicant": "PA Corp 3",
        "jurisdiction": "US",
    }
    patent_resp = await client.post("/api/v1/patents", json=patent_payload)
    patent_id = patent_resp.json()["id"]

    pa_payload = {
        "patent_id": str(patent_id),
        "source_patent_number": "US-7777777",
        "source_title": "Original Title",
        "relevance_score": 0.6,
    }
    pa_resp = await client.post("/api/v1/prior-art", json=pa_payload)
    pa_id = pa_resp.json()["id"]

    update = {"relevance_score": 0.95, "analysis_notes": "Updated after detailed review"}
    response = await client.put(f"/api/v1/prior-art/{pa_id}", json=update)
    assert response.status_code == 200
    data = response.json()
    assert data["relevance_score"] == 0.95
    assert data["analysis_notes"] == "Updated after detailed review"


@pytest.mark.asyncio
async def test_delete_prior_art(client: AsyncClient):
    patent_payload = {
        "patent_number": "US-PA-04",
        "title": "Prior Art Patent 4",
        "abstract": "Abstract.",
        "claims": ["Claim 1"],
        "filing_date": datetime(2024, 1, 15, tzinfo=timezone.utc).isoformat(),
        "status": "filed",
        "applicant": "PA Corp 4",
        "jurisdiction": "US",
    }
    patent_resp = await client.post("/api/v1/patents", json=patent_payload)
    patent_id = patent_resp.json()["id"]

    pa_payload = {
        "patent_id": str(patent_id),
        "source_patent_number": "US-8888888",
        "source_title": "Delete Me",
        "relevance_score": 0.3,
    }
    pa_resp = await client.post("/api/v1/prior-art", json=pa_payload)
    pa_id = pa_resp.json()["id"]

    response = await client.delete(f"/api/v1/prior-art/{pa_id}")
    assert response.status_code == 204

    get_resp = await client.get(f"/api/v1/prior-art/{pa_id}")
    assert get_resp.status_code == 404
