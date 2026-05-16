import pytest
from datetime import datetime, timezone, timedelta
from httpx import AsyncClient


@pytest.mark.asyncio
async def test_create_docket(client: AsyncClient):
    # Seed patent first
    patent_payload = {
        "patent_number": "US-DOC-01",
        "title": "Docket Patent",
        "abstract": "Abstract.",
        "claims": ["Claim 1"],
        "filing_date": datetime(2024, 1, 15, tzinfo=timezone.utc).isoformat(),
        "status": "filed",
        "applicant": "Docket Corp",
        "jurisdiction": "US",
    }
    patent_resp = await client.post("/api/v1/patents", json=patent_payload)
    patent_id = patent_resp.json()["id"]

    docket_payload = {
        "patent_id": str(patent_id),
        "event_type": "response_due",
        "due_date": (datetime.now(timezone.utc) + timedelta(days=10)).isoformat(),
        "description": "Office action response due",
        "status": "pending",
        "assignee": "Attorney A",
    }
    response = await client.post("/api/v1/dockets", json=docket_payload)
    assert response.status_code == 201
    data = response.json()
    assert data["event_type"] == "response_due"
    assert data["patent_id"] == str(patent_id)


@pytest.mark.asyncio
async def test_list_dockets_by_patent(client: AsyncClient):
    patent_payload = {
        "patent_number": "US-DOC-02",
        "title": "Docket Patent 2",
        "abstract": "Abstract.",
        "claims": ["Claim 1"],
        "filing_date": datetime(2024, 1, 15, tzinfo=timezone.utc).isoformat(),
        "status": "filed",
        "applicant": "Docket Corp 2",
        "jurisdiction": "US",
    }
    patent_resp = await client.post("/api/v1/patents", json=patent_payload)
    patent_id = patent_resp.json()["id"]

    for i in range(3):
        docket_payload = {
            "patent_id": str(patent_id),
            "event_type": "maintenance_fee",
            "due_date": (datetime.now(timezone.utc) + timedelta(days=30 + i)).isoformat(),
            "description": f"Maintenance fee {i}",
            "status": "pending",
        }
        await client.post("/api/v1/dockets", json=docket_payload)

    response = await client.get(f"/api/v1/dockets?patent_id={patent_id}")
    assert response.status_code == 200
    data = response.json()
    assert data["total"] == 3


@pytest.mark.asyncio
async def test_update_docket(client: AsyncClient):
    patent_payload = {
        "patent_number": "US-DOC-03",
        "title": "Docket Patent 3",
        "abstract": "Abstract.",
        "claims": ["Claim 1"],
        "filing_date": datetime(2024, 1, 15, tzinfo=timezone.utc).isoformat(),
        "status": "filed",
        "applicant": "Docket Corp 3",
        "jurisdiction": "US",
    }
    patent_resp = await client.post("/api/v1/patents", json=patent_payload)
    patent_id = patent_resp.json()["id"]

    docket_payload = {
        "patent_id": str(patent_id),
        "event_type": "custom",
        "due_date": (datetime.now(timezone.utc) + timedelta(days=5)).isoformat(),
        "description": "Custom event",
        "status": "pending",
    }
    docket_resp = await client.post("/api/v1/dockets", json=docket_payload)
    docket_id = docket_resp.json()["id"]

    update = {"status": "completed", "assignee": "Paralegal B"}
    response = await client.put(f"/api/v1/dockets/{docket_id}", json=update)
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "completed"
    assert data["assignee"] == "Paralegal B"


@pytest.mark.asyncio
async def test_delete_docket(client: AsyncClient):
    patent_payload = {
        "patent_number": "US-DOC-04",
        "title": "Docket Patent 4",
        "abstract": "Abstract.",
        "claims": ["Claim 1"],
        "filing_date": datetime(2024, 1, 15, tzinfo=timezone.utc).isoformat(),
        "status": "filed",
        "applicant": "Docket Corp 4",
        "jurisdiction": "US",
    }
    patent_resp = await client.post("/api/v1/patents", json=patent_payload)
    patent_id = patent_resp.json()["id"]

    docket_payload = {
        "patent_id": str(patent_id),
        "event_type": "filing",
        "due_date": (datetime.now(timezone.utc) + timedelta(days=1)).isoformat(),
        "description": "Filing deadline",
        "status": "pending",
    }
    docket_resp = await client.post("/api/v1/dockets", json=docket_payload)
    docket_id = docket_resp.json()["id"]

    response = await client.delete(f"/api/v1/dockets/{docket_id}")
    assert response.status_code == 204

    get_resp = await client.get(f"/api/v1/dockets/{docket_id}")
    assert get_resp.status_code == 404


@pytest.mark.asyncio
async def test_docket_alerts(client: AsyncClient):
    patent_payload = {
        "patent_number": "US-DOC-05",
        "title": "Docket Patent 5",
        "abstract": "Abstract.",
        "claims": ["Claim 1"],
        "filing_date": datetime(2024, 1, 15, tzinfo=timezone.utc).isoformat(),
        "status": "filed",
        "applicant": "Docket Corp 5",
        "jurisdiction": "US",
    }
    patent_resp = await client.post("/api/v1/patents", json=patent_payload)
    patent_id = patent_resp.json()["id"]

    # Create overdue event
    overdue_payload = {
        "patent_id": str(patent_id),
        "event_type": "response_due",
        "due_date": (datetime.now(timezone.utc) - timedelta(days=5)).isoformat(),
        "description": "Overdue response",
        "status": "pending",
    }
    await client.post("/api/v1/dockets", json=overdue_payload)

    # Create upcoming event
    upcoming_payload = {
        "patent_id": str(patent_id),
        "event_type": "maintenance_fee",
        "due_date": (datetime.now(timezone.utc) + timedelta(days=7)).isoformat(),
        "description": "Upcoming fee",
        "status": "pending",
    }
    await client.post("/api/v1/dockets", json=upcoming_payload)

    response = await client.get("/api/v1/dockets/alerts/summary?days=30")
    assert response.status_code == 200
    data = response.json()
    assert len(data["urgent"]) >= 1
    assert len(data["upcoming"]) >= 1
