"""Configuration management for VEO3 Consistency Generator."""

import os
from dataclasses import dataclass
from typing import Optional
from dotenv import load_dotenv

# Load environment variables
load_dotenv()


@dataclass
class VEO3Config:
    """VEO3 API and generation configuration."""
    
    api_key: str
    model: str = "veo-3"
    api_endpoint: str = "https://generativelanguage.googleapis.com/v1beta/models"
    consistency_mode: str = "strict"  # strict | balanced | creative
    
    # Generation settings
    default_duration: int = 5
    resolution: str = "1080p"
    fps: int = 24
    aspect_ratio: str = "16:9"
    
    # Output paths
    output_dir: str = "./output/videos"
    metadata_dir: str = "./data/metadata"
    
    # Consistency controls
    character_tracking: bool = True
    location_tracking: bool = True
    voice_tracking: bool = True
    lighting_tracking: bool = True
    style_tracking: bool = True
    
    # Safeguards
    prompt_validation: bool = True
    reference_checking: bool = True
    continuity_validation: bool = True
    max_retries: int = 3
    
    # Logging
    log_level: str = "INFO"
    
    @classmethod
    def from_env(cls) -> 'VEO3Config':
        """Load configuration from environment variables."""
        api_key = os.getenv('GOOGLE_API_KEY')
        if not api_key:
            raise ValueError("GOOGLE_API_KEY environment variable is required")
        
        return cls(
            api_key=api_key,
            model=os.getenv('VEO3_MODEL', 'veo-3'),
            consistency_mode=os.getenv('VEO3_CONSISTENCY_MODE', 'strict'),
            default_duration=int(os.getenv('VEO3_DEFAULT_DURATION', '5')),
            resolution=os.getenv('VEO3_RESOLUTION', '1080p'),
            fps=int(os.getenv('VEO3_FPS', '24')),
            aspect_ratio=os.getenv('VEO3_ASPECT_RATIO', '16:9'),
            output_dir=os.getenv('OUTPUT_DIR', './output/videos'),
            metadata_dir=os.getenv('METADATA_DIR', './data/metadata'),
            log_level=os.getenv('LOG_LEVEL', 'INFO')
        )
    
    def validate(self) -> bool:
        """Validate configuration settings."""
        if not self.api_key:
            raise ValueError("API key is required")
        
        if self.consistency_mode not in ['strict', 'balanced', 'creative']:
            raise ValueError(f"Invalid consistency mode: {self.consistency_mode}")
        
        if self.default_duration < 1 or self.default_duration > 60:
            raise ValueError(f"Duration must be between 1 and 60 seconds")
        
        # Create output directories if they don't exist
        os.makedirs(self.output_dir, exist_ok=True)
        os.makedirs(self.metadata_dir, exist_ok=True)
        
        return True
