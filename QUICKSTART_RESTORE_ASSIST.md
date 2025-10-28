# Quick Start: Restore Assist Integration

Your Restore Assist GPT methodology is now integrated with VEO3!

## What This Gives You

- **4x8-second platform-ready videos** (just like Restore Assist)
- **VEO3 consistency controls** (no more appearance changes between segments)
- **Questionnaire-driven workflow** (same easy input method)
- **Multi-platform export** (Instagram, TikTok, LinkedIn, YouTube Shorts)

## Setup (5 minutes)

1. Add your Google API key to .env
2. Install dependencies: pip install -r requirements.txt
3. Run example: python example_sop_video.py

## Three Ways to Use

### 1. Run the Example
```bash
python example_sop_video.py
```
Generates a complete product demo SOP video (4 segments x 8 seconds)

### 2. Use a Template
```python
from src.sop_questionnaire import QuestionnaireBuilder

builder = QuestionnaireBuilder()
questionnaire = builder.quick_template("product_demo")
# Customize and generate
```

Templates: product_demo, how_to, training, announcement

### 3. Interactive Builder
```bash
python example_sop_video.py interactive
```
Guides you through creating custom questionnaires

## Key Files

- `src/sop_questionnaire.py` - Questionnaire system
- `src/sop_translator.py` - Converts to VEO3 prompts
- `example_sop_video.py` - Complete examples
- `.claude/agents/sop-video-builder.md` - SOP agent workflow

## The Workflow

```
Your Input          VEO3 Output
-----------        --------------
Questionnaire  →   Segment 1 (8s)
(4 segments)   →   Segment 2 (8s)
                →   Segment 3 (8s)
                →   Segment 4 (8s)
                →   Full Video (32s)
                →   Platform versions
```

## Consistency Guarantees

Unlike standard VEO3, this integration ensures:
- Presenter looks identical in ALL segments
- Location never changes
- Lighting stays consistent
- Brand colors preserved
- No hallucinations between cuts

## Platform Export

Automatically creates versions for:
- Instagram (16:9, 9:16, 1:1)
- TikTok (9:16)
- YouTube Shorts (9:16)  
- LinkedIn (16:9)

## Example: Product Demo

See `example_sop_video.py` for a complete working example.

The questionnaire asks for:
- Project title and purpose
- Presenter description (locked for all segments)
- Location description (locked for all segments)
- 4 segment descriptions (8s each)
- Brand colors
- Target platforms

Then it generates consistent, professional videos ready to post!

## Next Steps

1. Run: python example_sop_video.py
2. Review generated prompts (see how questionnaire translates)
3. Create your own SOP video with your product/service
4. Export for your target platforms

Your Restore Assist methodology + VEO3 consistency = Perfect SOP videos every time!
