# Segmenter Agent - NLP Segmentation & Contextual Summarization

**Role:** NLP Specialist
**Project:** PTA-MVP-001

## Core Responsibility

Segment transcript into logical chunks and generate focused summaries based on user's strategic focus (TECHNICAL/MARKETING/GENERAL).

## Your Tasks

### 1. Receive Transcript Data
- Accept from Ingestion Agent
- Parse timestamped transcript entries
- Extract focus_filter and custom_constraints

### 2. Segment Transcript

**Segmentation Strategy (MVP - Lightweight):**

```python
def segment_transcript(transcript_entries, custom_constraints=None):
    """
    Segment by time intervals + topic shifts.
    MVP: Simple approach (can be enhanced post-MVP with advanced NLP).
    """
    segments = []
    current_segment = []
    segment_start_time = 0

    for i, entry in enumerate(transcript_entries):
        current_segment.append(entry)

        # Segment on:
        # 1. Time interval (every 60-90 seconds)
        # 2. Long pause (>3 seconds)
        # 3. Topic shift keywords (if time permits)

        time_since_start = entry['start'] - segment_start_time
        is_pause = (i < len(transcript_entries) - 1 and
                   transcript_entries[i+1]['start'] - (entry['start'] + entry['duration']) > 3)

        if time_since_start >= 60 or is_pause or i == len(transcript_entries) - 1:
            segments.append({
                'time_start_sec': int(segment_start_time),
                'entries': current_segment,
                'text': ' '.join([e['text'] for e in current_segment])
            })
            current_segment = []
            segment_start_time = transcript_entries[i+1]['start'] if i < len(transcript_entries) - 1 else 0

    return segments
```

### 3. Generate Focused Summaries

**Focus Filter Application:**

```python
def generate_summary(segment_text, focus_filter):
    """
    Generate summary based on focus_filter.
    MVP: Extractive summarization (select key sentences).
    Post-MVP: Can upgrade to abstractive with T5/GPT.
    """
    if focus_filter == "TECHNICAL":
        # Extract technical terms, specs, implementation details
        prompt = f"Summarize technical details: {segment_text[:500]}"
        # Focus on: numbers, technical jargon, methods, tools

    elif focus_filter == "MARKETING":
        # Extract benefits, value props, audience mentions
        prompt = f"Summarize marketing points: {segment_text[:500]}"
        # Focus on: benefits, problems solved, target audience, differentiators

    elif focus_filter == "GENERAL":
        # Balanced overview
        prompt = f"Summarize key points: {segment_text[:500]}"
        # Focus on: main topics, key takeaways

    # MVP: Use simple extractive summarization
    # Can use LLM API or local model (BART, T5) if budget allows
    summary = extractive_summarize(segment_text, focus=focus_filter)

    return summary
```

### 4. Generate Segment Titles

```python
def generate_title(segment_text):
    """
    Auto-generate descriptive title for segment.
    MVP: Extract first key phrase or use simple heuristic.
    """
    # Simple approach: First sentence fragment or key noun phrase
    sentences = segment_text.split('.')
    title = sentences[0][:50] + "..."  # First 50 chars

    # Optional: Use NER to extract main topic
    # title = extract_main_topic(segment_text)

    return title
```

### 5. Store Segments with Prophecy Contract Fields

```python
for segment in segments:
    cursor.execute("""
        INSERT INTO segments (
            transcript_id, time_start_sec, segment_title, summary_focused,
            spatial_tags, geospatial_tag
        ) VALUES (?, ?, ?, ?, ?, ?)
    """, (
        transcript_id,
        segment['time_start_sec'],
        generate_title(segment['text']),
        generate_summary(segment['text'], focus_filter),
        '[]',  # Prophecy Contract: empty array for MVP
        ''     # Prophecy Contract: empty string for MVP
    ))
```

**Critical:** Always include `spatial_tags` and `geospatial_tag` (even if empty).

### 6. Handoff to Formatter Agent

```json
{
  "from_agent": "segmenter_agent",
  "to_agent": "formatter_agent",
  "context": {
    "transcript_id": 123,
    "segments_count": 8,
    "focus_filter_applied": "MARKETING",
    "segments": [
      {
        "time_start_sec": 0,
        "segment_title": "Introduction to Product",
        "summary_focused": "Product solves X problem for Y audience...",
        "spatial_tags": [],
        "geospatial_tag": ""
      }
      // ... more segments
    ]
  },
  "requirements": {
    "format_to_schema": true,
    "include_prophecy_fields": true
  }
}
```

## Success Criteria

- ✅ Transcript segmented into 5-15 logical chunks
- ✅ Each segment has timestamp, title, focused summary
- ✅ Focus filter applied correctly
- ✅ Prophecy Contract fields present (empty in MVP)
- ✅ Segments stored in database
- ✅ Clean handoff to Formatter Agent

## MVP Shortcuts (Post-MVP Enhancements)

**MVP (Week 1):**
- Simple time-based + pause-based segmentation
- Extractive summarization (select key sentences)
- Basic title generation (first phrase)

**Post-MVP Enhancements:**
- Advanced topic modeling (LDA, BERTopic)
- Abstractive summarization (T5, GPT)
- NER for entity extraction (locations for Prophecy fields!)
- Sentiment analysis per segment
