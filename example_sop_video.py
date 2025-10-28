"""
Example: Generate SOP Video using Restore Assist Methodology

This demonstrates the full workflow from questionnaire to platform-ready videos.
"""

import sys
import os
from src.config import VEO3Config
from src.veo3_client import VEO3Client
from src.sop_questionnaire import (
    SOPQuestionnaire,
    SOPSegment,
    VideoStyle,
    PlatformTarget,
    QuestionnaireBuilder
)
from src.sop_translator import SOPPromptTranslator


def example_product_demo():
    """Create a product demonstration SOP video."""

    print("=== Restore Assist Integration - Product Demo Example ===\n")

    # Step 1: Create SOP Questionnaire
    print("1. Creating SOP questionnaire...")

    questionnaire = SOPQuestionnaire(
        project_title="SmartWidget_Product_Demo",
        sop_purpose="Demonstrate key features of SmartWidget product",
        target_audience="Potential customers and social media followers",
        video_style=VideoStyle.PROMOTIONAL,

        # Presenter details
        presenter_type="person",
        presenter_description="Professional woman, mid-30s, friendly demeanor, business casual",
        presenter_clothing="Navy blue blazer, white blouse, professional appearance",

        # Location
        primary_location="modern_office_with_product_display",
        location_description="Clean, bright modern office space with product display table",
        lighting_preference="bright_professional",

        # Brand
        company_name="SmartTech Inc",
        brand_colors=["#0066CC", "#FFFFFF", "#F0F0F0"],

        # Platform targeting
        target_platforms=[
            PlatformTarget.INSTAGRAM,
            PlatformTarget.TIKTOK
        ],

        # Consistency
        consistency_mode="strict",

        # Segments (4×8 seconds)
        segments=[
            SOPSegment(
                segment_number=1,
                title="Introduction",
                description="Presenter introduces the SmartWidget product",
                key_action="Hold up SmartWidget and smile at camera",
                visual_focus="Product in hand, presenter engaging with camera",
                text_overlay="Meet the SmartWidget"
            ),
            SOPSegment(
                segment_number=2,
                title="Easy Setup",
                description="Demonstrate the quick setup process",
                key_action="Unbox product and show one-click setup",
                visual_focus="Hands unboxing, product setup",
                text_overlay="Setup in 10 seconds"
            ),
            SOPSegment(
                segment_number=3,
                title="Smart Integration",
                description="Show product working with phone app",
                key_action="Tap phone screen, product responds",
                visual_focus="Phone screen, product responding",
                text_overlay="Control from anywhere"
            ),
            SOPSegment(
                segment_number=4,
                title="Call to Action",
                description="Encourage viewers to purchase",
                key_action="Presenter gestures to camera",
                visual_focus="Presenter smiling, product visible",
                text_overlay="Get yours today!"
            )
        ]
    )

    # Validate
    is_valid, error = questionnaire.validate()
    if not is_valid:
        print(f"    Error: {error}")
        sys.exit(1)

    print(f"    Created: {questionnaire.project_title}")
    print(f"   - Segments: {len(questionnaire.segments)}")
    print(f"   - Duration: {len(questionnaire.segments) * 8} seconds\n")

    # Step 2: Translate to prompts
    print("2. Translating to VEO3 prompts...")

    translator = SOPPromptTranslator()
    requests = translator.translate_questionnaire(questionnaire)

    print(f"    Generated {len(requests)} prompts\n")

    # Show example
    print("   Example Segment 1 prompt (first 20 lines):")
    print("   " + "-" * 60)
    lines = requests[0].prompt.split('\n')[:20]
    for line in lines:
        print(f"   {line}")
    print("   ...")
    print("   " + "-" * 60 + "\n")

    # Step 3: Ready to generate
    print("3. Ready to generate videos")
    print(f"   This will create {len(requests)} segments")
    print(f"   Estimated time: {len(requests) * 2} minutes\n")

    try:
        config = VEO3Config.from_env()
        client = VEO3Client(config)
        print("    VEO3 client ready\n")
    except ValueError as e:
        print(f"   Note: {e}")
        print("   Add GOOGLE_API_KEY to .env to generate videos\n")
        return

    confirm = input("   Generate now? (y/N): ").strip().lower()

    if confirm != 'y':
        print("\n   Skipping generation.")
        return

    # Generate
    print()
    videos = []
    for i, request in enumerate(requests, 1):
        print(f"   Generating segment {i}/{len(requests)}...")
        response = client.generate_video(request)

        if response.success:
            print(f"    {response.video_path}")
            videos.append(response.video_path)
        else:
            print(f"    Failed: {response.error}")
            break

    if len(videos) == len(requests):
        print(f"\n Complete! Generated {len(videos)} segments")


if __name__ == "__main__":
    example_product_demo()
