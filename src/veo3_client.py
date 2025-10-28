"""VEO3 API client for video generation."""

import os
import json
import time
import logging
from typing import Dict, Optional, Any
from dataclasses import dataclass
import requests

from src.config import VEO3Config

logger = logging.getLogger(__name__)


@dataclass
class VideoGenerationRequest:
    """Request for VEO3 video generation."""

    prompt: str
    duration: Optional[int] = None
    resolution: Optional[str] = None
    fps: Optional[int] = None
    aspect_ratio: Optional[str] = None
    consistency_markers: Optional[Dict] = None
    scene_id: Optional[str] = None
    sequence_id: Optional[str] = None


@dataclass
class VideoGenerationResponse:
    """Response from VEO3 video generation."""

    success: bool
    video_path: Optional[str] = None
    video_url: Optional[str] = None
    metadata: Optional[Dict] = None
    error: Optional[str] = None
    retry_count: int = 0


class VEO3Client:
    """Client for interacting with Google VEO3 API."""

    def __init__(self, config: VEO3Config):
        """Initialize VEO3 client with configuration."""
        self.config = config
        self.config.validate()

        # Configure logging
        logging.basicConfig(level=getattr(logging, config.log_level))
        logger.info(f"VEO3Client initialized with model: {config.model}")

    def generate_video(self, request: VideoGenerationRequest) -> VideoGenerationResponse:
        """
        Generate a video using VEO3 API.

        Args:
            request: Video generation request

        Returns:
            VideoGenerationResponse with result or error
        """
        # Use config defaults if not specified
        duration = request.duration or self.config.default_duration
        resolution = request.resolution or self.config.resolution
        fps = request.fps or self.config.fps
        aspect_ratio = request.aspect_ratio or self.config.aspect_ratio

        logger.info(f"Generating video: {request.scene_id or 'unnamed'}")
        logger.debug(f"Prompt: {request.prompt[:100]}...")

        # Prepare API request
        api_url = f"{self.config.api_endpoint}/{self.config.model}:generateVideo"

        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self.config.api_key}"
        }

        payload = {
            "prompt": request.prompt,
            "parameters": {
                "duration": duration,
                "resolution": resolution,
                "fps": fps,
                "aspect_ratio": aspect_ratio
            }
        }

        # Add consistency markers if provided
        if request.consistency_markers:
            payload["consistency_markers"] = request.consistency_markers

        try:
            # Make API request
            response = requests.post(api_url, headers=headers, json=payload, timeout=300)
            response.raise_for_status()

            result = response.json()

            # Handle async generation (if API returns operation ID)
            if "operationId" in result:
                return self._poll_generation_status(result["operationId"], request)

            # Handle sync generation
            if "videoUrl" in result:
                video_path = self._download_video(result["videoUrl"], request.scene_id)

                return VideoGenerationResponse(
                    success=True,
                    video_path=video_path,
                    video_url=result["videoUrl"],
                    metadata=result.get("metadata", {})
                )

            return VideoGenerationResponse(
                success=False,
                error="Unexpected API response format"
            )

        except requests.exceptions.RequestException as e:
            logger.error(f"API request failed: {str(e)}")
            return VideoGenerationResponse(
                success=False,
                error=str(e)
            )
        except Exception as e:
            logger.error(f"Video generation failed: {str(e)}")
            return VideoGenerationResponse(
                success=False,
                error=str(e)
            )

    def _poll_generation_status(
        self,
        operation_id: str,
        request: VideoGenerationRequest
    ) -> VideoGenerationResponse:
        """
        Poll for video generation status (for async generation).

        Args:
            operation_id: Operation ID from initial request
            request: Original generation request

        Returns:
            VideoGenerationResponse when complete
        """
        api_url = f"{self.config.api_endpoint}/operations/{operation_id}"
        headers = {"Authorization": f"Bearer {self.config.api_key}"}

        max_polls = 60  # 5 minutes with 5-second intervals
        poll_interval = 5

        for i in range(max_polls):
            try:
                response = requests.get(api_url, headers=headers, timeout=30)
                response.raise_for_status()

                result = response.json()

                if result.get("done"):
                    if "error" in result:
                        return VideoGenerationResponse(
                            success=False,
                            error=result["error"].get("message", "Unknown error")
                        )

                    video_url = result.get("response", {}).get("videoUrl")
                    if video_url:
                        video_path = self._download_video(video_url, request.scene_id)

                        return VideoGenerationResponse(
                            success=True,
                            video_path=video_path,
                            video_url=video_url,
                            metadata=result.get("response", {}).get("metadata", {})
                        )

                logger.info(f"Generation in progress... ({i+1}/{max_polls})")
                time.sleep(poll_interval)

            except Exception as e:
                logger.error(f"Status polling failed: {str(e)}")
                return VideoGenerationResponse(
                    success=False,
                    error=f"Polling failed: {str(e)}"
                )

        return VideoGenerationResponse(
            success=False,
            error="Generation timeout"
        )

    def _download_video(self, video_url: str, scene_id: Optional[str] = None) -> str:
        """
        Download generated video from URL.

        Args:
            video_url: URL of generated video
            scene_id: Optional scene ID for filename

        Returns:
            Local path to downloaded video
        """
        filename = f"{scene_id or 'video'}_{int(time.time())}.mp4"
        output_path = os.path.join(self.config.output_dir, filename)

        logger.info(f"Downloading video to {output_path}")

        try:
            response = requests.get(video_url, stream=True, timeout=300)
            response.raise_for_status()

            with open(output_path, 'wb') as f:
                for chunk in response.iter_content(chunk_size=8192):
                    f.write(chunk)

            logger.info(f"Video downloaded successfully: {output_path}")
            return output_path

        except Exception as e:
            logger.error(f"Video download failed: {str(e)}")
            raise

    def validate_prompt(self, prompt: str) -> tuple[bool, Optional[str]]:
        """
        Validate prompt before generation.

        Args:
            prompt: Prompt to validate

        Returns:
            Tuple of (is_valid, error_message)
        """
        if not prompt or len(prompt.strip()) == 0:
            return False, "Prompt cannot be empty"

        if len(prompt) < 10:
            return False, "Prompt too short (minimum 10 characters)"

        if len(prompt) > 5000:
            return False, "Prompt too long (maximum 5000 characters)"

        return True, None
