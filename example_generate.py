"""
Example script for generating a video with VEO3.

This demonstrates basic usage of the VEO3 Consistency Generator.
"""

import sys
from src.config import VEO3Config
from src.veo3_client import VEO3Client, VideoGenerationRequest


def main():
    """Generate a simple test video."""
    
    print("=== VEO3 Consistency Generator - Example ===\n")
    
    # Step 1: Load configuration
    print("1. Loading configuration...")
    try:
        config = VEO3Config.from_env()
        print(f"   ✓ Configuration loaded")
        print(f"   - Model: {config.model}")
        print(f"   - Consistency mode: {config.consistency_mode}")
        print(f"   - Output directory: {config.output_dir}\n")
    except ValueError as e:
        print(f"   ✗ Configuration error: {e}")
        print("\n   Make sure you have created a .env file with your GOOGLE_API_KEY")
        print("   See .env.example for reference")
        sys.exit(1)
    
    # Step 2: Initialize client
    print("2. Initializing VEO3 client...")
    client = VEO3Client(config)
    print(f"   ✓ Client initialized\n")
    
    # Step 3: Create generation request
    print("3. Preparing generation request...")
    prompt = """
    A peaceful morning scene: A young woman with long brown hair and casual clothing 
    walks through a sunlit park. Golden morning light filters through the trees. 
    Cinematic quality, 4K, natural colors, soft focus background.
    """
    
    request = VideoGenerationRequest(
        prompt=prompt.strip(),
        duration=5,
        resolution="1080p",
        scene_id="example_scene_001"
    )
    
    # Validate prompt
    is_valid, error = client.validate_prompt(request.prompt)
    if not is_valid:
        print(f"   ✗ Prompt validation failed: {error}")
        sys.exit(1)
    
    print(f"   ✓ Prompt validated")
    print(f"   - Duration: {request.duration}s")
    print(f"   - Resolution: {request.resolution}")
    print(f"   - Scene ID: {request.scene_id}\n")
    
    # Step 4: Generate video
    print("4. Generating video...")
    print("   (This may take several minutes)\n")
    
    response = client.generate_video(request)
    
    # Step 5: Check result
    print("5. Generation result:")
    if response.success:
        print(f"   ✓ Video generated successfully!")
        print(f"   - Path: {response.video_path}")
        if response.metadata:
            print(f"   - Metadata: {response.metadata}")
        print("\n✓ Generation complete!")
    else:
        print(f"   ✗ Generation failed: {response.error}")
        print("\n   Possible reasons:")
        print("   - Invalid API key")
        print("   - API quota exceeded")
        print("   - Network connectivity issues")
        print("   - VEO3 service unavailable")
        sys.exit(1)


if __name__ == "__main__":
    main()
