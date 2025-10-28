"""
VEO3 Consistency Generator - Web API
FastAPI application for Vercel deployment
"""

from fastapi import FastAPI, HTTPException, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field
from typing import List, Optional, Dict
import os
import sys

# Add parent directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.sop_questionnaire import SOPQuestionnaire, SOPSegment, VideoStyle, PlatformTarget

app = FastAPI(
    title="VEO3 Consistency Generator API",
    description="Generate consistent SOP videos using Google VEO3 with Restore Assist methodology",
    version="1.0.0"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Pydantic models for API
class SegmentRequest(BaseModel):
    segment_number: int = Field(..., ge=1, le=10)
    title: str = Field(..., min_length=1, max_length=100)
    description: str = Field(..., min_length=1, max_length=500)
    key_action: str = Field(..., min_length=1, max_length=200)
    visual_focus: str = Field(..., min_length=1, max_length=200)
    duration: int = Field(default=8, ge=3, le=15)
    text_overlay: Optional[str] = None
    voiceover_script: Optional[str] = None
    props_needed: List[str] = Field(default_factory=list)


class QuestionnaireRequest(BaseModel):
    project_title: str = Field(..., min_length=1, max_length=100)
    sop_purpose: str = Field(..., min_length=1, max_length=500)
    target_audience: str = Field(..., min_length=1, max_length=200)
    video_style: str = Field(default="promotional")
    presenter_type: str = Field(default="person")
    presenter_description: Optional[str] = None
    presenter_clothing: Optional[str] = None
    primary_location: str = Field(default="")
    location_description: str = Field(default="")
    lighting_preference: str = Field(default="bright_professional")
    brand_colors: List[str] = Field(default_factory=list)
    company_name: Optional[str] = None
    target_platforms: List[str] = Field(default_factory=lambda: ["instagram", "tiktok"])
    consistency_mode: str = Field(default="strict")
    segments: List[SegmentRequest]


class QuestionnaireResponse(BaseModel):
    success: bool
    message: str
    questionnaire_id: Optional[str] = None
    segment_count: Optional[int] = None
    total_duration: Optional[int] = None


class PromptResponse(BaseModel):
    success: bool
    prompts: List[Dict]
    total_prompts: int


class StatusResponse(BaseModel):
    status: str
    message: str
    api_configured: bool


# Root endpoint
@app.get("/")
async def root():
    """Root endpoint with API information."""
    return {
        "name": "VEO3 Consistency Generator API",
        "version": "1.0.0",
        "status": "online",
        "description": "Generate consistent SOP videos using Google VEO3",
        "features": [
            "Restore Assist methodology (4×8-second segments)",
            "Questionnaire-driven video generation",
            "Perfect consistency across segments",
            "Multi-platform export",
            "Hallucination detection"
        ],
        "endpoints": {
            "GET /": "API information",
            "GET /health": "Health check",
            "GET /status": "System status and configuration",
            "POST /api/questionnaire/validate": "Validate SOP questionnaire",
            "POST /api/questionnaire/translate": "Translate questionnaire to VEO3 prompts",
            "GET /api/templates": "List available templates",
            "GET /api/templates/{name}": "Get specific template"
        },
        "documentation": "/docs",
        "github": "https://github.com/CleanExpo/VEO3-Generator"
    }


@app.get("/health")
async def health_check():
    """Health check endpoint."""
    return {"status": "healthy", "service": "VEO3 Consistency Generator"}


@app.get("/status", response_model=StatusResponse)
async def get_status():
    """Get system status and configuration."""
    api_key_configured = bool(os.getenv("GOOGLE_API_KEY"))

    return StatusResponse(
        status="operational",
        message="System ready" if api_key_configured else "API key not configured",
        api_configured=api_key_configured
    )


@app.post("/api/questionnaire/validate", response_model=QuestionnaireResponse)
async def validate_questionnaire(request: QuestionnaireRequest):
    """Validate an SOP questionnaire."""
    try:
        # Convert to internal format
        segments = [
            SOPSegment(
                segment_number=s.segment_number,
                title=s.title,
                description=s.description,
                key_action=s.key_action,
                visual_focus=s.visual_focus,
                duration=s.duration,
                text_overlay=s.text_overlay,
                voiceover_script=s.voiceover_script,
                props_needed=s.props_needed
            )
            for s in request.segments
        ]

        # Map string to enum
        video_style_map = {
            "professional": VideoStyle.PROFESSIONAL,
            "casual": VideoStyle.CASUAL,
            "educational": VideoStyle.EDUCATIONAL,
            "promotional": VideoStyle.PROMOTIONAL
        }
        video_style = video_style_map.get(request.video_style.lower(), VideoStyle.PROMOTIONAL)

        platform_map = {
            "instagram": PlatformTarget.INSTAGRAM,
            "tiktok": PlatformTarget.TIKTOK,
            "youtube_shorts": PlatformTarget.YOUTUBE_SHORTS,
            "linkedin": PlatformTarget.LINKEDIN,
            "facebook": PlatformTarget.FACEBOOK,
            "twitter": PlatformTarget.TWITTER
        }
        target_platforms = [
            platform_map.get(p.lower(), PlatformTarget.INSTAGRAM)
            for p in request.target_platforms
        ]

        questionnaire = SOPQuestionnaire(
            project_title=request.project_title,
            sop_purpose=request.sop_purpose,
            target_audience=request.target_audience,
            video_style=video_style,
            presenter_type=request.presenter_type,
            presenter_description=request.presenter_description,
            presenter_clothing=request.presenter_clothing,
            primary_location=request.primary_location,
            location_description=request.location_description,
            lighting_preference=request.lighting_preference,
            brand_colors=request.brand_colors,
            company_name=request.company_name,
            target_platforms=target_platforms,
            consistency_mode=request.consistency_mode,
            segments=segments
        )

        # Validate
        is_valid, error = questionnaire.validate()

        if not is_valid:
            raise HTTPException(status_code=400, detail=error)

        return QuestionnaireResponse(
            success=True,
            message="Questionnaire is valid",
            questionnaire_id=request.project_title,
            segment_count=len(segments),
            total_duration=sum(s.duration for s in segments)
        )

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Validation error: {str(e)}")


@app.post("/api/questionnaire/translate", response_model=PromptResponse)
async def translate_questionnaire(request: QuestionnaireRequest):
    """Translate questionnaire to VEO3 prompts."""
    try:
        from src.sop_translator import SOPPromptTranslator

        # First validate
        validate_response = await validate_questionnaire(request)

        if not validate_response.success:
            raise HTTPException(status_code=400, detail="Invalid questionnaire")

        # Convert to internal format (same as validation)
        segments = [
            SOPSegment(
                segment_number=s.segment_number,
                title=s.title,
                description=s.description,
                key_action=s.key_action,
                visual_focus=s.visual_focus,
                duration=s.duration,
                text_overlay=s.text_overlay,
                voiceover_script=s.voiceover_script,
                props_needed=s.props_needed
            )
            for s in request.segments
        ]

        video_style_map = {
            "professional": VideoStyle.PROFESSIONAL,
            "casual": VideoStyle.CASUAL,
            "educational": VideoStyle.EDUCATIONAL,
            "promotional": VideoStyle.PROMOTIONAL
        }
        video_style = video_style_map.get(request.video_style.lower(), VideoStyle.PROMOTIONAL)

        platform_map = {
            "instagram": PlatformTarget.INSTAGRAM,
            "tiktok": PlatformTarget.TIKTOK,
            "youtube_shorts": PlatformTarget.YOUTUBE_SHORTS,
            "linkedin": PlatformTarget.LINKEDIN,
            "facebook": PlatformTarget.FACEBOOK,
            "twitter": PlatformTarget.TWITTER
        }
        target_platforms = [
            platform_map.get(p.lower(), PlatformTarget.INSTAGRAM)
            for p in request.target_platforms
        ]

        questionnaire = SOPQuestionnaire(
            project_title=request.project_title,
            sop_purpose=request.sop_purpose,
            target_audience=request.target_audience,
            video_style=video_style,
            presenter_type=request.presenter_type,
            presenter_description=request.presenter_description,
            presenter_clothing=request.presenter_clothing,
            primary_location=request.primary_location,
            location_description=request.location_description,
            lighting_preference=request.lighting_preference,
            brand_colors=request.brand_colors,
            company_name=request.company_name,
            target_platforms=target_platforms,
            consistency_mode=request.consistency_mode,
            segments=segments
        )

        # Translate to prompts
        translator = SOPPromptTranslator()
        generation_requests = translator.translate_questionnaire(questionnaire)

        # Convert to response format
        prompts = [
            {
                "segment_number": i + 1,
                "scene_id": req.scene_id,
                "prompt": req.prompt,
                "duration": req.duration,
                "consistency_markers": req.consistency_markers
            }
            for i, req in enumerate(generation_requests)
        ]

        return PromptResponse(
            success=True,
            prompts=prompts,
            total_prompts=len(prompts)
        )

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Translation error: {str(e)}")


@app.get("/api/templates")
async def list_templates():
    """List available SOP video templates."""
    return {
        "templates": [
            {
                "name": "product_demo",
                "title": "Product Demonstration",
                "description": "Showcase product features and benefits",
                "segments": 4,
                "use_case": "Product launches, feature highlights"
            },
            {
                "name": "how_to",
                "title": "How-To Tutorial",
                "description": "Step-by-step instructional content",
                "segments": 4,
                "use_case": "Tutorials, skill training"
            },
            {
                "name": "training",
                "title": "Employee Training",
                "description": "Workplace procedures and protocols",
                "segments": 4,
                "use_case": "Onboarding, safety training"
            },
            {
                "name": "announcement",
                "title": "Company Announcement",
                "description": "News and updates",
                "segments": 4,
                "use_case": "Company updates, news"
            }
        ]
    }


@app.get("/api/templates/{template_name}")
async def get_template(template_name: str):
    """Get a specific template."""
    from src.sop_questionnaire import QuestionnaireBuilder

    valid_templates = ["product_demo", "how_to", "training", "announcement"]

    if template_name not in valid_templates:
        raise HTTPException(
            status_code=404,
            detail=f"Template not found. Available: {', '.join(valid_templates)}"
        )

    try:
        builder = QuestionnaireBuilder()
        questionnaire = builder.quick_template(template_name)

        return {
            "template_name": template_name,
            "questionnaire": questionnaire.to_dict()
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Template error: {str(e)}")


# Error handlers
@app.exception_handler(404)
async def not_found_handler(request, exc):
    return JSONResponse(
        status_code=404,
        content={"error": "Not found", "message": str(exc)}
    )


@app.exception_handler(500)
async def internal_error_handler(request, exc):
    return JSONResponse(
        status_code=500,
        content={"error": "Internal server error", "message": str(exc)}
    )


# For Vercel serverless
app = app
