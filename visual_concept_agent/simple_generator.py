"""
Simple Visual Concept Generator - Standalone function to avoid token issues
"""

import os
import datetime
import base64
from typing import Dict, Any

def generate_visual_concept_simple(concept: str) -> Dict[str, Any]:
    """
    Simple image generation function that bypasses ADK agent system.
    Directly calls Vertex AI Imagen to avoid token accumulation issues.
    
    Args:
        concept (str): Instagram caption or brief visual concept description
        
    Returns:
        Dict[str, Any]: Contains success status, base64 image data, and Instagram caption
    """
    
    try:
        from google import genai
        
        # Configure with API key
        api_key = os.environ.get('GOOGLE_API_KEY')
        if not api_key:
            return {"success": False, "error": "GOOGLE_API_KEY not found"}
        
        # Initialize the client
        client = genai.Client(api_key=api_key)
        
        # Extract visual elements from Instagram caption and generate image
        # Remove hashtags and emojis for the visual prompt
        import re
        visual_prompt = re.sub(r'#\w+', '', concept)  # Remove hashtags
        visual_prompt = re.sub(r'[^\w\s.,!?-]', '', visual_prompt)  # Remove emojis
        visual_prompt = visual_prompt.strip()
        
        # Generate marketing image - NO TEXT to avoid spelling errors
        enhanced_prompt = f"Marketing visual: {visual_prompt}. Professional, high-quality, brand-appropriate, Instagram-worthy. NO text, words, letters, or typography in the image. Focus on pure visual storytelling through imagery, colors, and composition only."
        
        # Generate image using Imagen
        response = client.models.generate_images(
            model="imagen-3.0-generate-002",
            prompt=enhanced_prompt,
        )
        
        if response.generated_images:
            # Get the generated image
            generated_image = response.generated_images[0]
            image_bytes = generated_image.image.image_bytes
            
            timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"marketing_{timestamp}.jpg"
            
            # Convert to base64 for direct display in frontend
            base64_image = base64.b64encode(image_bytes).decode('utf-8')
            data_url = f"data:image/jpeg;base64,{base64_image}"
            
            return {
                "success": True,
                "image_data": data_url,
                "filename": filename,
                "concept": concept,
                "caption": concept  # The full Instagram caption with emojis and hashtags
            }
        else:
            return {"success": False, "error": "No image generated"}
            
    except Exception as e:
        return {"success": False, "error": f"Image generation failed: {str(e)}"} 