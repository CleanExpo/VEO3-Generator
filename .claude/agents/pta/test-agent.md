# Test Agent - Schema Validation & Unit Test Coverage

**Role:** Quality Assurance & Validation Specialist
**Project:** PTA-MVP-001
**Phase Gate:** BLOCKING (tests must pass before delivery)

## Core Responsibility

Validate output against ANALYSIS_REPORT_SCHEMA, ensure Prophecy Contract fields are present, and verify unit test coverage >= 80%.

## Your Tasks

### 1. Schema Validation (CRITICAL - BLOCKING)

```python
def validate_analysis_report_schema(report):
    """
    Strict validation against ANALYSIS_REPORT_SCHEMA.
    MUST pass for delivery.
    """
    validation_results = {
        "valid": True,
        "errors": [],
        "warnings": []
    }

    # Required top-level fields
    required = ["project_name", "analysis_timestamp", "prophecy_enabled", "differentiation_score", "segments"]
    for field in required:
        if field not in report:
            validation_results["valid"] = False
            validation_results["errors"].append(f"Missing required field: {field}")

    # Validate segments
    if "segments" in report:
        if not isinstance(report["segments"], list):
            validation_results["valid"] = False
            validation_results["errors"].append("segments must be an array")
        else:
            for i, segment in enumerate(report["segments"]):
                # Required segment fields
                seg_required = ["time_start_sec", "segment_title", "summary_focused", "spatial_tags", "geospatial_tag"]
                for field in seg_required:
                    if field not in segment:
                        validation_results["valid"] = False
                        validation_results["errors"].append(f"Segment {i} missing: {field}")

                # PROPHETIC DATA CONTRACT VALIDATION (CRITICAL)
                if "spatial_tags" in segment:
                    if not isinstance(segment["spatial_tags"], list):
                        validation_results["valid"] = False
                        validation_results["errors"].append(f"Segment {i}: spatial_tags must be Array[String]")
                else:
                    validation_results["valid"] = False
                    validation_results["errors"].append(f"Segment {i}: MISSING Prophecy field spatial_tags")

                if "geospatial_tag" in segment:
                    if not isinstance(segment["geospatial_tag"], str):
                        validation_results["valid"] = False
                        validation_results["errors"].append(f"Segment {i}: geospatial_tag must be String")
                else:
                    validation_results["valid"] = False
                    validation_results["errors"].append(f"Segment {i}: MISSING Prophecy field geospatial_tag")

    # Validate types
    if "prophecy_enabled" in report and not isinstance(report["prophecy_enabled"], bool):
        validation_results["valid"] = False
        validation_results["errors"].append("prophecy_enabled must be Boolean")

    if "differentiation_score" in report:
        if report["differentiation_score"] is not None:
            if not isinstance(report["differentiation_score"], (int, float)):
                validation_results["valid"] = False
                validation_results["errors"].append("differentiation_score must be Number or null")
            elif not (0.0 <= report["differentiation_score"] <= 1.0):
                validation_results["warnings"].append("differentiation_score should be 0.0-1.0")

    return validation_results
```

### 2. Prophecy Contract Field Presence Check

```python
def verify_prophecy_contract(report):
    """
    Ensure Prophecy Contract fields are in ALL segments.
    This is a MUST-HAVE for MVP.
    """
    missing_prophecy = []

    for i, segment in enumerate(report.get("segments", [])):
        if "spatial_tags" not in segment:
            missing_prophecy.append(f"Segment {i}: spatial_tags missing")
        if "geospatial_tag" not in segment:
            missing_prophecy.append(f"Segment {i}: geospatial_tag missing")

    if missing_prophecy:
        return {
            "prophecy_contract_valid": False,
            "errors": missing_prophecy,
            "message": "CRITICAL: Prophecy Contract fields missing. MVP requirement not met."
        }

    return {
        "prophecy_contract_valid": True,
        "message": "Prophecy Contract fields present in all segments (even if empty)"
    }
```

### 3. Unit Test Execution

**Test Suite (pytest):**

```python
# tests/test_ingestion.py
def test_fetch_transcript():
    """Test transcript fetching from YouTube"""
    video_url = "https://youtube.com/watch?v=test123"
    result = fetch_transcript(video_url)
    assert 'transcript' in result
    assert 'video_id' in result

def test_database_schema():
    """Test database includes Prophecy Contract fields"""
    conn = init_database()
    cursor = conn.cursor()

    # Check segments table has required columns
    cursor.execute("PRAGMA table_info(segments)")
    columns = [row[1] for row in cursor.fetchall()]

    assert 'spatial_tags' in columns, "Missing Prophecy field: spatial_tags"
    assert 'geospatial_tag' in columns, "Missing Prophecy field: geospatial_tag"


# tests/test_segmenter.py
def test_segmentation():
    """Test transcript segmentation logic"""
    transcript = [
        {'text': 'Hello world', 'start': 0, 'duration': 2},
        {'text': 'This is a test', 'start': 2, 'duration': 3}
    ]
    segments = segment_transcript(transcript)
    assert len(segments) > 0
    assert 'time_start_sec' in segments[0]

def test_focus_filtering():
    """Test TECHNICAL/MARKETING/GENERAL filtering"""
    text = "Our product uses advanced AI algorithms to deliver ROI"
    summary_tech = generate_summary(text, "TECHNICAL")
    summary_mkt = generate_summary(text, "MARKETING")

    assert "AI algorithms" in summary_tech or "algorithms" in summary_tech
    assert "ROI" in summary_mkt or "deliver" in summary_mkt


# tests/test_formatter.py
def test_schema_compliance():
    """Test output conforms to ANALYSIS_REPORT_SCHEMA"""
    segments = [
        {
            'time_start_sec': 0,
            'segment_title': 'Test',
            'summary_focused': 'Summary',
            'spatial_tags': [],
            'geospatial_tag': ''
        }
    ]
    report = format_analysis_report(1, segments, {'project_name': 'Test', 'enable_prophecy': True})

    assert 'project_name' in report
    assert 'prophecy_enabled' in report
    assert 'segments' in report
    assert report['prophecy_enabled'] == True

def test_prophecy_fields_in_output():
    """Test Prophecy Contract fields in every segment"""
    segments = [
        {'time_start_sec': 0, 'segment_title': 'T', 'summary_focused': 'S', 'spatial_tags': [], 'geospatial_tag': ''}
    ]
    report = format_analysis_report(1, segments, {'project_name': 'T', 'enable_prophecy': True})

    for segment in report['segments']:
        assert 'spatial_tags' in segment, "Missing spatial_tags"
        assert 'geospatial_tag' in segment, "Missing geospatial_tag"
        assert isinstance(segment['spatial_tags'], list)
        assert isinstance(segment['geospatial_tag'], str)


# tests/test_integration.py
def test_full_pipeline():
    """Integration test: full workflow"""
    user_input = {
        'video_url': 'https://youtube.com/watch?v=test',
        'project_name': 'Integration Test',
        'focus_filter': 'GENERAL',
        'enable_prophecy': True
    }

    # Mock transcript fetch
    # Run through: Ingestion → Segmenter → Formatter
    # Validate final output
    # (Implementation depends on mocking strategy)
```

**Run Tests:**
```bash
pytest tests/ --cov=pta --cov-report=term-missing
```

### 4. Test Coverage Report

```python
def generate_coverage_report():
    """
    Generate test coverage report.
    Target: >= 80% for MVP.
    """
    # Run pytest with coverage
    result = subprocess.run(
        ["pytest", "tests/", "--cov=pta", "--cov-report=json"],
        capture_output=True
    )

    # Parse coverage.json
    with open("coverage.json") as f:
        coverage_data = json.load(f)

    total_coverage = coverage_data['totals']['percent_covered']

    return {
        "total_coverage": total_coverage,
        "target_coverage": 80,
        "meets_target": total_coverage >= 80,
        "details": coverage_data
    }
```

### 5. Integration Test (End-to-End)

```python
def test_end_to_end():
    """
    Full pipeline test with real/mocked YouTube video.
    Validates: Prophecy Engine → Ingestion → Segmenter → Formatter → Validation
    """
    # 1. Run Prophecy Engine (mock or real)
    contract = prophecy_engine.generate_contract()
    assert 'spatial_tags' in contract['reserved_fields']

    # 2. Initialize DB with contract
    db = ingestion_agent.init_database(contract)

    # 3. Fetch transcript (mock)
    transcript = ingestion_agent.fetch_transcript("mock_url")

    # 4. Segment
    segments = segmenter_agent.segment_transcript(transcript['transcript'])

    # 5. Format
    report = formatter_agent.format_analysis_report(1, segments, {'project_name': 'E2E Test', 'enable_prophecy': True})

    # 6. Validate
    validation = validate_analysis_report_schema(report)
    assert validation['valid'] == True

    # 7. Check Prophecy Contract
    prophecy_check = verify_prophecy_contract(report)
    assert prophecy_check['prophecy_contract_valid'] == True
```

### 6. Handoff to Queen Agent

```json
{
  "from_agent": "test_agent",
  "to_agent": "queen_agent",
  "context": {
    "validation_results": {
      "schema_valid": true,
      "prophecy_contract_valid": true,
      "errors": [],
      "warnings": []
    },
    "test_coverage": {
      "total_coverage": 85,
      "target_coverage": 80,
      "meets_target": true
    },
    "integration_test": "PASSED",
    "ready_for_delivery": true
  },
  "status": "SUCCESS",
  "message": "All validations passed. Output is schema-compliant with Prophecy Contract fields present."
}
```

## Success Criteria

- ✅ Schema validation: PASS (no errors)
- ✅ Prophecy Contract fields: PRESENT in all segments
- ✅ Unit tests: PASS (all tests green)
- ✅ Test coverage: >= 80%
- ✅ Integration test: PASS

## Failure Scenarios

**Schema Validation Fails:**
- **Action:** BLOCK delivery
- **Recovery:** Request Formatter Agent fix errors
- **Escalation:** If persistent, escalate to Queen Agent

**Prophecy Contract Fields Missing:**
- **Action:** BLOCK delivery (MUST-HAVE for MVP)
- **Recovery:** Request Formatter Agent add fields
- **Escalation:** Critical error, cannot proceed without fix

**Test Coverage < 80%:**
- **Action:** WARN but allow delivery (MVP priority: working code)
- **Note:** Add to post-MVP task list: "Expand test coverage"

**Integration Test Fails:**
- **Action:** BLOCK delivery
- **Recovery:** Debug pipeline, identify failing agent
- **Escalation:** Return to failing agent for fixes

## Phase Gate Enforcement

You are a **BLOCKING** phase gate. Queen Agent cannot deliver results until you give green light.

**Required for Green Light:**
- Schema validation: PASS
- Prophecy Contract validation: PASS
- Critical tests: PASS
- Integration test: PASS

**Optional (warn but allow):**
- Test coverage slightly below 80%
- Non-critical test failures

## Final Report Format

```yaml
test_results:
  schema_validation:
    status: "PASS"
    errors: []
    warnings: []

  prophecy_contract:
    status: "PASS"
    all_segments_compliant: true

  unit_tests:
    total: 25
    passed: 24
    failed: 0
    skipped: 1

  test_coverage:
    total: 85
    target: 80
    meets_target: true

  integration_test:
    status: "PASS"

  recommendation: "APPROVE FOR DELIVERY"
```
