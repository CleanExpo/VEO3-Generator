"""
SOP Questionnaire Module - Restore Assist Integration

Captures structured information for generating SOP videos using VEO3.
"""

from dataclasses import dataclass, field
from typing import List, Optional, Dict
from enum import Enum
import json


class VideoStyle(Enum):
    """Video style options."""
    PROFESSIONAL = "professional"
    CASUAL = "casual"
    EDUCATIONAL = "educational"
    PROMOTIONAL = "promotional"


class PlatformTarget(Enum):
    """Target platforms for video output."""
    INSTAGRAM = "instagram"
    TIKTOK = "tiktok"
    YOUTUBE_SHORTS = "youtube_shorts"
    FACEBOOK = "facebook"
    LINKEDIN = "linkedin"
    TWITTER = "twitter"


@dataclass
class SOPSegment:
    """Single 8-second segment of an SOP video."""

    segment_number: int
    title: str
    description: str
    key_action: str
    visual_focus: str
    duration: int = 8

    # Optional elements
    text_overlay: Optional[str] = None
    voiceover_script: Optional[str] = None
    props_needed: List[str] = field(default_factory=list)
    location: Optional[str] = None


@dataclass
class SOPQuestionnaire:
    """Complete questionnaire for SOP video generation."""

    # Core information
    project_title: str
    sop_purpose: str
    target_audience: str

    # Visual style
    video_style: VideoStyle
    brand_colors: List[str] = field(default_factory=list)
    brand_fonts: List[str] = field(default_factory=list)

    # Platform requirements
    target_platforms: List[PlatformTarget] = field(default_factory=list)

    # Character/Presenter
    presenter_type: str = "none"  # none, person, animated_character, text_only
    presenter_description: Optional[str] = None
    presenter_clothing: Optional[str] = None

    # Location/Setting
    primary_location: str = ""
    location_description: str = ""
    lighting_preference: str = "bright_professional"

    # Segments (4×8 seconds)
    segments: List[SOPSegment] = field(default_factory=list)

    # Branding
    company_name: Optional[str] = None
    logo_placement: Optional[str] = None
    intro_outro_needed: bool = True

    # Audio
    music_style: Optional[str] = None
    voiceover_needed: bool = False
    voiceover_language: str = "english"

    # Consistency requirements
    consistency_mode: str = "strict"  # strict, balanced, creative

    def to_dict(self) -> Dict:
        """Convert questionnaire to dictionary."""
        return {
            "project_title": self.project_title,
            "sop_purpose": self.sop_purpose,
            "target_audience": self.target_audience,
            "video_style": self.video_style.value,
            "brand_colors": self.brand_colors,
            "brand_fonts": self.brand_fonts,
            "target_platforms": [p.value for p in self.target_platforms],
            "presenter_type": self.presenter_type,
            "presenter_description": self.presenter_description,
            "presenter_clothing": self.presenter_clothing,
            "primary_location": self.primary_location,
            "location_description": self.location_description,
            "lighting_preference": self.lighting_preference,
            "segments": [
                {
                    "segment_number": s.segment_number,
                    "title": s.title,
                    "description": s.description,
                    "key_action": s.key_action,
                    "visual_focus": s.visual_focus,
                    "duration": s.duration,
                    "text_overlay": s.text_overlay,
                    "voiceover_script": s.voiceover_script,
                    "props_needed": s.props_needed,
                    "location": s.location
                }
                for s in self.segments
            ],
            "company_name": self.company_name,
            "logo_placement": self.logo_placement,
            "intro_outro_needed": self.intro_outro_needed,
            "music_style": self.music_style,
            "voiceover_needed": self.voiceover_needed,
            "voiceover_language": self.voiceover_language,
            "consistency_mode": self.consistency_mode
        }

    def to_json(self, filepath: str):
        """Save questionnaire to JSON file."""
        with open(filepath, 'w') as f:
            json.dump(self.to_dict(), f, indent=2)

    @classmethod
    def from_json(cls, filepath: str) -> 'SOPQuestionnaire':
        """Load questionnaire from JSON file."""
        with open(filepath, 'r') as f:
            data = json.load(f)

        return cls(
            project_title=data["project_title"],
            sop_purpose=data["sop_purpose"],
            target_audience=data["target_audience"],
            video_style=VideoStyle(data["video_style"]),
            brand_colors=data.get("brand_colors", []),
            brand_fonts=data.get("brand_fonts", []),
            target_platforms=[PlatformTarget(p) for p in data.get("target_platforms", [])],
            presenter_type=data.get("presenter_type", "none"),
            presenter_description=data.get("presenter_description"),
            presenter_clothing=data.get("presenter_clothing"),
            primary_location=data.get("primary_location", ""),
            location_description=data.get("location_description", ""),
            lighting_preference=data.get("lighting_preference", "bright_professional"),
            segments=[
                SOPSegment(
                    segment_number=s["segment_number"],
                    title=s["title"],
                    description=s["description"],
                    key_action=s["key_action"],
                    visual_focus=s["visual_focus"],
                    duration=s.get("duration", 8),
                    text_overlay=s.get("text_overlay"),
                    voiceover_script=s.get("voiceover_script"),
                    props_needed=s.get("props_needed", []),
                    location=s.get("location")
                )
                for s in data.get("segments", [])
            ],
            company_name=data.get("company_name"),
            logo_placement=data.get("logo_placement"),
            intro_outro_needed=data.get("intro_outro_needed", True),
            music_style=data.get("music_style"),
            voiceover_needed=data.get("voiceover_needed", False),
            voiceover_language=data.get("voiceover_language", "english"),
            consistency_mode=data.get("consistency_mode", "strict")
        )

    def validate(self) -> tuple[bool, Optional[str]]:
        """Validate questionnaire completeness."""
        if not self.project_title:
            return False, "Project title is required"

        if not self.sop_purpose:
            return False, "SOP purpose is required"

        if not self.target_audience:
            return False, "Target audience is required"

        if len(self.segments) == 0:
            return False, "At least one segment is required"

        if len(self.segments) > 6:
            return False, "Maximum 6 segments allowed (48 seconds total)"

        # Validate each segment
        for segment in self.segments:
            if not segment.title:
                return False, f"Segment {segment.segment_number} missing title"
            if not segment.description:
                return False, f"Segment {segment.segment_number} missing description"
            if not segment.key_action:
                return False, f"Segment {segment.segment_number} missing key action"

        return True, None


class QuestionnaireBuilder:
    """Interactive builder for SOP questionnaires."""

    def __init__(self):
        self.questionnaire = None

    def create_interactive(self) -> SOPQuestionnaire:
        """Create questionnaire through interactive prompts."""
        print("=== SOP Video Questionnaire (Restore Assist Integration) ===\n")

        # Basic info
        project_title = input("Project Title: ").strip()
        sop_purpose = input("What is the purpose of this SOP? ").strip()
        target_audience = input("Who is the target audience? ").strip()

        # Style
        print("\nVideo Style:")
        print("1. Professional")
        print("2. Casual")
        print("3. Educational")
        print("4. Promotional")
        style_choice = input("Choose style (1-4): ").strip()

        style_map = {
            "1": VideoStyle.PROFESSIONAL,
            "2": VideoStyle.CASUAL,
            "3": VideoStyle.EDUCATIONAL,
            "4": VideoStyle.PROMOTIONAL
        }
        video_style = style_map.get(style_choice, VideoStyle.PROFESSIONAL)

        # Presenter
        print("\nPresenter Type:")
        print("1. No presenter (text/visuals only)")
        print("2. Real person")
        print("3. Animated character")
        presenter_choice = input("Choose presenter type (1-3): ").strip()

        presenter_map = {
            "1": "none",
            "2": "person",
            "3": "animated_character"
        }
        presenter_type = presenter_map.get(presenter_choice, "none")

        presenter_description = None
        presenter_clothing = None

        if presenter_type == "person":
            presenter_description = input("Describe the presenter (age, gender, appearance): ").strip()
            presenter_clothing = input("Presenter clothing/style: ").strip()
        elif presenter_type == "animated_character":
            presenter_description = input("Describe the character: ").strip()

        # Location
        primary_location = input("\nPrimary location/setting: ").strip()
        location_description = input("Describe the location: ").strip()

        # Segments
        print("\n=== Segments (8 seconds each) ===")
        num_segments = int(input("How many segments? (typically 4): ").strip() or "4")

        segments = []
        for i in range(num_segments):
            print(f"\n--- Segment {i+1} ---")
            title = input(f"Segment {i+1} title: ").strip()
            description = input(f"Segment {i+1} description: ").strip()
            key_action = input(f"Key action in this segment: ").strip()
            visual_focus = input(f"Visual focus: ").strip()
            text_overlay = input(f"Text overlay (optional): ").strip() or None

            segments.append(SOPSegment(
                segment_number=i+1,
                title=title,
                description=description,
                key_action=key_action,
                visual_focus=visual_focus,
                text_overlay=text_overlay
            ))

        # Create questionnaire
        self.questionnaire = SOPQuestionnaire(
            project_title=project_title,
            sop_purpose=sop_purpose,
            target_audience=target_audience,
            video_style=video_style,
            presenter_type=presenter_type,
            presenter_description=presenter_description,
            presenter_clothing=presenter_clothing,
            primary_location=primary_location,
            location_description=location_description,
            segments=segments
        )

        return self.questionnaire

    def quick_template(self, template_name: str) -> SOPQuestionnaire:
        """Create questionnaire from predefined template."""
        templates = {
            "product_demo": self._product_demo_template(),
            "how_to": self._how_to_template(),
            "training": self._training_template(),
            "announcement": self._announcement_template()
        }

        return templates.get(template_name, self._product_demo_template())

    def _product_demo_template(self) -> SOPQuestionnaire:
        """Template for product demonstration videos."""
        return SOPQuestionnaire(
            project_title="Product Demo Template",
            sop_purpose="Demonstrate product features and benefits",
            target_audience="Potential customers",
            video_style=VideoStyle.PROMOTIONAL,
            presenter_type="person",
            primary_location="clean_modern_office",
            segments=[
                SOPSegment(1, "Introduction", "Introduce the product", "Show product", "Product close-up"),
                SOPSegment(2, "Key Feature 1", "Demonstrate main feature", "Use feature", "Feature in action"),
                SOPSegment(3, "Key Feature 2", "Show second feature", "Demonstrate benefit", "Results"),
                SOPSegment(4, "Call to Action", "Encourage purchase/signup", "Show CTA", "CTA text and link")
            ]
        )

    def _how_to_template(self) -> SOPQuestionnaire:
        """Template for how-to instruction videos."""
        return SOPQuestionnaire(
            project_title="How-To Template",
            sop_purpose="Teach a specific skill or process",
            target_audience="Learners/Students",
            video_style=VideoStyle.EDUCATIONAL,
            presenter_type="person",
            primary_location="workshop_or_classroom",
            segments=[
                SOPSegment(1, "Overview", "Explain what will be taught", "State goal", "Instructor speaking"),
                SOPSegment(2, "Step 1", "First step of process", "Demonstrate step 1", "Hands-on action"),
                SOPSegment(3, "Step 2", "Second step", "Demonstrate step 2", "Continued action"),
                SOPSegment(4, "Result", "Show final outcome", "Display result", "Finished product")
            ]
        )

    def _training_template(self) -> SOPQuestionnaire:
        """Template for employee training videos."""
        return SOPQuestionnaire(
            project_title="Training Template",
            sop_purpose="Train employees on procedure",
            target_audience="Employees",
            video_style=VideoStyle.PROFESSIONAL,
            presenter_type="person",
            primary_location="workplace",
            segments=[
                SOPSegment(1, "Safety First", "Safety guidelines", "Show safety gear", "PPE and precautions"),
                SOPSegment(2, "Setup", "Prepare workspace", "Arrange tools", "Organized workspace"),
                SOPSegment(3, "Procedure", "Execute main task", "Perform procedure", "Correct technique"),
                SOPSegment(4, "Completion", "Wrap up and verify", "Quality check", "Verification process")
            ]
        )

    def _announcement_template(self) -> SOPQuestionnaire:
        """Template for company announcements."""
        return SOPQuestionnaire(
            project_title="Announcement Template",
            sop_purpose="Announce news or updates",
            target_audience="Team members or customers",
            video_style=VideoStyle.PROFESSIONAL,
            presenter_type="person",
            primary_location="office_or_studio",
            segments=[
                SOPSegment(1, "Greeting", "Welcome and introduce topic", "Greet audience", "Presenter speaking"),
                SOPSegment(2, "Announcement", "Share the news", "State announcement", "Key information"),
                SOPSegment(3, "Impact", "Explain what it means", "Describe benefits", "Visual of impact"),
                SOPSegment(4, "Next Steps", "Call to action", "Direct next steps", "Action items")
            ]
        )
