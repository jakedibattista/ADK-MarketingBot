"""
Veo Generator Agent - Video Generation Tool
"""

import os
import datetime
import time
import json
import requests
from typing import Dict, Any
from google.adk.agents.llm_agent import LlmAgent

def generate_single_video(script: str) -> Dict[str, Any]:
    """
    Generates a single marketing video from a Veo script and uploads to Google Cloud Storage.
    
    Args:
        script (str): The Veo 2.0 script/prompt for video generation
        
    Returns:
        Dict[str, Any]: Contains success status, video details, and GCS URL
    """
    
    try:
        from google.auth import default
        from google.auth.transport.requests import Request
        from google.cloud import storage
        
        # Get credentials and project info
        credentials, project_id = default()
        if not credentials.valid:
            credentials.refresh(Request())
        
        access_token = credentials.token
        timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        
        # Use the working Veo 2.0 simple generator instead of Veo 3.0
        from .simple_veo_generator import generate_veo_video_simple
        
        # Enhance script to avoid text overlays that often have spelling errors
        enhanced_script = f"{script}\n\nIMPORTANT: Generate video with NO visible text, words, letters, or typography on screen. Focus on pure visual storytelling through action, emotion, and imagery. Any brand messaging should be conveyed through visual elements only, not text overlays."
        
        # Use the working Veo 2.0 generator
        result = generate_veo_video_simple(enhanced_script)
        
        if result.get("success"):
            return {
                "success": True,
                "video_url": result.get("video_url"),
                "script_used": script,
                "model": "veo-2.0-generate-001",
                "operation_name": result.get("operation_name"),
                "features": {
                    "duration": "~5 seconds",
                    "aspect_ratio": "16:9",
                    "model": "Veo 2.0"
                },
                "message": f"Video generated successfully using Veo 2.0"
            }
        else:
            return {
                "success": False,
                "error": result.get("error", "Unknown error"),
                "model": "veo-2.0-generate-001"
            }

            
    except Exception as e:
        return {"success": False, "error": str(e)}

def check_video_status(operation_name: str) -> Dict[str, Any]:
    """
    Checks the status of a video generation operation.
    
    Args:
        operation_name (str): The operation name from video generation
        
    Returns:
        Dict[str, Any]: Contains operation status and video URL if completed
    """
    
    try:
        from google.auth import default
        from google.auth.transport.requests import Request
        
        # Get credentials and project info
        credentials, project_id = default()
        if not credentials.valid:
            credentials.refresh(Request())
        
        access_token = credentials.token
        location = "us-central1"
        model_id = "veo-2.0-generate-001"
        
        # Check operation status
        fetch_url = f"https://{location}-aiplatform.googleapis.com/v1/projects/{project_id}/locations/{location}/publishers/google/models/{model_id}:fetchPredictOperation"
        fetch_payload = {
            "operationName": operation_name
        }
        
        headers = {
            "Authorization": f"Bearer {access_token}",
            "Content-Type": "application/json"
        }
        
        response = requests.post(fetch_url, headers=headers, json=fetch_payload)
        
        if response.status_code == 200:
            result = response.json()
            
            if result.get("done"):
                if "error" in result:
                    return {
                        "success": False,
                        "status": "failed",
                        "error": str(result["error"])
                    }
                else:
                    # Extract video URL from result
                    response_data = result.get("response", {})
                    videos = response_data.get("videos", [])
                    
                    return {
                        "success": True,
                        "status": "completed",
                        "has_video_data": len(videos) > 0,
                        "operation_name": operation_name,
                        "videos": videos
                    }
            else:
                return {
                    "success": True,
                    "status": "in_progress",
                    "operation_name": operation_name,
                    "message": "Video generation in progress..."
                }
        else:
            return {
                "success": False,
                "error": f"Failed to check status: {response.status_code} - {response.text}"
            }
            
    except Exception as e:
        return {"success": False, "error": str(e)}

# Create focused veo generator agent
veo_generator_agent = LlmAgent(
    model='gemini-1.5-flash',
    name='veo_generator_agent',
    instruction="""You generate marketing videos from Veo scripts using Vertex AI Veo 2.0. CRITICAL: Always generate videos WITHOUT any visible text, words, or typography to avoid spelling errors. Focus on pure visual storytelling through action, emotion, and imagery. When given a video script, use generate_single_video to create a professional video and get a video URL. You can also check video generation status with check_video_status.""",
    description="Generates single marketing videos from Veo scripts using Vertex AI Veo 2.0 with no text overlays",
    tools=[generate_single_video, check_video_status]
)

# ADK expects root_agent for module loading
root_agent = veo_generator_agent 