import pytest
from datetime import datetime, timezone
from httpx import AsyncClient


@pytest.mark.asyncio
async def test_create_patent(client: AsyncClient):
    payload = {
        "patent_number": "US1234567",
        "title": "Quantum Error Correction",
        "abstract": "A method for quantum error correction using surface codes.",
        "claims": ["1. A quantum computing device comprising..."],
        "description": "Detailed description of the invention.",
        "filing_date": datetime(2024, 1, 15, tzinfo=timezone.utc).isoformat(),
        "status": "filed",
        "applicant": "ACME Corp",
        "inventors": ["Alice Smith", "Bob Jones"],
        "technology_category": "quantum_computing",
        "jurisdiction": "US",
    }
    response = await client.post("/api/v1/patents", json=payload)
    assert response.status_code == 201
    data = response.json()
    assert data["patent_number"] == "US1234567"
    assert data["title"] == "Quantum Error Correction"
    assert data["id"] is not None


@pytest.mark.asyncio
async def test_create_patent_duplicate_number(client: AsyncClient):
    payload = {
        "patent_number": "US-DUP-001",
        "title": "Test Patent",
        "abstract": "Abstract.",
        "claims": ["Claim 1"],
        "filing_date": datetime(2024, 1, 15, tzinfo=timezone.utc).isoformat(),
        "status": "filed",
        "applicant": "Test Corp",
        "jurisdiction": "US",
    }
    response = await client.post("/api/v1/patents", json=payload)
    assert response.status_code == 201
    response2 = await client.post("/api/v1/patents", json=payload)
    assert response2.status_code == 409


@pytest.mark.asyncio
async def test_list_patents(client: AsyncClient):
    # Seed a patent
    payload = {
        "patent_number": "US-LIST-01",
        "title": "Listed Patent",
        "abstract": "Abstract text.",
        "claims": ["Claim 1"],
        "filing_date": datetime(2024, 2, 1, tzinfo=timezone.utc).isoformat(),
        "status": "issued",
        "applicant": "Seeder Inc",
        "jurisdiction": "US",
    }
    await client.post("/api/v1/patents", json=payload)

    response = await client.get("/api/v1/patents")
    assert response.status_code == 200
    data = response.json()
    assert data["total"] >= 1
    assert len(data["items"]) >= 1


@pytest.mark.asyncio
async def test_get_patent(client: AsyncClient):
    payload = {
        "patent_number": "US-GET-01",
        "title": "Get Patent",
        "abstract": "Abstract.",
        "claims": ["Claim 1"],
        "filing_date": datetime(2024, 3, 1, tzinfo=timezone.utc).isoformat(),
        "status": "filed",
        "applicant": "Getter Corp",
        "jurisdiction": "US",
    }
    create_resp = await client.post("/api/v1/patents", json=payload)
    patent_id = create_resp.json()["id"]

    response = await client.get(f"/api/v1/patents/{patent_id}")
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == patent_id
    assert data["patent_number"] == "US-GET-01"


@pytest.mark.asyncio
async def test_update_patent(client: AsyncClient):
    payload = {
        "patent_number": "US-UPD-01",
        "title": "Old Title",
        "abstract": "Abstract.",
        "claims": ["Claim 1"],
        "filing_date": datetime(2024, 4, 1, tzinfo=timezone.utc).isoformat(),
        "status": "filed",
        "applicant": "Updater Corp",
        "jurisdiction": "US",
    }
    create_resp = await client.post("/api/v1/patents", json=payload)
    patent_id = create_resp.json()["id"]

    update = {"title": "New Title", "status": "issued"}
    response = await client.put(f"/api/v1/patents/{patent_id}", json=update)
    assert response.status_code == 200
    data = response.json()
    assert data["title"] == "New Title"
    assert data["status"] == "issued"


@pytest.mark.asyncio
async def test_delete_patent(client: AsyncClient):
    payload = {
        "patent_number": "US-DEL-01",
        "title": "Delete Me",
        "abstract": "Abstract.",
        "claims": ["Claim 1"],
        "filing_date": datetime(2024, 5, 1, tzinfo=timezone.utc).isoformat(),
        "status": "filed",
        "applicant": "Deleter Corp",
        "jurisdiction": "US",
    }
    create_resp = await client.post("/api/v1/patents", json=payload)
    patent_id = create_resp.json()["id"]

    response = await client.delete(f"/api/v1/patents/{patent_id}")
    assert response.status_code == 204

    get_resp = await client.get(f"/api/v1/patents/{patent_id}")
    assert get_resp.status_code == 404


@pytest.mark.asyncio
async def test_filter_patents_by_status(client: AsyncClient):
    for i, status in enumerate(["filed", "issued", "abandoned"]):
        payload = {
            "patent_number": f"US-FIL-{i}",
            "title": f"Patent {status}",
            "abstract": "Abstract.",
            "claims": ["Claim 1"],
            "filing_date": datetime(2024, 6, 1, tzinfo=timezone.utc).isoformat(),
            "status": status,
            "applicant": "Filter Corp",
            "jurisdiction": "US",
        }
        await client.post("/api/v1/patents", json=payload)

    response = await client.get("/api/v1/patents?status=issued")
    assert response.status_code == 200
    data = response.json()
    for item in data["items"]:
        if item["patent_number"].startswith("US-FIL-"):
            assert item["status"] == "issued"
