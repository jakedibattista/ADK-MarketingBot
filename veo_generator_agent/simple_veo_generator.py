"""
Simple Veo 2.0 Video Generator
Direct video generation using google-genai library with Veo 2.0
"""

import os
import sys
import time
from typing import Dict, Any

def generate_veo_video_simple(script: str) -> Dict[str, Any]:
    """
    Generate video using Veo 2.0 directly via google-genai library
    """
    try:
        # Import google-genai library
        from google import genai
        from google.genai import types
        
        # Configure API key
        GOOGLE_API_KEY = os.getenv('GOOGLE_API_KEY')
        if not GOOGLE_API_KEY:
            raise ValueError("GOOGLE_API_KEY environment variable is required")
        
        client = genai.Client(api_key=GOOGLE_API_KEY)
        
        print(f"Generating Veo 2.0 video with script: {script[:100]}...")
        
        # Generate video using Veo 2.0
        operation = client.models.generate_videos(
            model="veo-2.0-generate-001",
            prompt=script,
            config=types.GenerateVideosConfig(
                person_generation="allow_adult",  # Allow people in videos
                aspect_ratio="16:9",  # Only supported ratios: "16:9" or "9:16"
            ),
        )
        
        print(f"Veo 2.0 operation started: {operation.name}")
        
        # Wait for completion (up to 5 minutes)
        max_wait_time = 300
        start_time = time.time()
        
        while not operation.done and (time.time() - start_time) < max_wait_time:
            elapsed = int(time.time() - start_time)
            print(f"Waiting for video generation... {elapsed}s elapsed")
            time.sleep(20)  # Check every 20 seconds
            operation = client.operations.get(operation)
        
        elapsed_time = int(time.time() - start_time)
        
        if operation.done:
            print(f"Video generation completed in {elapsed_time}s")
            
            # Extract video information
            result = {
                "success": True,
                "operation_name": operation.name,
                "status": "completed",
                "elapsed_time": elapsed_time,
                "message": f"Veo 2.0 video generated successfully in {elapsed_time}s",
                "model": "veo-2.0-generate-001",
                "features": {
                    "duration": "~5 seconds",
                    "aspect_ratio": "16:9",
                    "model": "Veo 2.0"
                }
            }
            
            # Get video URLs if available
            if hasattr(operation, 'response') and operation.response:
                if hasattr(operation.response, 'generated_videos'):
                    videos = operation.response.generated_videos
                    if videos is not None:
                        result["video_count"] = len(videos)
                        result["videos"] = []
                    else:
                        result["video_count"] = 0
                        result["videos"] = []
                        videos = []
                    
                    for i, video in enumerate(videos):
                        video_info = {
                            "index": i,
                            "model": "veo-2.0-generate-001",
                            "available": True
                        }
                        
                        if hasattr(video, 'video') and video.video:
                            if hasattr(video.video, 'uri'):
                                # For Gemini API, we need to append the API key to download
                                video_uri = video.video.uri
                                if '?' in video_uri:
                                    video_url = f"{video_uri}&key={GOOGLE_API_KEY}"
                                else:
                                    video_url = f"{video_uri}?key={GOOGLE_API_KEY}"
                                
                                video_info["uri"] = video_url
                                result["video_url"] = video_url  # Primary video URL
                                video_info["available"] = True
                            else:
                                video_info["available"] = False
                        else:
                            video_info["available"] = False
                        
                        result["videos"].append(video_info)
                        
                    print(f"Generated {len(videos)} video(s)")
                    if result.get("video_url"):
                        print(f"Video URL: {result['video_url']}")
                else:
                    # No generated_videos attribute
                    result["video_count"] = 0
                    result["videos"] = []
                    result["response_details"] = str(operation.response)
            else:
                # No response or response is None
                result["video_count"] = 0
                result["videos"] = []
                result["response_details"] = "No response from operation"
            
            return result
            
        else:
            # Timeout but operation may still be running
            return {
                "success": False,
                "operation_name": operation.name,
                "status": "timeout",
                "elapsed_time": elapsed_time,
                "message": f"Video generation timed out after {max_wait_time}s (may still be processing)",
                "error": "Generation timeout - video may still be processing in background"
            }
            
    except Exception as e:
        print(f"Veo 2.0 video generation failed: {e}")
        import traceback
        traceback.print_exc()
        
        return {
            "success": False,
            "error": str(e),
            "error_type": type(e).__name__,
            "message": "Veo 2.0 video generation failed",
            "status": "error"
        }

# This module is imported and used by the Veo Generator Agent 