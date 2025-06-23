"""
ADK Marketing Platform - Cloud Run Service
Receives requests from the Firebase frontend and orchestrates the 6-agent workflow.
"""

import os
import sys
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
from google.adk.runners import Runner
from google.adk.sessions import InMemorySessionService
from google.genai import types
import asyncio

# Add project root to the Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Import the main marketing agent
from marketing_agent.agent import root_agent

# Initialize FastAPI app
app = FastAPI(
    title="ADK Marketing Platform API",
    description="API for orchestrating the multi-agent marketing campaign workflow.",
    version="1.0.0",
)

# --- CORS Configuration ---
# Allow requests from the Firebase frontend and local development
origins = [
    "https://adkchl.web.app",
    "http://localhost",
    "http://localhost:3000",
    "http://localhost:8000",
    "http://127.0.0.1:3000",
    "http://127.0.0.1:8000",
    "*"  # Allow all origins for local development
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# --- Request and Response Models ---
class QueryRequest(BaseModel):
    query: str

class QueryResponse(BaseModel):
    response: str

class VisualConceptRequest(BaseModel):
    concept: str
    campaign_content: str = None  # Add campaign content field

class VisualConceptResponse(BaseModel):
    success: bool
    image_data: str = None
    filename: str = None
    concept: str = None
    caption: str = None  # Add caption field
    visual_description: str = None  # Add visual description field
    error: str = None

# Create session service and runner
session_service = InMemorySessionService()
APP_NAME = "adk_marketing_platform"
USER_ID = "api_user"

# Create runner for the marketing agent
runner = Runner(agent=root_agent, app_name=APP_NAME, session_service=session_service)

# --- API Endpoints ---
@app.get("/", summary="Health Check")
def read_root():
    """Health check endpoint to confirm the service is running."""
    return {"status": "ADK Marketing Platform API is running"}

@app.post("/query", response_model=QueryResponse, summary="Query the Marketing Agent")
async def query_agent(request: QueryRequest):
    """
    Receives a user query, passes it to the main marketing agent,
    and returns the agent's final response.
    """
    print(f"Received query: {request.query}")
    try:
        # Create a session for this request
        import uuid
        session_id = str(uuid.uuid4())
        
        # Create session using await since it's async
        session = await session_service.create_session(
            app_name=APP_NAME, 
            user_id=USER_ID, 
            session_id=session_id
        )
        
        # Create user content
        user_content = types.Content(
            role='user', 
            parts=[types.Part(text=request.query)]
        )
        
        # Run the agent using the async runner
        events = []
        async for event in runner.run_async(
            user_id=USER_ID,
            session_id=session_id,
            new_message=user_content
        ):
            events.append(event)
            # Debug logging
            if hasattr(event, 'content') and event.content:
                text_len = 0
                if hasattr(event.content, 'parts') and event.content.parts and len(event.content.parts) > 0:
                    text_len = len(event.content.parts[0].text) if event.content.parts[0].text else 0
                print(f"Event: {event.content.role} - {text_len} chars")
        
        # Extract the final response from events - collect all model responses
        model_responses = []
        for event in events:
            if (hasattr(event, 'content') and event.content and 
                hasattr(event.content, 'parts') and event.content.parts and 
                len(event.content.parts) > 0 and event.content.parts[0] and
                hasattr(event.content.parts[0], 'text')):
                # Collect all agent responses
                if event.content.role == 'model':
                    response_text = event.content.parts[0].text
                    if response_text and response_text.strip():
                        model_responses.append(response_text)
                        print(f"Collected response: {response_text[:100]}...")
        
        # Use the last non-empty response, or combine all responses
        final_response = ""
        if model_responses:
            # For campaign generation, we want the marketing agent's final response
            # which should contain the formatted campaigns
            final_response = model_responses[-1]
            
            # If the last response is very short, it might be incomplete
            # In that case, combine the responses
            if len(final_response) < 100 and len(model_responses) > 1:
                final_response = "\n\n".join(model_responses[-2:])
        
        # If still no response, try session messages as fallback
        if not final_response:
            try:
                # Get all messages from session
                session_messages = []
                # Note: session_service.get_messages doesn't exist, so we'll skip this
                print("No final response found in events, session fallback not available")
            except Exception as session_error:
                print(f"Could not retrieve session messages: {session_error}")
        
        print(f"Agent response: {final_response}")
        return QueryResponse(response=final_response or "No response generated from agent")
        
    except Exception as e:
        print(f"An error occurred: {e}")
        import traceback
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=str(e))

# To run this app locally for testing:
# uvicorn service.main:app --reload

@app.post("/generate-visual", response_model=VisualConceptResponse, summary="Generate Visual Concept")
async def generate_visual_concept(request: VisualConceptRequest):
    """
    Generate Instagram caption and visual concept from campaign content using AI
    """
    print(f"Generating visual concept for: {request.concept}")
    try:
        # If we have campaign content, use AI to generate Instagram content
        if request.campaign_content:
            print(f"Using campaign content for AI generation: {request.campaign_content[:200]}...")
            
            # Import Google Generative AI
            from google import genai
            
            # Configure Gemini API
            GOOGLE_API_KEY = os.getenv('GOOGLE_API_KEY')
            if not GOOGLE_API_KEY:
                raise ValueError("GOOGLE_API_KEY environment variable is required")
            
            client = genai.Client(api_key=GOOGLE_API_KEY)
            
            # Create Instagram specialist prompt
            instagram_prompt = f"""
You are an Instagram marketing specialist. Create engaging Instagram content from this marketing campaign.

SELECTED CAMPAIGN:
{request.campaign_content}

CONCEPT NUMBER: {request.concept}

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
- Make it different for concept 1 vs concept 2

FORMAT YOUR RESPONSE EXACTLY LIKE THIS:
INSTAGRAM_CAPTION: [your engaging caption with emojis and hashtags]
VISUAL_DESCRIPTION: [detailed image description ending with "NO text or words in image"]
"""

            # Generate content using Gemini
            response = client.models.generate_content(
                model='gemini-1.5-flash',
                contents=instagram_prompt
            )
            
            if not response or not hasattr(response, 'text') or not response.text:
                raise Exception("No response from Gemini model")
            
            content = response.text.strip()
            print(f"AI Generated Content: {content}")
            
            # Parse the response
            caption = ""
            visual_description = ""
            
            if content:
                lines = content.split('\n')
                for line in lines:
                    if line and line.startswith('INSTAGRAM_CAPTION:'):
                        caption = line.replace('INSTAGRAM_CAPTION:', '').strip()
                    elif line and line.startswith('VISUAL_DESCRIPTION:'):
                        visual_description = line.replace('VISUAL_DESCRIPTION:', '').strip()
                
                # Fallback parsing if format isn't followed exactly
                if not caption or not visual_description:
                    if 'INSTAGRAM_CAPTION:' in content and 'VISUAL_DESCRIPTION:' in content:
                        try:
                            parts = content.split('VISUAL_DESCRIPTION:')
                            if len(parts) >= 2:
                                caption_part = parts[0].replace('INSTAGRAM_CAPTION:', '').strip()
                                visual_part = parts[1].strip()
                                
                                if not caption and caption_part:
                                    caption = caption_part
                                if not visual_description and visual_part:
                                    visual_description = visual_part
                        except Exception as parse_error:
                            print(f"Parsing error: {parse_error}")
                    
                    # Last resort - use the full response as caption and create generic visual
                    if not caption:
                        caption = content if content else "Generated Instagram content"
                    if not visual_description:
                        visual_description = f"Professional marketing image showcasing the campaign concept, high-quality commercial photography, engaging composition, NO text or words in image"
            
            print(f"Parsed Caption: {caption}")
            print(f"Parsed Visual Description: {visual_description}")
            
            # Use the visual description for image generation
            image_concept = visual_description
        else:
            # Fallback to original concept if no campaign content provided
            image_concept = request.concept if request.concept else "Professional marketing image"
            caption = request.concept if request.concept else "Marketing content"
            visual_description = request.concept if request.concept else "Professional marketing image"
        
        # Import the simple generator for image generation
        sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
        from visual_concept_agent.simple_generator import generate_visual_concept_simple
        
        # Generate the visual concept using the AI-generated description
        result = generate_visual_concept_simple(image_concept)
        
        # Add the caption and visual description to the response
        result['caption'] = caption
        result['visual_description'] = visual_description
        result['concept'] = f"Concept {request.concept}"
        
        return VisualConceptResponse(**result)
        
    except Exception as e:
        print(f"Visual concept generation failed: {e}")
        import traceback
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/generate-instagram-content", summary="Generate Instagram Content from Campaign")
async def generate_instagram_content_endpoint(request: dict):
    """
    Generate Instagram caption and visual concept from campaign content using AI specialist
    """
    try:
        campaign_content = request.get('campaign_content', '')
        concept_number = request.get('concept_number', 1)
        
        print(f"Generating Instagram content for concept #{concept_number}")
        print(f"Campaign content: {campaign_content[:200]}...")
        
        # Import the Instagram specialist
        sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
        from visual_concept_agent.instagram_specialist import generate_instagram_content
        
        # Generate Instagram content
        result = generate_instagram_content(campaign_content, concept_number)
        
        return result
        
    except Exception as e:
        print(f"Instagram content generation failed: {e}")
        import traceback
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/generate-script", summary="Generate Veo 2.0 Script from Campaign and Visual Concept")
async def generate_script(request: dict):
    """
    Generate a detailed Veo 2.0 script using the Script Writer Agent
    """
    try:
        campaign_content = request.get('campaign_content', '')
        visual_concept = request.get('visual_concept', '')
        company_name = request.get('company_name', '')
        
        print(f"Generating Veo 2.0 script for campaign and visual concept")
        print(f"Campaign: {campaign_content[:100]}...")
        print(f"Visual: {visual_concept[:100]}...")
        
        # Import the script writer agent
        sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
        from script_writer_agent.agent import root_agent as script_writer_agent
        
        # Create session service and runner for script writer
        import uuid
        session_id = str(uuid.uuid4())
        
        session = await session_service.create_session(
            app_name=APP_NAME, 
            user_id=USER_ID, 
            session_id=session_id
        )
        
        # Create script generation request
        script_request = f"""Create a detailed Veo 2.0 script for this marketing campaign:

COMPANY: {company_name}

SELECTED CAMPAIGN:
{campaign_content}

APPROVED VISUAL CONCEPT:
{visual_concept}

Generate a professional ~5-second Veo 2.0 video script that includes:
- Multiple camera angles and movements
- Rich visual descriptions
- Natural brand integration
- 16:9 aspect ratio composition
- Cinematic lighting and mood
- IMPORTANT: Include "NO visible text, words, letters, or typography" to avoid spelling errors

Make it specific to this campaign and visual concept, not generic."""

        user_content = types.Content(
            role='user', 
            parts=[types.Part(text=script_request)]
        )
        
        # Create runner for script writer agent
        script_runner = Runner(agent=script_writer_agent, app_name=APP_NAME, session_service=session_service)
        
        # Run the script writer agent
        events = []
        async for event in script_runner.run_async(
            user_id=USER_ID,
            session_id=session_id,
            new_message=user_content
        ):
            events.append(event)
        
        # Extract the script from events
        script_responses = []
        for event in events:
            if (hasattr(event, 'content') and event.content and 
                hasattr(event.content, 'parts') and event.content.parts and 
                len(event.content.parts) > 0 and event.content.parts[0] and
                hasattr(event.content.parts[0], 'text')):
                if event.content.role == 'model':
                    response_text = event.content.parts[0].text
                    if response_text and response_text.strip():
                        script_responses.append(response_text)
        
        # Use the last response as the script
        final_script = script_responses[-1] if script_responses else "Default script generation failed"
        
        return {
            "success": True,
            "script": final_script,
            "campaign_content": campaign_content,
            "visual_concept": visual_concept,
            "message": "Veo 2.0 script generated successfully"
        }
        
    except Exception as e:
        print(f"Script generation failed: {e}")
        import traceback
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/generate-video-direct", summary="Generate Video Directly with Veo 2.0")
async def generate_video_direct(request: dict):
    """
    Direct Veo 2.0 video generation endpoint - matches deployed working version
    """
    try:
        script = request.get('script', '')
        campaign_content = request.get('campaign_content', '')
        visual_concept = request.get('visual_concept', '')
        
        print(f"Generating Veo 2.0 video directly")
        print(f"Script: {script[:200]}...")
        
        # Import the working Veo 2.0 generator
        sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
        from veo_generator_agent.simple_veo_generator import generate_veo_video_simple
        
        # Generate the video using Veo 2.0 (working deployed version)
        result = generate_veo_video_simple(script)
        
        return result
        
    except Exception as e:
        print(f"Direct video generation failed: {e}")
        import traceback
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=str(e))

# Add static file serving (optional)
import os
if os.path.exists("static"):
    app.mount("/static", StaticFiles(directory="static"), name="static")

# Run the server
if __name__ == "__main__":
    import uvicorn
    print("🚀 Starting ADK Marketing Platform server...")
    print("📍 Server will be available at: http://localhost:8080")
    print("📋 API documentation at: http://localhost:8080/docs")
    uvicorn.run(app, host="0.0.0.0", port=8080) 