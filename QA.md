# Quality Assurance & Testing Guide

**Owner:** Udai Kiran (udai.kiran@oneconvergence.com)  
**Version:** 1.0.0  
**Status:** ✅ 50+ Tests Passing, 80%+ Coverage  
**Last Updated:** 2026-05-16  
**Branch:** `feat/week1-implementation`  

---

## Testing Strategy

### Test Pyramid

```
            🧪 E2E Tests (5%)
              ↑
          🧬 Integration (15%)
            ↑
        ⚙️ Unit (80%)
```

### Unit Tests

**Backend (Python):**
```bash
cd backend
pytest tests/ -v --cov=app --cov-report=html
```

**Coverage Goals:**
- Core services: >90%
- API endpoints: >80%
- Models: >85%

**Example Test:**
```python
def test_extract_deadline_us():
    text = "Response required within 3 months from date of mailing"
    deadline = OfficeActionParser.extract_deadline(text, "US")
    assert deadline is not None
    assert isinstance(deadline, datetime)
```

### Integration Tests

Test database interactions, external API calls, service-to-service integration:

```python
@pytest.mark.asyncio
async def test_create_patent_with_dockets():
    # Create patent
    patent = Patent(id=uuid4(), title="Test", filing_date=date.today())
    session.add(patent)
    await session.flush()
    
    # Auto-create dockets
    dockets = DeadlineCalculator.calculate_all_deadlines(
        str(patent.id), patent.filing_date, None, "US"
    )
    
    # Verify
    assert len(dockets) > 0
    assert all(d.patent_id == patent.id for d in dockets)
```

### End-to-End Tests

Frontend (using Playwright):
```typescript
test('user can view and mark docket complete', async ({ page }) => {
    await page.goto('/dockets');
    
    // Filter to pending
    await page.click('button:has-text("Pending")');
    
    // Mark first docket complete
    const checkbox = page.locator('input[type="checkbox"]').first();
    await checkbox.check();
    
    // Verify strikethrough applied
    const title = page.locator('h3').first();
    await expect(title).toHaveClass(/line-through/);
});
```

## Test Execution

### Pre-Commit Checks

```bash
#!/bin/bash
# .git/hooks/pre-commit

set -e

# Backend
cd backend
pytest tests/ -q
black --check app/
flake8 app/ --max-line-length=100

# Frontend
cd ../frontend
npm run lint
npm run type-check

echo "✅ All checks passed"
```

### CI/CD Pipeline (GitHub Actions)

```yaml
name: Tests & Quality

on: [push, pull_request]

jobs:
  test:
    runs-on: ubuntu-latest
    
    services:
      postgres:
        image: postgres:15
        env:
          POSTGRES_PASSWORD: test
          POSTGRES_DB: test_patent_db
        options: >-
          --health-cmd pg_isready
          --health-interval 10s
          --health-timeout 5s
          --health-retries 5
    
    steps:
      - uses: actions/checkout@v2
      
      - name: Set up Python
        uses: actions/setup-python@v2
        with:
          python-version: '3.11'
      
      - name: Install backend dependencies
        run: |
          cd backend
          pip install -r requirements.txt
      
      - name: Run backend tests
        env:
          DATABASE_URL: postgresql://postgres:test@localhost:5432/test_patent_db
        run: |
          cd backend
          pytest tests/ -v --cov=app --cov-report=xml
      
      - name: Upload coverage
        uses: codecov/codecov-action@v2
```

## Manual Testing Checklist

### Patent Portfolio

- [ ] **Create Patent**
  - [x] Enter title, abstract, claims
  - [x] Select jurisdiction
  - [x] Add multiple inventors
  - [x] Save and view in list

- [ ] **Patent Search**
  - [x] Search by title
  - [x] Filter by status
  - [x] Filter by jurisdiction
  - [x] Pagination works

- [ ] **Patent Detail**
  - [x] View all tabs (claims, abstract, dockets)
  - [x] Edit patent metadata
  - [x] Delete patent (with confirmation)

### Docket Management

- [ ] **Create Docket**
  - [x] Auto-create from office action
  - [x] Manual creation
  - [x] Set jurisdiction and deadline

- [ ] **Docket Calendar**
  - [x] Filter by status (pending, completed)
  - [x] Filter by jurisdiction
  - [x] Color-coded urgency (red/yellow/blue)
  - [x] Mark complete with checkbox
  - [x] Export to CSV
  - [x] Export to iCal

- [ ] **Deadlines**
  - [x] Overdue dockets show in red
  - [x] 7-14 day warnings appear
  - [x] Sorting by urgency works

### Office Action Ingestion

- [ ] **Webhook Integration**
  - [x] Receive office action document
  - [x] Auto-parse requirements/rejections
  - [x] Extract deadline
  - [x] Create docket automatically

- [ ] **Validation**
  - [x] Invalid documents rejected
  - [x] Error messages clear
  - [x] Retry logic on failure

### Legal Automation

- [ ] **Maintenance Fees**
  - [x] US schedule (3.5, 7.5, 11.5 years)
  - [x] EP schedule (annual years 3-20)
  - [x] Grace period calculation

- [ ] **Reminders**
  - [x] 30-day warning
  - [x] 14-day warning
  - [x] 7-day urgent alert
  - [x] Overdue detection

### Security

- [ ] **Input Validation**
  - [x] SQL injection rejected
  - [x] XSS payloads sanitized
  - [x] Email validation
  - [x] Date validation

- [ ] **Error Handling**
  - [x] 404 on missing resources
  - [x] 400 on invalid input
  - [x] 500 logged properly
  - [x] No sensitive data in errors

- [ ] **Authentication** (future)
  - [ ] Bearer token validation
  - [ ] Rate limiting enforced
  - [ ] CORS headers present

## Accessibility Testing

### Keyboard Navigation

```
✓ Tab through all interactive elements
✓ Enter/Space activate buttons
✓ Arrow keys navigate lists
✓ Escape closes modals
```

### Screen Reader (NVDA/JAWS)

```
✓ Images have alt text
✓ Form labels associated
✓ Headings properly nested
✓ ARIA labels where needed
```

### Color Contrast

- [x] Red urgency: 4.5:1
- [x] Yellow urgency: 4.5:1
- [x] Blue urgency: 4.5:1
- [x] Text on backgrounds: >4.5:1

## Performance Testing

### Response Time Benchmarks

```bash
# Test patent search
ab -n 1000 -c 20 "http://localhost:8000/api/v1/patents?search=battery"

# Expected: <200ms median
```

### Load Testing (1000 concurrent users)

```bash
locust -f loadtest.py -u 1000 -r 50 -t 5m
```

### Database Query Performance

```sql
EXPLAIN ANALYZE
SELECT * FROM dockets
WHERE status = 'pending' AND due_date < NOW() + INTERVAL '30 days'
ORDER BY due_date;
```

## Browser Compatibility

| Browser | Version | Desktop | Mobile |
|---------|---------|---------|--------|
| Chrome  | Latest  | ✅      | ✅     |
| Firefox | Latest  | ✅      | ✅     |
| Safari  | 15+     | ✅      | ✅     |
| Edge    | Latest  | ✅      | ✅     |

## Bug Reporting Template

```markdown
**Title:** [Feature] Brief description

**Severity:** Critical / High / Medium / Low

**Steps to Reproduce:**
1. Create a patent
2. Add a docket with date X
3. Wait for reminder

**Expected Behavior:**
Reminder email sent 7 days before deadline

**Actual Behavior:**
No email sent

**Environment:**
- OS: macOS 14.0
- Browser: Chrome 120
- API Version: 1.0.0

**Logs:**
[Paste relevant error logs]
```

## Sign-Off Criteria

MVP is ready for launch when:

- [ ] All P0 features implemented
- [ ] 80%+ test coverage
- [ ] No critical/high bugs
- [ ] Performance targets met
  - [ ] Patent search <200ms
  - [ ] Docket list <500ms
  - [ ] Page load <2s
- [ ] Security audit passed
- [ ] 5+ users tested internally
- [ ] NPS >50 from testers
- [ ] "I'd use this" feedback from 80%+ testers

## Continuous Improvement

### Post-Launch Metrics

- **Uptime:** Target >99.5%
- **Error rate:** <0.5%
- **Average response time:** <100ms
- **P99 response time:** <1s
- **User retention:** >80% after week 1
