"""
Script Writer Agent Tools
Tools for creating compelling Veo prompts with multiple angles and settings
"""

import logging
from typing import Dict, Any, List, Optional

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def create_veo_prompt(
    visual_concept: str,
    campaign_idea: str,
    company_name: str
) -> Dict[str, Any]:
    """
    Create detailed Veo prompt optimized for video generation
    
    Args:
        visual_concept: Approved visual concept description
        campaign_idea: Selected campaign idea
        company_name: Company name for branding        
    Returns:
        Dict containing detailed Veo prompt and specifications
    """
    
    try:
        # Camera angle variations for dynamic video
        camera_angles = [
            "Wide establishing shot",
            "Medium shot focusing on subject",
            "Close-up detail shot",
            "Dynamic tracking shot"
        ]
        
        # Setting descriptions based on brand style
        setting_styles = {
            "professional": "Clean, modern office environment with natural lighting",
            "casual": "Relaxed, contemporary space with warm lighting",
            "elegant": "Sophisticated, minimalist setting with soft lighting", 
            "bold": "Dynamic, energetic environment with dramatic lighting"
        }
        
        # Audio elements for Veo 2.0
        audio_elements = {
            "inspiring": "Uplifting background music, confident voiceover",
            "exciting": "Dynamic music with energy, enthusiastic narration",
            "trustworthy": "Calm, reassuring background music, professional voiceover",
            "innovative": "Modern, tech-inspired music, forward-thinking narration"
        }
        
        # Build comprehensive Veo prompt with default professional style
        brand_style = "professional"
        target_emotion = "inspiring"
        call_to_action = "Engage with brand"
        
        setting = setting_styles.get(brand_style, setting_styles["professional"])
        audio = audio_elements.get(target_emotion, audio_elements["inspiring"])
        
        # Create multi-angle video prompt
        veo_prompt = f"""
        {camera_angles[0]} of {setting}. Camera smoothly transitions to {camera_angles[1]} showing {visual_concept}. 
        {camera_angles[2]} capturing key details of {campaign_idea} for {company_name}. 
        {camera_angles[3]} following the action with smooth movement. 
        
        Audio: {audio}. 
        
        Visual style: {brand_style} aesthetic with high production value. 
        Mood: {target_emotion} and engaging. 
        
        Brand integration: Subtle {company_name} branding throughout. 
        
        Duration: ~5 seconds optimized for Veo 2.0. 
        Aspect ratio: 16:9 for professional presentation.
        """
        
        # Clean up the prompt
        cleaned_prompt = " ".join(veo_prompt.split())
        
        result = {
            "success": True,
            "veo_prompt": cleaned_prompt,
            "specifications": {
                "duration": "8 seconds",
                "aspect_ratio": "16:9",
                "camera_angles": camera_angles,
                "audio_style": audio,
                "visual_style": brand_style,
                "target_emotion": target_emotion
            },
            "optimization": {
                "veo_version": "3.0",
                "native_audio": True,
                "prompt_enhancement": "Automatic",
                "quality": "Enhanced"
            },
            "brand_integration": {
                "company": company_name,
                "style": brand_style,
                "call_to_action": call_to_action if call_to_action else "Engage with brand"
            }
        }
        
        logger.info(f"Created Veo prompt for {company_name} with {brand_style} style")
        return result
        
    except Exception as e:
        logger.error(f"Veo prompt creation failed: {e}")
        return {
            "success": False,
            "error": str(e),
            "message": "Failed to create Veo prompt"
        }

def optimize_prompt_for_veo(
    base_prompt: str,
    duration_seconds: int = 8,
    aspect_ratio: str = "16:9",
    include_audio: bool = True
) -> Dict[str, Any]:
    """
    Optimize existing prompt for Veo 2.0 specifications
    
    Args:
        base_prompt: Base video prompt to optimize
        duration_seconds: Video duration (~5 seconds for Veo 2.0)
        aspect_ratio: Video aspect ratio (16:9 for Veo 2.0)
        include_audio: Whether to include audio descriptions
        
    Returns:
        Dict containing optimized prompt and Veo specifications
    """
    
    try:
        # Veo 2.0 optimization guidelines
        optimizations = [
            "Enhanced for Veo 2.0 capabilities",
            "~5-second duration with smooth pacing",
            "16:9 aspect ratio composition",
            "Audio generation enabled"
        ]
        
        # Add technical specifications to prompt
        optimized_prompt = f"{base_prompt}. "
        
        if include_audio:
            optimized_prompt += "Include audio with background music and sound effects. "
        
        optimized_prompt += f"Optimized for {duration_seconds}-second duration in {aspect_ratio} format. "
        optimized_prompt += "High-quality video with enhanced motion understanding."
        
        result = {
            "success": True,
            "original_prompt": base_prompt,
            "optimized_prompt": optimized_prompt,
            "veo_specifications": {
                "model": "veo-2.0-generate-001",
                "duration": f"{duration_seconds} seconds",
                "aspect_ratio": aspect_ratio,
                "fps": "24",
                "audio": "Generation enabled" if include_audio else "None"
            },
            "optimizations_applied": optimizations
        }
        
        logger.info("Prompt optimized for Veo 2.0 specifications")
        return result
        
    except Exception as e:
        logger.error(f"Prompt optimization failed: {e}")
        return {
            "success": False,
            "error": str(e),
            "message": "Failed to optimize prompt for Veo"
        }

def create_multi_angle_sequence(
    scene_description: str,
    key_moments: List[str],
    brand_elements: str = "",
    transition_style: str = "smooth"
) -> Dict[str, Any]:
    """
    Create multi-angle video sequence with smooth transitions
    
    Args:
        scene_description: Main scene description
        key_moments: List of key moments to highlight
        brand_elements: Brand elements to integrate
        transition_style: Transition style (smooth, dynamic, cut)
        
    Returns:
        Dict containing multi-angle sequence prompt
    """
    
    try:
        # Define camera movements and angles
        angles = [
            "establishing wide shot",
            "medium tracking shot", 
            "close-up detail shot",
            "dynamic movement shot"
        ]
        
        # Transition styles
        transitions = {
            "smooth": "seamlessly transitions",
            "dynamic": "dynamically cuts",
            "cut": "quickly cuts"
        }
        
        transition = transitions.get(transition_style, "smoothly transitions")
        
        # Build sequence
        sequence_parts = []
        
        # Opening shot
        sequence_parts.append(f"Opening {angles[0]} of {scene_description}")
        
        # Key moments with different angles
        for i, moment in enumerate(key_moments[:3]):  # Limit to 3 moments for 8 seconds
            angle = angles[min(i + 1, len(angles) - 1)]
            sequence_parts.append(f"Camera {transition} to {angle} capturing {moment}")
        
        # Brand integration
        if brand_elements:
            sequence_parts.append(f"Subtle integration of {brand_elements}")
        
        # Combine into cohesive prompt
        multi_angle_prompt = ". ".join(sequence_parts) + "."
        
        result = {
            "success": True,
            "multi_angle_prompt": multi_angle_prompt,
            "sequence_breakdown": {
                "opening": sequence_parts[0],
                "key_moments": sequence_parts[1:-1] if brand_elements else sequence_parts[1:],
                "brand_integration": sequence_parts[-1] if brand_elements else "None"
            },
            "technical_specs": {
                "angles_used": len(sequence_parts),
                "transition_style": transition_style,
                "pacing": "~5-second optimization"
            }
        }
        
        logger.info(f"Created multi-angle sequence with {len(key_moments)} key moments")
        return result
        
    except Exception as e:
        logger.error(f"Multi-angle sequence creation failed: {e}")
        return {
            "success": False,
            "error": str(e),
            "message": "Failed to create multi-angle sequence"
        }

def enhance_prompt_with_audio(
    visual_prompt: str,
    audio_style: str = "professional",
    include_dialogue: bool = False,
    music_genre: str = "corporate"
) -> Dict[str, Any]:
    """
    Enhance video prompt with detailed audio descriptions for Veo 2.0
    
    Args:
        visual_prompt: Base visual prompt
        audio_style: Audio style (professional, casual, energetic, calm)
        include_dialogue: Whether to include dialogue/voiceover
        music_genre: Background music genre
        
    Returns:
        Dict containing audio-enhanced prompt
    """
    
    try:
        # Audio style descriptions
        audio_styles = {
            "professional": "Clean, corporate background music with professional voiceover",
            "casual": "Friendly, approachable music with conversational tone",
            "energetic": "Upbeat, dynamic music with enthusiastic delivery",
            "calm": "Soothing, ambient music with gentle narration"
        }
        
        # Music genre specifications
        music_descriptions = {
            "corporate": "Professional corporate background music",
            "upbeat": "Energetic, motivational music",
            "ambient": "Soft, atmospheric background music",
            "tech": "Modern, tech-inspired background music"
        }
        
        audio_description = audio_styles.get(audio_style, audio_styles["professional"])
        music_desc = music_descriptions.get(music_genre, music_descriptions["corporate"])
        
        # Build enhanced prompt
        enhanced_prompt = f"{visual_prompt}. Audio: {music_desc}"
        
        if include_dialogue:
            enhanced_prompt += f" with {audio_description}"
        else:
            enhanced_prompt += " with subtle sound effects"
        
        enhanced_prompt += ". Veo 2.0 audio generation for high-quality sound design."
        
        result = {
            "success": True,
            "original_prompt": visual_prompt,
            "audio_enhanced_prompt": enhanced_prompt,
            "audio_specifications": {
                "style": audio_style,
                "music_genre": music_genre,
                "dialogue": include_dialogue,
                "sound_effects": True,
                "native_generation": True
            },
            "veo_audio_features": [
                "Native audio generation",
                "Dialogue support",
                "Sound effects",
                "Background music",
                "High-quality audio"
            ]
        }
        
        logger.info(f"Enhanced prompt with {audio_style} audio style")
        return result
        
    except Exception as e:
        logger.error(f"Audio enhancement failed: {e}")
        return {
            "success": False,
            "error": str(e),
            "message": "Failed to enhance prompt with audio"
        }

def validate_veo_prompt(
    prompt: str,
    max_length: int = 1000,
    required_elements: List[str] = None
) -> Dict[str, Any]:
    """
    Validate Veo prompt for optimal generation
    
    Args:
        prompt: Veo prompt to validate
        max_length: Maximum prompt length
        required_elements: List of required elements to check for
        
    Returns:
        Dict containing validation results and suggestions
    """
    
    try:
        if required_elements is None:
            required_elements = ["camera", "lighting", "audio", "duration"]
        
        validation_results = {
            "length_check": len(prompt) <= max_length,
            "current_length": len(prompt),
            "max_length": max_length,
            "required_elements": {},
            "suggestions": []
        }
        
        # Check for required elements
        prompt_lower = prompt.lower()
        for element in required_elements:
            validation_results["required_elements"][element] = element.lower() in prompt_lower
        
        # Generate suggestions
        if not validation_results["length_check"]:
            validation_results["suggestions"].append("Prompt is too long, consider shortening")
        
        missing_elements = [elem for elem, present in validation_results["required_elements"].items() if not present]
        if missing_elements:
            validation_results["suggestions"].append(f"Consider adding: {', '.join(missing_elements)}")
        
        # Check for Veo 2.0 specific elements
        veo_elements = ["16:9", "5 second", "audio"]
        for element in veo_elements:
            if element not in prompt_lower:
                validation_results["suggestions"].append(f"Consider specifying {element} for Veo 2.0 optimization")
        
        validation_results["is_valid"] = (
            validation_results["length_check"] and 
            len(missing_elements) == 0
        )
        
        result = {
            "success": True,
            "validation": validation_results,
            "prompt": prompt,
            "optimization_score": calculate_optimization_score(validation_results)
        }
        
        logger.info(f"Prompt validation completed with score: {result['optimization_score']}/100")
        return result
        
    except Exception as e:
        logger.error(f"Prompt validation failed: {e}")
        return {
            "success": False,
            "error": str(e),
            "message": "Failed to validate Veo prompt"
        }

def calculate_optimization_score(validation_results: Dict[str, Any]) -> int:
    """Calculate optimization score based on validation results"""
    score = 0
    
    # Length check (20 points)
    if validation_results["length_check"]:
        score += 20
    
    # Required elements (60 points total)
    required_count = len(validation_results["required_elements"])
    present_count = sum(validation_results["required_elements"].values())
    if required_count > 0:
        score += int((present_count / required_count) * 60)
    
    # Bonus for no suggestions needed (20 points)
    if len(validation_results["suggestions"]) == 0:
        score += 20
    
    return min(score, 100) 