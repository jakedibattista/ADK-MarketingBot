"""
Instagram Specialist Agent
Generates Instagram captions and visual concepts from campaign content using AI
"""

import os
import sys
from typing import Dict, Any
import google.generativeai as genai
from google.cloud import storage
import uuid
import base64
from io import BytesIO

# Configure Gemini API
GOOGLE_API_KEY = os.getenv('GOOGLE_API_KEY')
if not GOOGLE_API_KEY:
    raise ValueError("GOOGLE_API_KEY environment variable is required")

genai.configure(api_key=GOOGLE_API_KEY)

def generate_instagram_content(campaign_content: str, concept_number: int = 1) -> Dict[str, Any]:
    """
    Generate Instagram caption and visual concept from campaign content using AI
    """
    try:
        # Create Instagram specialist prompt
        instagram_prompt = f"""
You are an Instagram marketing specialist. Your job is to create engaging Instagram content from marketing campaigns.

CAMPAIGN CONTENT:
{campaign_content}

TASK: Create Instagram content for concept #{concept_number}

Generate TWO things:

1. INSTAGRAM CAPTION (for social media post):
- Write an engaging Instagram caption with emojis and hashtags
- Make it viral-worthy and shareable
- Include relevant hashtags (5-8 hashtags)
- Keep it authentic and engaging
- Match the campaign's tone and target audience

2. VISUAL DESCRIPTION (for image generation):
- Describe the perfect image to accompany this campaign
- Be specific about setting, people, objects, mood, lighting
- Focus on visual storytelling that matches the campaign
- Include "NO text or words in image" at the end
- Make it different for concept #1 vs #2 (if concept #2, show alternative angle/perspective)

FORMAT YOUR RESPONSE EXACTLY LIKE THIS:
INSTAGRAM_CAPTION: [your engaging caption with emojis and hashtags]
VISUAL_DESCRIPTION: [detailed image description ending with "NO text or words in image"]
"""

        # Generate content using Gemini
        model = genai.GenerativeModel('gemini-1.5-flash')
        response = model.generate_content(instagram_prompt)
        
        if not response or not response.text:
            raise Exception("No response from Gemini model")
        
        content = response.text.strip()
        
        # Parse the response
        caption = ""
        visual_description = ""
        
        lines = content.split('\n')
        for line in lines:
            if line.startswith('INSTAGRAM_CAPTION:'):
                caption = line.replace('INSTAGRAM_CAPTION:', '').strip()
            elif line.startswith('VISUAL_DESCRIPTION:'):
                visual_description = line.replace('VISUAL_DESCRIPTION:', '').strip()
        
        # Fallback parsing if format isn't followed exactly
        if not caption or not visual_description:
            # Try to extract from the full response
            if 'INSTAGRAM_CAPTION:' in content and 'VISUAL_DESCRIPTION:' in content:
                parts = content.split('VISUAL_DESCRIPTION:')
                caption_part = parts[0].replace('INSTAGRAM_CAPTION:', '').strip()
                visual_part = parts[1].strip()
                
                caption = caption_part
                visual_description = visual_part
            else:
                # Last resort - use the full response as caption and create generic visual
                caption = content
                visual_description = f"Professional marketing image showcasing the campaign concept, high-quality commercial photography, engaging composition, NO text or words in image"
        
        # Generate the actual image using the visual description
        image_result = generate_image_from_description(visual_description)
        
        return {
            "success": True,
            "caption": caption,
            "visual_description": visual_description,
            "image_data": image_result["image_data"],
            "filename": image_result.get("filename", ""),
            "concept": f"Concept {concept_number}",
            "error": None
        }
        
    except Exception as e:
        print(f"Instagram content generation failed: {e}")
        return {
            "success": False,
            "caption": "",
            "visual_description": "",
            "image_data": None,
            "filename": "",
            "concept": f"Concept {concept_number}",
            "error": str(e)
        }

def generate_image_from_description(visual_description: str) -> Dict[str, Any]:
    """
    Generate image from visual description using Vertex AI Imagen
    """
    try:
        # Use the existing simple generator for image generation
        sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
        from visual_concept_agent.simple_generator import generate_visual_concept_simple
        
        # Generate the image
        result = generate_visual_concept_simple(visual_description)
        return result
        
    except Exception as e:
        print(f"Image generation failed: {e}")
        return {
            "success": False,
            "image_data": None,
            "filename": "",
            "error": str(e)
        }

# This module is imported and used by the Visual Concept Agent 