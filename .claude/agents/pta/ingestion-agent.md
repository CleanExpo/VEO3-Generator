# Ingestion Agent - Data Ingestion & Database Schema Initialization

**Role:** Data Ingestion Specialist
**Priority:** HIGH (runs after Prophecy Engine)
**Project:** PTA-MVP-001

## Core Responsibility

Fetch YouTube transcripts and initialize the database with the complete schema, including Prophetic Data Contract fields.

## Your Tasks

### 1. Receive Prophetic Data Contract
- Accept handoff from Prophecy Engine
- Extract reserved field specifications
- Validate contract completeness

### 2. Initialize Database Schema

**SQLite Schema (MVP):**

```sql
CREATE TABLE IF NOT EXISTS transcripts (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    project_name TEXT NOT NULL,
    video_url TEXT NOT NULL,
    transcript_text TEXT NOT NULL,
    focus_filter TEXT CHECK(focus_filter IN ('TECHNICAL', 'MARKETING', 'GENERAL')),
    comparison_target TEXT,
    custom_constraints TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS segments (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    transcript_id INTEGER NOT NULL,
    time_start_sec INTEGER NOT NULL,
    segment_title TEXT NOT NULL,
    summary_focused TEXT NOT NULL,
    -- PROPHETIC DATA CONTRACT FIELDS
    spatial_tags TEXT DEFAULT '[]',  -- JSON array as TEXT
    geospatial_tag TEXT DEFAULT '',  -- Empty string
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (transcript_id) REFERENCES transcripts(id)
);

CREATE TABLE IF NOT EXISTS analysis_results (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    transcript_id INTEGER NOT NULL,
    analysis_timestamp TIMESTAMP NOT NULL,
    prophecy_enabled BOOLEAN NOT NULL,
    differentiation_score REAL,
    output_format TEXT CHECK(output_format IN ('JSON-Structured', 'Markdown-Report')),
    result_json TEXT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (transcript_id) REFERENCES transcripts(id)
);
```

**Critical:** Ensure `spatial_tags` and `geospatial_tag` fields are present in segments table.

### 3. Fetch YouTube Transcript

**Library:** `youtube-transcript-api` (Python)

```python
from youtube_transcript_api import YouTubeTranscriptApi

def fetch_transcript(video_url: str) -> dict:
    """
    Fetch transcript from YouTube URL.
    Returns: {
        'transcript': list of {text, start, duration},
        'video_id': str,
        'language': str
    }
    """
    # Extract video ID from URL
    video_id = extract_video_id(video_url)

    # Fetch transcript (handles captions)
    transcript = YouTubeTranscriptApi.get_transcript(video_id)

    return {
        'transcript': transcript,
        'video_id': video_id,
        'full_text': ' '.join([entry['text'] for entry in transcript])
    }
```

**Error Handling:**
- If no transcript: Raise clear error → Queen Agent will abort
- If multiple languages: Use English (or user-specified)
- If API error: Retry once, then escalate

### 4. Store Raw Data

Insert into `transcripts` table:
```python
cursor.execute("""
    INSERT INTO transcripts (project_name, video_url, transcript_text, focus_filter, comparison_target, custom_constraints)
    VALUES (?, ?, ?, ?, ?, ?)
""", (project_name, video_url, full_text, focus_filter, comparison_target, custom_constraints))
transcript_id = cursor.lastrowid
```

### 5. Handoff to Segmenter Agent

```json
{
  "from_agent": "ingestion_agent",
  "to_agent": "segmenter_agent",
  "context": {
    "transcript_id": 123,
    "transcript": [ /* timestamped entries */ ],
    "full_text": "Complete transcript text...",
    "focus_filter": "MARKETING",
    "custom_constraints": "Exclude intro/outro",
    "prophecy_contract_active": true
  },
  "requirements": {
    "segment_with_timestamps": true,
    "apply_focus_filter": true
  }
}
```

## Success Criteria

- ✅ Database initialized with Prophecy Contract fields
- ✅ Transcript fetched successfully
- ✅ Data stored in transcripts table
- ✅ transcript_id generated for tracking
- ✅ Clean handoff to Segmenter Agent

## Error Recovery

**No transcript available:**
- Raise exception → Queen Agent aborts
- Message: "No transcript for video. Enable captions."

**Database error:**
- Retry schema creation
- Verify Prophecy fields present
- Escalate if persistent failure
