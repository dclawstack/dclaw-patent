# DClaw Patent API Documentation

**Base URL:** `http://localhost:8000/api/v1`

**Version:** 1.0.0

---

## Authentication

Currently, endpoints use query parameters for user context:
- `user_id`: Unique user identifier
- `user_name`: User's display name
- `user_email`: User's email address

Future versions will use Bearer token authentication.

---

## Endpoints by Category

### Patents

#### List Patents
```
GET /patents?skip=0&limit=20&status=draft&search=battery
```

**Query Parameters:**
- `skip` (int): Pagination offset (default: 0)
- `limit` (int): Items per page (default: 20)
- `status` (string): Filter by status (draft, filed, prosecution, issued, abandoned)
- `search` (string): Full-text search in title/abstract/claims
- `jurisdiction` (string): Filter by jurisdiction

**Response:**
```json
{
  "patents": [
    {
      "id": "uuid",
      "title": "Battery Technology",
      "status": "filed",
      "filing_date": "2024-01-15",
      "publication_date": "2024-07-15",
      "issue_date": null,
      "abstract": "...",
      "jurisdiction": "US",
      "inventors": ["John Doe", "Jane Smith"],
      "created_at": "2024-01-15T10:00:00Z"
    }
  ],
  "total": 42
}
```

#### Create Patent
```
POST /patents
```

**Request Body:**
```json
{
  "title": "Battery Technology",
  "abstract": "Novel lithium-ion battery design",
  "claims": "1. A battery comprising...",
  "filing_date": "2024-01-15",
  "jurisdiction": "US",
  "inventors": ["inventor@example.com"]
}
```

#### Get Patent
```
GET /patents/{patent_id}
```

#### Update Patent
```
PUT /patents/{patent_id}
```

#### Delete Patent
```
DELETE /patents/{patent_id}
```

---

### Dockets

#### List Dockets
```
GET /dockets?status=pending&jurisdiction=US&patent_id=uuid&event_type=office_action&due_date_from=2024-01-01&due_date_to=2024-12-31
```

**Query Parameters:**
- `status` (string): pending, completed, overdue
- `jurisdiction` (string): US, EP, JP, CN, IN, etc.
- `patent_id` (uuid): Filter by patent
- `event_type` (string): office_action, maintenance_fee, response_deadline, etc.
- `due_date_from` (date): Start of date range
- `due_date_to` (date): End of date range
- `skip` (int): Pagination offset
- `limit` (int): Items per page

#### Get Overdue Dockets
```
GET /dockets/overdue
```

**Response:**
```json
[
  {
    "id": "uuid",
    "patent_id": "uuid",
    "event_type": "office_action",
    "due_date": "2024-01-15",
    "jurisdiction": "US",
    "status": "pending",
    "description": "Office action response required",
    "auto_generated": true,
    "created_at": "2024-01-14T10:00:00Z"
  }
]
```

#### Get Upcoming Dockets
```
GET /dockets/upcoming?days_ahead=30
```

Returns dockets due in the next N days (for urgency-colored dashboard).

#### Create Docket
```
POST /dockets
```

**Request Body:**
```json
{
  "patent_id": "uuid",
  "event_type": "office_action",
  "due_date": "2024-06-15",
  "jurisdiction": "US",
  "description": "Office action response required"
}
```

#### Mark Docket Complete
```
POST /dockets/{docket_id}/mark-complete
```

#### Mark Docket Pending
```
POST /dockets/{docket_id}/mark-pending
```

#### Export Dockets to CSV
```
GET /dockets/export/csv?jurisdiction=US&status=pending
```

Returns CSV file download.

#### Export Dockets to iCal
```
GET /dockets/export/ical?jurisdiction=US
```

Returns `.ics` file for calendar apps (Google Calendar, Outlook, etc.).

---

### Legal Automation

#### Analyze Office Action
```
POST /legal-automation/analyze-office-action
```

**Request Body:**
```json
{
  "text": "Office action document text or base64-encoded PDF content",
  "jurisdiction": "US"
}
```

**Response:**
```json
{
  "action_type": "first examination report",
  "deadline": "2024-06-15T00:00:00Z",
  "rejections": [
    {
      "claims": [1, 2, 3],
      "reason": "obvious under 35 U.S.C. § 103"
    }
  ],
  "requirements": [
    "Provide detailed explanation of amendments",
    "Submit IDS per 37 CFR 1.98"
  ]
}
```

#### Get Maintenance Fees
```
GET /legal-automation/maintenance-fees/{patent_id}?jurisdiction=US
```

**Response:**
```json
{
  "patent_id": "uuid",
  "issue_date": "2024-01-15",
  "jurisdiction": "US",
  "fees": [
    {
      "due_date": "2027-06-15",
      "grace_period_end": "2027-12-15",
      "amount": "$1,600 (small entity: $800)",
      "year": "Year 3"
    },
    {
      "due_date": "2031-06-15",
      "grace_period_end": "2031-12-15",
      "amount": "$3,200 (small entity: $1,600)",
      "year": "Year 7"
    },
    {
      "due_date": "2035-06-15",
      "grace_period_end": "2035-12-15",
      "amount": "$4,800 (small entity: $2,400)",
      "year": "Year 11"
    }
  ]
}
```

#### Schedule Reminders
```
POST /legal-automation/schedule-reminders/{patent_id}
```

**Request Body:**
```json
{
  "due_date": "2024-06-15T00:00:00Z"
}
```

#### Get Reminders for Deadline
```
POST /legal-automation/get-reminders
```

**Request Body:**
```json
{
  "due_date": "2024-06-15T00:00:00Z"
}
```

---

### Webhooks (Office Action Ingestion)

#### Ingest Office Action
```
POST /webhooks/office-action
```

**Request Body:**
```json
{
  "patent_id": "uuid",
  "jurisdiction": "US",
  "document_content": "base64:... or raw text",
  "document_source": "USPTO",
  "external_reference_id": "2024-01-12345"
}
```

**Response:**
```json
{
  "success": true,
  "patent_id": "uuid",
  "action_type": "first examination report",
  "docket_created": true,
  "docket_id": "uuid",
  "deadline": "2024-06-15T00:00:00Z",
  "rejections_count": 3,
  "requirements_count": 2,
  "message": "Office action parsed — Docket created with deadline 2024-06-15"
}
```

#### Get Office Action History
```
GET /webhooks/office-action/{patent_id}/history
```

**Response:**
```json
{
  "patent_id": "uuid",
  "office_actions": [
    {
      "id": "uuid",
      "due_date": "2024-06-15",
      "description": "first examination report - Provide detailed explanation of amendments",
      "status": "pending",
      "created_at": "2024-01-15T10:00:00Z",
      "auto_generated": true
    }
  ],
  "total_count": 1
}
```

---

### AI Services

#### Patent Search
```
POST /ai/patent-search?q=lithium battery
```

Returns similar patents from USPTO/EPO databases using semantic search.

#### Draft Claims
```
POST /ai/draft-claims
```

**Request Body:**
```json
{
  "disclosure_id": "uuid"
}
```

#### Draft Abstract
```
POST /ai/draft-abstract
```

#### Quality Score
```
POST /ai/quality-score
```

---

### Collaboration

#### Create Comment
```
POST /collaboration
```

**Request Body:**
```json
{
  "text": "This claim could be stronger",
  "patent_id": "uuid",
  "parent_id": null,
  "mentions": ["john@example.com"]
}
```

**Query Parameters:**
- `user_id` (required)
- `user_name` (required)
- `user_email` (required)

#### Get Comment Replies
```
GET /collaboration/{comment_id}/replies
```

#### Get User Mentions
```
GET /collaboration/mentions/{user_email}?unread_only=true&limit=20
```

---

## Error Responses

### 400 Bad Request
```json
{
  "detail": "Invalid jurisdiction. Supported: US, EP, JP, CN, IN"
}
```

### 404 Not Found
```json
{
  "detail": "Patent not found"
}
```

### 500 Server Error
```json
{
  "detail": "Internal server error"
}
```

---

## Rate Limiting

- Patent search: 10 requests/minute per user
- AI operations: 5 requests/minute per user
- General endpoints: 100 requests/minute per user

---

## Async Operations

Long-running operations (AI claim drafting, patent search) are async:

1. Submit request → Returns `job_id`
2. Poll `/jobs/{job_id}` for status
3. Retrieve results when status == "completed"

---

## Webhooks

### Office Action Webhook
Receives POST requests from USPTO/EPO when office actions are available.

```
POST /webhooks/office-action
```

Example payload:
```json
{
  "patent_id": "uuid",
  "jurisdiction": "US",
  "document_url": "https://uspto.gov/office-action/12345",
  "received_at": "2024-01-15T10:00:00Z"
}
```

---

## Integration Examples

### Python
```python
import requests

BASE_URL = "http://localhost:8000/api/v1"

# List patents
response = requests.get(
    f"{BASE_URL}/patents",
    params={"status": "filed", "skip": 0, "limit": 20}
)
patents = response.json()

# Create docket
docket_data = {
    "patent_id": "...",
    "event_type": "office_action",
    "due_date": "2024-06-15",
    "jurisdiction": "US"
}
response = requests.post(f"{BASE_URL}/dockets", json=docket_data)
docket = response.json()

# Mark complete
requests.post(f"{BASE_URL}/dockets/{docket['id']}/mark-complete")
```

### JavaScript
```javascript
const BASE_URL = 'http://localhost:8000/api/v1';

// Get overdue dockets
const response = await fetch(`${BASE_URL}/dockets/overdue`);
const dockets = await response.json();

// Export to CSV
window.location.href = `${BASE_URL}/dockets/export/csv`;
```

---

## Deployment

See `DEPLOYMENT.md` for Docker, Kubernetes, and CI/CD setup.
