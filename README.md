# VEO3 Consistency Generator

A production-ready orchestration framework for generating consistent videos using Google VEO3 with specialized AI agent coordination.

## 🎯 NEW: Restore Assist Integration

This system now includes full integration with the **Restore Assist methodology** for building platform-ready SOP videos!

- **4×8-second segments**: Create professional 32-second videos optimized for social media
- **Questionnaire-driven**: Simple input → professional output
- **Perfect consistency**: No appearance changes between segments
- **Multi-platform export**: Instagram, TikTok, LinkedIn, YouTube Shorts ready

**Quick Start**: See [QUICKSTART_RESTORE_ASSIST.md](QUICKSTART_RESTORE_ASSIST.md) or run `python example_sop_video.py`

## Features

### Consistency Controls
- **Character Tracking**: Maintain consistent character appearance, clothing, and features across scenes
- **Location Tracking**: Ensure spatial and environmental continuity
- **Voice Tracking**: Maintain voice consistency (if supported by VEO3)
- **Lighting Tracking**: Keep lighting and color palette consistent
- **Style Tracking**: Preserve visual style and cinematography across sequences

### Hallucination Reduction
- Prompt validation before generation
- Reference checking against scene requirements
- Continuity validation between scenes
- Automatic retry with prompt adjustments
- Pattern detection for common hallucination types

### AI Agent Orchestration
- **Research Agent**: Gathers VEO3 best practices and API documentation
- **VEO3 Prompt Engineer**: Crafts optimized, consistent prompts
- **VEO3 Continuity Tracker**: Tracks scene-to-scene state and consistency
- **VEO3 Validator**: Validates outputs and detects hallucinations
- **Coder Agent**: Implements generation logic
- **Integrator Agent**: Finalizes and compiles sequences
- **Stuck Agent**: Handles edge cases and escalations

## Installation

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd VEO3-Consistency-Generator
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Configure environment**
   ```bash
   cp .env.example .env
   # Edit .env and add your GOOGLE_API_KEY
   ```

4. **Verify installation**
   ```bash
   python -m src.config
   ```

## Quick Start

### Generate a Single Video

```python
from src.config import VEO3Config
from src.veo3_client import VEO3Client, VideoGenerationRequest

# Load configuration
config = VEO3Config.from_env()

# Initialize client
client = VEO3Client(config)

# Create generation request
request = VideoGenerationRequest(
    prompt="A serene sunset over a calm ocean, warm golden light, cinematic",
    duration=5,
    scene_id="scene_001"
)

# Generate video
response = client.generate_video(request)

if response.success:
    print(f"Video generated: {response.video_path}")
else:
    print(f"Generation failed: {response.error}")
```

### Generate a Sequence with Continuity

```python
# Example coming soon - see documentation
```

## Configuration

### Environment Variables

Create a `.env` file with the following:

```env
# Required
GOOGLE_API_KEY=your_google_api_key_here

# Optional (with defaults)
VEO3_MODEL=veo-3
VEO3_CONSISTENCY_MODE=strict
VEO3_DEFAULT_DURATION=5
VEO3_RESOLUTION=1080p
VEO3_FPS=24
VEO3_ASPECT_RATIO=16:9
OUTPUT_DIR=./output/videos
METADATA_DIR=./data/metadata
LOG_LEVEL=INFO
```

### Consistency Modes

- **strict**: Maximum consistency enforcement, minimal variation
- **balanced**: Balance between consistency and creative variation
- **creative**: Allow more creative variation while maintaining core elements

## Project Structure

```
VEO3-Consistency-Generator/
├── .claude/                    # Orchestrator configuration
│   ├── agents/                 # Agent definitions
│   │   ├── veo3-prompt-engineer.md
│   │   ├── veo3-continuity-tracker.md
│   │   └── veo3-validator.md
│   ├── config.yaml             # Orchestrator config
│   └── claude.md               # Orchestration flow
├── src/                        # Source code
│   ├── config.py               # Configuration management
│   ├── veo3_client.py          # VEO3 API client
│   ├── continuity_tracker.py  # Continuity tracking
│   └── validator.py            # Validation logic
├── data/                       # Data storage
│   └── metadata/               # Scene metadata
├── output/                     # Generated videos
│   └── videos/
├── tests/                      # Test suite
├── .env.example                # Environment template
├── requirements.txt            # Python dependencies
└── README.md                   # This file
```

## Usage Examples

### Basic Video Generation

```python
# See Quick Start section
```

### Multi-Scene Sequence

```python
# Coming soon
```

### Handling Hallucinations

The system automatically detects and handles hallucinations:

1. **Detection**: VEO3 Validator identifies inconsistencies
2. **Analysis**: Stuck Agent analyzes patterns
3. **Correction**: Prompt Engineer refines prompts
4. **Retry**: System regenerates with improved prompts
5. **Validation**: Re-validation ensures consistency

## Troubleshooting

### Common Issues

**API Key Not Found**
```
Error: GOOGLE_API_KEY environment variable is required
Solution: Set your API key in .env file
```

**Generation Timeout**
```
Error: Generation timeout
Solution: Increase timeout in config or check API status
```

**Consistency Violations**
```
Error: Continuity validation failed
Solution: Review continuity tracker logs and adjust prompts
```

## Development

### Running Tests

```bash
pytest tests/
```

### Adding Custom Agents

1. Create agent definition in `.claude/agents/your-agent.md`
2. Add agent configuration to `.claude/config.yaml`
3. Implement agent logic in `src/agents/`

## Roadmap

- [ ] Advanced continuity tracking with computer vision
- [ ] Automated scene segmentation
- [ ] Multi-model support (beyond VEO3)
- [ ] Real-time validation during generation
- [ ] Web interface for video management
- [ ] Batch processing for large sequences
- [ ] Advanced hallucination pattern library

## Contributing

Contributions are welcome! Please:

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Submit a pull request

## License

[Add your license here]

## Support

For issues and questions:
- GitHub Issues: [repository-url]/issues
- Documentation: [docs-url]

## Acknowledgments

- Built with the Drop-In-Claude-Orchestrator framework
- Powered by Google VEO3
- Agent coordination by Claude Code
