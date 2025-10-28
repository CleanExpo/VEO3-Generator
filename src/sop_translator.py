"""
SOP to VEO3 Prompt Translator

Converts structured SOP questionnaires into optimized VEO3 prompts.
Restore Assist methodology integration.
"""

from typing import Dict, List
from src.sop_questionnaire import SOPQuestionnaire, SOPSegment, VideoStyle
from src.veo3_client import VideoGenerationRequest


class SOPPromptTranslator:
    """Translates SOP questionnaires into VEO3-optimized prompts."""

    def __init__(self):
        self.style_to_cinematography = {
            VideoStyle.PROFESSIONAL: "steady, professional camera work, clean composition, corporate aesthetic",
            VideoStyle.CASUAL: "handheld feel, natural movement, relaxed framing, approachable style",
            VideoStyle.EDUCATIONAL: "clear, focused shots, instructional framing, detailed visibility",
            VideoStyle.PROMOTIONAL: "dynamic angles, engaging movement, polished production, eye-catching"
        }

        self.style_to_lighting = {
            VideoStyle.PROFESSIONAL: "bright, even professional lighting, high-key setup",
            VideoStyle.CASUAL: "natural lighting, soft shadows, warm tones",
            VideoStyle.EDUCATIONAL: "clear, well-lit environment, no harsh shadows, visibility priority",
            VideoStyle.PROMOTIONAL: "dramatic lighting, vibrant colors, high contrast, professional grade"
        }

    def translate_segment(
        self,
        segment: SOPSegment,
        questionnaire: SOPQuestionnaire,
        previous_segment: SOPSegment = None
    ) -> str:
        """
        Translate a single SOP segment into a VEO3 prompt.

        Args:
            segment: The segment to translate
            questionnaire: Full questionnaire for context
            previous_segment: Previous segment for continuity

        Returns:
            Detailed VEO3 prompt string
        """
        prompt_parts = []

        # Duration constraint
        prompt_parts.append(f"[8-second video segment - {segment.title}]")
        prompt_parts.append("")

        # Scene description
        prompt_parts.append(f"Scene: {segment.description}")
        prompt_parts.append(f"Key Action: {segment.key_action}")
        prompt_parts.append(f"Visual Focus: {segment.visual_focus}")
        prompt_parts.append("")

        # Presenter (if applicable)
        if questionnaire.presenter_type == "person":
            if questionnaire.presenter_description:
                prompt_parts.append(f"Presenter: {questionnaire.presenter_description}")
            if questionnaire.presenter_clothing:
                prompt_parts.append(f"Clothing: {questionnaire.presenter_clothing}")
            prompt_parts.append("Presenter position: Center frame, professional posture, engaging with camera")
            prompt_parts.append("")

        elif questionnaire.presenter_type == "animated_character":
            if questionnaire.presenter_description:
                prompt_parts.append(f"Animated Character: {questionnaire.presenter_description}")
            prompt_parts.append("Character animation: Smooth, professional quality, expressive")
            prompt_parts.append("")

        # Location and environment
        if segment.location:
            prompt_parts.append(f"Location: {segment.location}")
        elif questionnaire.primary_location:
            prompt_parts.append(f"Location: {questionnaire.primary_location}")

        if questionnaire.location_description:
            prompt_parts.append(questionnaire.location_description)

        prompt_parts.append("")

        # Cinematography
        cinematography = self.style_to_cinematography.get(
            questionnaire.video_style,
            "professional, clean composition"
        )
        prompt_parts.append(f"Cinematography: {cinematography}")

        # Lighting
        lighting = self.style_to_lighting.get(
            questionnaire.video_style,
            questionnaire.lighting_preference
        )
        prompt_parts.append(f"Lighting: {lighting}")
        prompt_parts.append("")

        # Brand colors (if provided)
        if questionnaire.brand_colors:
            colors = ", ".join(questionnaire.brand_colors)
            prompt_parts.append(f"Color palette: {colors}, maintaining brand consistency")
            prompt_parts.append("")

        # Text overlay (if specified)
        if segment.text_overlay:
            prompt_parts.append(f"Text Overlay: '{segment.text_overlay}'")
            prompt_parts.append("Text position: Lower third, clean sans-serif font, high contrast")
            if questionnaire.brand_colors:
                prompt_parts.append(f"Text color: {questionnaire.brand_colors[0]}")
            prompt_parts.append("")

        # Props (if needed)
        if segment.props_needed:
            props = ", ".join(segment.props_needed)
            prompt_parts.append(f"Props visible: {props}")
            prompt_parts.append("")

        # Continuity anchors (if not first segment)
        if previous_segment and segment.segment_number > 1:
            prompt_parts.append("CONTINUITY REQUIREMENTS:")

            if questionnaire.presenter_type in ["person", "animated_character"]:
                prompt_parts.append(f"- Presenter MUST match exact appearance from Segment {previous_segment.segment_number}")
                if questionnaire.presenter_clothing:
                    prompt_parts.append(f"- Maintain exact clothing: {questionnaire.presenter_clothing}")

            if questionnaire.primary_location:
                prompt_parts.append(f"- Location MUST be identical to previous segment")
                prompt_parts.append(f"- Lighting MUST match previous segment exactly")

            prompt_parts.append(f"- Color palette MUST be consistent with previous segment")
            prompt_parts.append("")

        # Quality constraints
        prompt_parts.append("Technical Requirements:")
        prompt_parts.append("- Exactly 8 seconds duration")
        prompt_parts.append("- Smooth, professional quality")
        prompt_parts.append("- No camera shake or jitter")
        prompt_parts.append("- Clear, in-focus subjects")
        prompt_parts.append("- Professional production value")

        # Consistency mode enforcement
        if questionnaire.consistency_mode == "strict":
            prompt_parts.append("- STRICT consistency: no variations from established baseline")
        elif questionnaire.consistency_mode == "balanced":
            prompt_parts.append("- Balanced: maintain core consistency while allowing natural variation")
        else:  # creative
            prompt_parts.append("- Creative: preserve key elements but allow creative expression")

        prompt_parts.append("")

        # Negative constraints (what NOT to include)
        prompt_parts.append("DO NOT INCLUDE:")
        prompt_parts.append("- Unrelated objects or people")
        prompt_parts.append("- Sudden lighting changes")
        prompt_parts.append("- Jump cuts or abrupt transitions")
        prompt_parts.append("- Inconsistent styles or aesthetics")
        if segment.segment_number > 1:
            prompt_parts.append("- ANY changes to presenter appearance")
            prompt_parts.append("- ANY changes to location or background")

        return "\n".join(prompt_parts)

    def translate_questionnaire(
        self,
        questionnaire: SOPQuestionnaire
    ) -> List[VideoGenerationRequest]:
        """
        Translate entire questionnaire into VEO3 generation requests.

        Args:
            questionnaire: Complete SOP questionnaire

        Returns:
            List of VideoGenerationRequest objects, one per segment
        """
        requests = []

        # Validate questionnaire
        is_valid, error = questionnaire.validate()
        if not is_valid:
            raise ValueError(f"Invalid questionnaire: {error}")

        # Generate prompts for each segment
        previous_segment = None
        for segment in questionnaire.segments:
            prompt = self.translate_segment(segment, questionnaire, previous_segment)

            # Create consistency markers
            consistency_markers = {
                "segment_number": segment.segment_number,
                "sequence_id": questionnaire.project_title,
                "consistency_mode": questionnaire.consistency_mode
            }

            # Add presenter ID if applicable
            if questionnaire.presenter_type in ["person", "animated_character"]:
                consistency_markers["presenter_id"] = "presenter_001"

            # Add location ID
            if questionnaire.primary_location:
                consistency_markers["location_id"] = "location_001"

            # Create generation request
            request = VideoGenerationRequest(
                prompt=prompt,
                duration=segment.duration,
                scene_id=f"{questionnaire.project_title}_segment_{segment.segment_number}",
                sequence_id=questionnaire.project_title,
                consistency_markers=consistency_markers
            )

            requests.append(request)
            previous_segment = segment

        return requests

    def generate_intro_outro(
        self,
        questionnaire: SOPQuestionnaire,
        segment_type: str  # "intro" or "outro"
    ) -> str:
        """
        Generate prompt for intro or outro segment.

        Args:
            questionnaire: SOP questionnaire
            segment_type: "intro" or "outro"

        Returns:
            VEO3 prompt for intro/outro
        """
        prompt_parts = []

        if segment_type == "intro":
            prompt_parts.append(f"[3-second intro - {questionnaire.project_title}]")
            prompt_parts.append("")
            prompt_parts.append(f"Professional video intro for: {questionnaire.sop_purpose}")

            if questionnaire.company_name:
                prompt_parts.append(f"Company: {questionnaire.company_name}")

            if questionnaire.brand_colors:
                colors = ", ".join(questionnaire.brand_colors)
                prompt_parts.append(f"Brand colors: {colors}")

            prompt_parts.append("")
            prompt_parts.append("Visual Elements:")
            prompt_parts.append(f"- Title text: '{questionnaire.project_title}'")
            prompt_parts.append("- Clean, professional animation")
            prompt_parts.append("- Brand colors prominent")

            if questionnaire.logo_placement:
                prompt_parts.append(f"- Logo placement: {questionnaire.logo_placement}")

        else:  # outro
            prompt_parts.append(f"[3-second outro - Call to Action]")
            prompt_parts.append("")
            prompt_parts.append("Professional video outro with call to action")

            if questionnaire.company_name:
                prompt_parts.append(f"Company: {questionnaire.company_name}")

            if questionnaire.brand_colors:
                colors = ", ".join(questionnaire.brand_colors)
                prompt_parts.append(f"Brand colors: {colors}")

            prompt_parts.append("")
            prompt_parts.append("Visual Elements:")
            prompt_parts.append("- 'Thank you' or 'Questions?' text")
            prompt_parts.append("- Contact information display")
            prompt_parts.append("- Clean fade out")

            if questionnaire.logo_placement:
                prompt_parts.append(f"- Logo: {questionnaire.logo_placement}")

        prompt_parts.append("")
        prompt_parts.append("Technical:")
        if segment_type == "intro":
            prompt_parts.append("- Exactly 3 seconds")
        else:
            prompt_parts.append("- Exactly 3 seconds")
        prompt_parts.append("- Professional animation quality")
        prompt_parts.append("- Smooth, polished execution")

        return "\n".join(prompt_parts)

    def get_platform_specs(self, platform: str) -> Dict:
        """
        Get platform-specific video specifications.

        Args:
            platform: Platform name (instagram, tiktok, etc.)

        Returns:
            Dictionary with platform specs
        """
        specs = {
            "instagram": {
                "aspect_ratios": ["16:9", "1:1", "9:16"],
                "max_duration": 60,
                "recommended_duration": 30,
                "resolution": "1080x1080",
                "format": "mp4"
            },
            "tiktok": {
                "aspect_ratios": ["9:16"],
                "max_duration": 60,
                "recommended_duration": 15,
                "resolution": "1080x1920",
                "format": "mp4"
            },
            "youtube_shorts": {
                "aspect_ratios": ["9:16"],
                "max_duration": 60,
                "recommended_duration": 30,
                "resolution": "1080x1920",
                "format": "mp4"
            },
            "linkedin": {
                "aspect_ratios": ["16:9"],
                "max_duration": 600,
                "recommended_duration": 30,
                "resolution": "1920x1080",
                "format": "mp4"
            },
            "facebook": {
                "aspect_ratios": ["16:9", "1:1"],
                "max_duration": 240,
                "recommended_duration": 30,
                "resolution": "1920x1080",
                "format": "mp4"
            },
            "twitter": {
                "aspect_ratios": ["16:9", "1:1"],
                "max_duration": 140,
                "recommended_duration": 30,
                "resolution": "1920x1080",
                "format": "mp4"
            }
        }

        return specs.get(platform.lower(), specs["instagram"])
