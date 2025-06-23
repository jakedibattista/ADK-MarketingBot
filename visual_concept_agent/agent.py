"""
Visual Concept Agent - Single Image Generation Tool
"""

import os
import datetime
from typing import Dict, Any
from google.adk.agents.llm_agent import LlmAgent

def generate_single_image(request: str) -> Dict[str, Any]:
    """
    Generates a single marketing image from a concept and returns the GCS URL.
    
    Args:
        request (str): The marketing concept to visualize (e.g., "Modern family enjoying road trip")
        
    Returns:
        Dict[str, Any]: Contains success status, GCS URL, and filename
    """
    
    try:
        from google import genai
        import tempfile
        
        # Configure with API key
        api_key = os.environ.get('GOOGLE_API_KEY')
        if not api_key:
            return {"success": False, "error": "GOOGLE_API_KEY not found"}
        
        # Initialize the client
        client = genai.Client(api_key=api_key)
        
        # Generate marketing image - NO TEXT to avoid spelling errors
        enhanced_prompt = f"Marketing visual: {request}. Professional, high-quality, brand-appropriate. NO text, words, letters, or typography in the image. Focus on pure visual storytelling through imagery, colors, and composition only."
        
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
            import base64
            base64_image = base64.b64encode(image_bytes).decode('utf-8')
            data_url = f"data:image/jpeg;base64,{base64_image}"
            
            return {
                "success": True,
                "image_data": data_url,
                "filename": filename,
                "concept": request
            }
        else:
            return {"success": False, "error": "No image generated"}
        
    except Exception as e:
        return {"success": False, "error": f"Image generation failed: {str(e)}"}

# Create focused visual concept agent
visual_concept_agent = LlmAgent(
    model='gemini-1.5-flash',
    name='visual_concept_agent',
    instruction="""You generate marketing visuals from concepts. CRITICAL: Always generate images WITHOUT any visible text, words, or typography to avoid spelling errors. Focus on pure visual storytelling through imagery, colors, and composition. When given a marketing concept, use generate_single_image to create a professional image and return the GCS URL.""",
    description="Generates single marketing images from concepts with no text overlays and returns GCS URLs",
    tools=[generate_single_image]
)

# ADK expects root_agent for module loading
root_agent = visual_concept_agent 