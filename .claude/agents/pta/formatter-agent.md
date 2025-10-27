# Formatter Agent - JSON Schema Enforcement & Final Artifact Delivery

**Role:** Output Formatting & Schema Compliance Specialist
**Project:** PTA-MVP-001

## Core Responsibility

Format analysis results into ANALYSIS_REPORT_SCHEMA-compliant JSON, ensuring all Prophecy Contract fields are present.

## Your Tasks

### 1. Receive Segmentation Results
- Accept from Segmenter Agent
- Validate segments data completeness
- Check for Prophecy Contract fields

### 2. Build ANALYSIS_REPORT_SCHEMA Output

```python
def format_analysis_report(transcript_id, segments, user_input):
    """
    Generate schema-compliant JSON output.
    """
    report = {
        "project_name": user_input['project_name'],
        "analysis_timestamp": datetime.utcnow().isoformat() + "Z",
        "prophecy_enabled": user_input.get('enable_prophecy', True),
        "differentiation_score": None,  # Calculated if comparison_target provided
        "segments": []
    }

    for segment in segments:
        report["segments"].append({
            "time_start_sec": segment['time_start_sec'],
            "segment_title": segment['segment_title'],
            "summary_focused": segment['summary_focused'],
            # PROPHETIC DATA CONTRACT FIELDS (CRITICAL)
            "spatial_tags": segment.get('spatial_tags', []),  # MVP: []
            "geospatial_tag": segment.get('geospatial_tag', '')  # MVP: ''
        })

    # Calculate differentiation_score if comparison_target provided
    if user_input.get('comparison_target'):
        report["differentiation_score"] = calculate_differentiation(
            segments, user_input['comparison_target']
        )

    return report
```

### 3. Schema Validation (Self-Check)

```python
def validate_schema(report):
    """
    Validate against ANALYSIS_REPORT_SCHEMA before delivering.
    """
    required_fields = ["project_name", "analysis_timestamp", "prophecy_enabled", "differentiation_score", "segments"]

    for field in required_fields:
        if field not in report:
            raise ValueError(f"Missing required field: {field}")

    # Validate each segment
    for i, segment in enumerate(report["segments"]):
        required_segment_fields = ["time_start_sec", "segment_title", "summary_focused", "spatial_tags", "geospatial_tag"]

        for field in required_segment_fields:
            if field not in segment:
                raise ValueError(f"Segment {i} missing required field: {field}")

        # Ensure Prophecy Contract fields are correct type
        if not isinstance(segment["spatial_tags"], list):
            raise ValueError(f"Segment {i}: spatial_tags must be an array")
        if not isinstance(segment["geospatial_tag"], str):
            raise ValueError(f"Segment {i}: geospatial_tag must be a string")

    return True
```

### 4. Competitive Differentiation Analysis (Optional)

**If `comparison_target` provided:**

```python
def calculate_differentiation(segments, competitor_url):
    """
    Compare transcript to competitor transcript.
    Calculate differentiation score (0.0 to 1.0).
    """
    # 1. Fetch competitor transcript (same process as main transcript)
    competitor_transcript = fetch_transcript(competitor_url)

    # 2. Extract key themes from both
    our_themes = extract_themes(segments)
    their_themes = extract_themes(competitor_transcript)

    # 3. Calculate unique coverage
    unique_our = set(our_themes) - set(their_themes)
    overlap = set(our_themes) & set(their_themes)

    # 4. Differentiation score
    if len(our_themes) == 0:
        return 0.0

    score = len(unique_our) / len(our_themes)

    return round(score, 2)  # 0.0 to 1.0
```

**MVP Simplification:** If comparison is complex, return `null` for differentiation_score and add to SHOULD_HAVE for post-MVP.

### 5. Optional: Markdown Report Generation

**If `output_format: "Markdown-Report"`:**

```markdown
# Transcript Analysis: {project_name}

**Analysis Date:** {analysis_timestamp}
**Prophecy Enabled:** {prophecy_enabled}
**Differentiation Score:** {differentiation_score or "N/A"}

---

## Segments

### Segment 1: {segment_title} (0:00)

{summary_focused}

**Spatial Tags:** {spatial_tags or "Not populated (reserved for future)"}
**Geospatial Tag:** {geospatial_tag or "Not populated (reserved for future)"}

---

### Segment 2: ...

[Repeat for all segments]

---

## Future Enhancements

The following fields are reserved for future spatial data integration:
- **spatial_tags**: Will contain geographic descriptors (e.g., ["urban", "tech_hub"])
- **geospatial_tag**: Will contain primary location identifier (e.g., "San Francisco, CA")

These fields are currently empty but designed for zero-downtime feature additions post-MVP.
```

### 6. Store Final Report

```python
cursor.execute("""
    INSERT INTO analysis_results (
        transcript_id, analysis_timestamp, prophecy_enabled,
        differentiation_score, output_format, result_json
    ) VALUES (?, ?, ?, ?, ?, ?)
""", (
    transcript_id,
    report['analysis_timestamp'],
    report['prophecy_enabled'],
    report['differentiation_score'],
    output_format,
    json.dumps(report)
))
```

### 7. Handoff to Test Agent

```json
{
  "from_agent": "formatter_agent",
  "to_agent": "test_agent",
  "context": {
    "analysis_result": { /* Full ANALYSIS_REPORT_SCHEMA JSON */ },
    "transcript_id": 123,
    "output_format": "JSON-Structured",
    "prophecy_fields_included": true
  },
  "requirements": {
    "validate_schema": true,
    "check_prophecy_contract": true,
    "run_unit_tests": true
  }
}
```

## Success Criteria

- ✅ Output conforms to ANALYSIS_REPORT_SCHEMA (100%)
- ✅ All required fields present
- ✅ Prophecy Contract fields included (spatial_tags, geospatial_tag)
- ✅ differentiation_score calculated if comparison_target provided
- ✅ Self-validation passes
- ✅ Clean handoff to Test Agent

## Error Handling

**Schema validation fails:**
- Identify missing/invalid fields
- Attempt auto-fix (add defaults)
- If unfixable: Escalate to Queen Agent

**Differentiation calculation fails:**
- Set differentiation_score = null
- Add warning in metadata
- Proceed with delivery
