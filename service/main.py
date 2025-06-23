"""
ADK Marketing Platform - Hybrid Architecture Service
FastAPI service with specialized agent endpoints for research and creative development
"""

import asyncio
import json
import logging
import os
import uuid
from datetime import datetime
from typing import Dict, Any, List, Optional

import uvicorn
from fastapi import FastAPI, HTTPException, BackgroundTasks, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from pydantic import BaseModel

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Import ADK components
from google.adk.runners import Runner
from google.adk.sessions import InMemorySessionService
from google.genai import types

# Add parent directory to path for imports
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Import ADK multi-agent coordinator and individual agents
from marketing_agent.campaign_coordinator import root_agent as campaign_coordinator  # Main coordinator
from marketing_agent.campaign_coordinator import campaign_pipeline  # Sequential pipeline
from marketing_agent.agent import root_agent as marketing_agent  # Google Search agent
from research_specialist.agent import root_agent as research_specialist_agent  # Analysis agent
from creative_director.agent import root_agent as creative_director_agent
from visual_concept_agent.agent import visual_concept_agent
from script_writer_agent.agent import root_agent as script_writer_agent
from veo_generator_agent.agent import root_agent as veo_generator_agent

# Request/Response Models
class MarketingRequest(BaseModel):
    company: str
    website: str
    goals: str
    target_audience: str

class ResearchRequest(BaseModel):
    company: str
    website: str
    goals: str
    target_audience: str

class CreativeRequest(BaseModel):
    research_report: str
    company: str
    goals: str
    target_audience: str

class HybridCampaignRequest(BaseModel):
    company: str
    website: str
    goals: str
    target_audience: str

class VisualConceptRequest(BaseModel):
    campaign: str
    campaign_content: Optional[str] = None
    brand_style: Optional[str] = None
    target_audience: str

class VisualConceptResponse(BaseModel):
    success: bool
    visual_concept: str
    session_id: str
    timestamp: str
    caption: Optional[str] = None
    visual_description: Optional[str] = None
    filename: Optional[str] = None

# Initialize FastAPI app
app = FastAPI(
    title="ADK Marketing Platform - Hybrid Architecture",
    description="Specialized agent endpoints for research and creative development",
    version="2.0.0"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Add validation error handler
@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    print(f"🚨 VALIDATION ERROR on {request.method} {request.url.path}")
    print(f"Request body: {await request.body()}")
    print(f"Validation errors: {exc.errors()}")
    return JSONResponse(
        status_code=422,
        content={"detail": exc.errors(), "body": str(await request.body())}
    )

# Initialize ADK components for each agent
APP_NAME = "adk_marketing_platform_hybrid"
USER_ID = "marketing_user"

# ADK Multi-Agent Coordinator Setup (NEW - Proper ADK Pattern)
coordinator_session_service = InMemorySessionService()
coordinator_runner = Runner(agent=campaign_coordinator, app_name=f"{APP_NAME}_coordinator", session_service=coordinator_session_service)

# Sequential Pipeline Setup (Alternative ADK Pattern)
pipeline_session_service = InMemorySessionService()
pipeline_runner = Runner(agent=campaign_pipeline, app_name=f"{APP_NAME}_pipeline", session_service=pipeline_session_service)

# Individual Agent Setup (Legacy endpoints)
# Marketing Agent Setup (Google Search)
marketing_session_service = InMemorySessionService()
marketing_runner = Runner(agent=marketing_agent, app_name=f"{APP_NAME}_marketing", session_service=marketing_session_service)

# Research Specialist Setup (Analysis)
analysis_session_service = InMemorySessionService()
analysis_runner = Runner(agent=research_specialist_agent, app_name=f"{APP_NAME}_analysis", session_service=analysis_session_service)

# Creative Director Setup  
creative_session_service = InMemorySessionService()
creative_runner = Runner(agent=creative_director_agent, app_name=f"{APP_NAME}_creative", session_service=creative_session_service)

# Other agents setup (existing)
visual_session_service = InMemorySessionService()
visual_runner = Runner(agent=visual_concept_agent, app_name=f"{APP_NAME}_visual", session_service=visual_session_service)

script_session_service = InMemorySessionService()
script_runner = Runner(agent=script_writer_agent, app_name=f"{APP_NAME}_script", session_service=script_session_service)

veo_session_service = InMemorySessionService()
veo_runner = Runner(agent=veo_generator_agent, app_name=f"{APP_NAME}_veo", session_service=veo_session_service)

def format_campaign_concepts(grok_result: dict, company: str, target_audience: str) -> str:
    """
    Format Grok API response into nice campaign presentation layouts
    """
    try:
        campaign_ideas = grok_result.get('campaign_ideas', [])
        if not campaign_ideas:
            return "No campaign concepts generated. Please try again."
        
        formatted_output = f"""🎨 CREATIVE CAMPAIGN CONCEPTS FOR {company.upper()}

🎯 **Target Audience:** {target_audience}
📊 **Research Source:** {grok_result.get('source', 'Grok API')}
⏰ **Generated:** {grok_result.get('generated_date', 'Now')}

"""
        
        for i, idea in enumerate(campaign_ideas[:2], 1):  # Limit to 2 campaigns
            formatted_output += f"""
**CAMPAIGN {i}: {idea.get('title', 'Untitled Campaign')}**
📢 **Tagline:** {idea.get('key_messages', [''])[0] if idea.get('key_messages') else 'Creative tagline needed'}
🎯 **Target:** {idea.get('target_audience', target_audience)}
💡 **Key Message:** {idea.get('description', 'Campaign description needed')}
🏆 **Positioning:** {idea.get('approach', 'Strategic positioning needed')}
🎨 **Visual Concept:** {idea.get('tone', 'Visual direction needed')} style with {', '.join(idea.get('channels', ['digital']))} focus
📋 **Content Strategy:** {', '.join(idea.get('content_pillars', ['Brand awareness', 'Engagement', 'Conversion']))}
📱 **Channel Mix:** {', '.join(idea.get('channels', ['Social Media', 'Digital Advertising']))}
📈 **Success Metrics:** Engagement rate, conversion rate, brand awareness lift

---
"""
        
        formatted_output += f"""
🔍 **RESEARCH INTEGRATION:**
These campaigns leverage the comprehensive market research showing {company}'s competitive advantages and target audience insights. Each concept is designed to address specific pain points and motivations identified in the research phase.

🎯 **NEXT STEPS:**
1. Select preferred campaign concept
2. Develop detailed creative brief
3. Create visual mockups and content calendar
4. Launch pilot campaign for testing

📋 **CAMPAIGN DEVELOPMENT COMPLETE** - Ready for client selection and visual production
"""
        
        return formatted_output
        
    except Exception as e:
        print(f"❌ Campaign formatting error: {e}")
        return f"Campaign formatting failed: {str(e)}\n\nRaw Grok Response:\n{str(grok_result)}"

async def query_agent(runner, session_service, query: str, session_id: str = None):
    """Generic function to query any agent"""
    if session_id is None:
        session_id = str(uuid.uuid4())
    
    try:
        session = await session_service.create_session(
            app_name=runner.app_name,
            user_id=USER_ID,
            session_id=session_id
        )
        
        content = types.Content(role='user', parts=[types.Part(text=query)])
        
        response_text = ""
        async for event in runner.run_async(
            user_id=USER_ID,
            session_id=session_id,
            new_message=content
        ):
            if event.content and event.content.parts:
                text_len = len(event.content.parts[0].text) if event.content.parts[0].text else 0
                print(f"Event: {event.content.role} - {text_len} chars")
                
                if event.content.role == 'model':
                    if event.content.parts[0].text:
                        response_text += event.content.parts[0].text
                    else:
                        print(f"⚠️ Warning: Empty text in model response part")
        
        return {"response": response_text, "session_id": session_id}
        
    except Exception as e:
        logger.error(f"An error occurred: {e}")
        raise HTTPException(status_code=500, detail=f"Agent query failed: {str(e)}")

@app.get("/")
async def root():
    return {
        "message": "ADK Marketing Platform - Hybrid Architecture",
        "version": "2.0.0",
        "architecture": "Specialized agent endpoints",
        "endpoints": {
            "adk-campaign": "/adk-campaign - ADK Multi-Agent Coordinator (RECOMMENDED)",
            "adk-pipeline": "/adk-pipeline - ADK Sequential Pipeline (ALTERNATIVE)",
            "research": "/research - Market intelligence gathering (LEGACY)",
            "creative": "/creative - Campaign development (LEGACY)",
            "hybrid": "/hybrid-campaign - Complete workflow (LEGACY)",
            "visual": "/generate-visual - Visual concept generation",
            "script": "/generate-script - Script writing",
            "video": "/generate-video-direct - Video generation"
        }
    }

@app.post("/research")
async def research_endpoint(request: ResearchRequest):
    """Specialized endpoint for market research using Gemini knowledge base"""
    print(f"Research request: {request.company} - {request.website}")
    
    query = f"""
    Company: {request.company}
    Website: {request.website}
    Target Audience: {request.target_audience}
    Goals: {request.goals}
    
    Please provide comprehensive market intelligence using your training knowledge.
    """
    
    try:
        result = await query_agent(marketing_runner, marketing_session_service, query)
        return JSONResponse(content={
            "success": True,
            "research_report": result["response"],
            "session_id": result["session_id"],
            "timestamp": datetime.now().isoformat()
        })
    except Exception as e:
        logger.error(f"Research endpoint error: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/creative")
async def creative_endpoint(request: CreativeRequest):
    """Specialized endpoint for campaign development using Grok API"""
    print(f"Creative request for: {request.company}")
    
    query = f"""
    Research Intelligence Report:
    {request.research_report}
    
    Company: {request.company}
    Target Audience: {request.target_audience}
    Goals: {request.goals}
    
    Based on this research intelligence, please develop 2 innovative campaign concepts.
    """
    
    try:
        result = await query_agent(creative_runner, creative_session_service, query)
        return JSONResponse(content={
            "success": True,
            "campaign_concepts": result["response"],
            "session_id": result["session_id"],
            "timestamp": datetime.now().isoformat()
        })
    except Exception as e:
        logger.error(f"Creative endpoint error: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/hybrid-campaign")
async def hybrid_campaign_endpoint(request: HybridCampaignRequest):
    """Complete hybrid workflow: Research → Creative → Campaign"""
    print(f"Hybrid campaign request: {request.company} - {request.website}")
    
    try:
        # Step 1: Research Phase
        print("🔍 Phase 1: Market Research")
        research_request = ResearchRequest(
            company=request.company,
            website=request.website,
            goals=request.goals,
            target_audience=request.target_audience
        )
        research_result = await research_endpoint(research_request)
        
        # Extract research report properly from JSONResponse
        if hasattr(research_result, 'body'):
            research_data = json.loads(research_result.body.decode())
        else:
            # research_result is already a JSONResponse object
            research_data = research_result.__dict__
            if 'body' in research_data:
                research_data = json.loads(research_data['body'])
        
        raw_research_data = research_data.get("research_report", "")
        print(f"📋 Raw research data length: {len(raw_research_data)} chars")
        print(f"📋 Raw research preview: {raw_research_data[:200]}...")
        
        # Step 2: Research Analysis Phase
        print("📊 Phase 2: Research Analysis")
        analysis_query = f"""
        Raw Research Data from Marketing Agent:
        {raw_research_data}
        
        Company: {request.company}
        Target Audience: {request.target_audience}
        Goals: {request.goals}
        
        Please analyze this raw research data and create a comprehensive intelligence report.
        """
        
        analysis_result = await query_agent(analysis_runner, analysis_session_service, analysis_query)
        research_report = analysis_result["response"]
        print(f"📋 Structured research report length: {len(research_report)} chars")
        print(f"📋 Structured report preview: {research_report[:200]}...")
        
        # Step 3: Get Raw Campaign Ideas from Grok API
        print("🎨 Phase 3a: Grok API Call")
        
        # Import and call Grok directly to get raw campaign ideas
        from creative_director.tools import grok_creative_assistant
        
        grok_result = grok_creative_assistant(
            research_report=research_report,
            goals_audience=f"{request.target_audience} - {request.goals}",
            company_name=request.company
        )
        
        print(f"📋 Grok result status: {grok_result.get('status', 'unknown')}")
        print(f"📋 Campaign ideas count: {len(grok_result.get('campaign_ideas', []))}")
        print(f"📋 Grok source: {grok_result.get('source', 'unknown')}")
        
        # DEBUG: Print the actual Grok response structure
        print(f"🔍 DEBUG: Grok response keys: {list(grok_result.keys())}")
        print(f"🔍 DEBUG: First 500 chars of Grok response: {str(grok_result)[:500]}")
        
        # Step 4: Creative Director Agent Formats the Grok Response
        print("🎨 Phase 3b: Creative Director Processing")
        
        creative_query = f"""
        Raw Grok API Response:
        {str(grok_result)}
        
        Research Intelligence Report:
        {research_report}
        
        Company: {request.company}
        Target Audience: {request.target_audience}
        Goals: {request.goals}
        
        Your task is to take the raw Grok API response above and transform it into beautiful, structured campaign presentations that users can easily select from. 
        
        Create 2 polished campaign concepts with:
        - Campaign names and taglines
        - Key messaging and positioning
        - Visual concepts and creative direction  
        - Channel strategies and tactics
        - Success metrics and KPIs
        - Implementation timelines
        
        Format these as professional campaign presentations ready for client selection.
        """
        
        creative_result = await query_agent(creative_runner, creative_session_service, creative_query)
        campaign_concepts = creative_result["response"]
        
        print(f"📋 Campaign concepts length: {len(campaign_concepts)} chars")
        print(f"📋 Campaign concepts preview: {campaign_concepts[:200]}...")
        
        return JSONResponse(content={
            "success": True,
            "workflow": "hybrid",
            "research_report": research_report,
            "campaign_concepts": campaign_concepts,
            "timestamp": datetime.now().isoformat(),
            "message": "Complete hybrid workflow executed successfully"
        })
        
    except Exception as e:
        logger.error(f"Hybrid campaign error: {e}")
        raise HTTPException(status_code=500, detail=f"Hybrid workflow failed: {str(e)}")

# Legacy endpoint for backward compatibility
@app.post("/query")
async def legacy_query_endpoint(request: MarketingRequest):
    """Legacy endpoint - redirects to hybrid workflow"""
    print(f"🔍 DEBUG: Received request data:")
    print(f"  Company: {request.company}")
    print(f"  Website: {request.website}")
    print(f"  Goals: {request.goals}")
    print(f"  Target Audience: {request.target_audience}")
    print(f"Legacy query redirected to hybrid workflow: {request.company}")
    
    hybrid_request = HybridCampaignRequest(
        company=request.company,
        website=request.website,
        goals=request.goals,
        target_audience=request.target_audience
    )
    
    return await hybrid_campaign_endpoint(hybrid_request)

# To run this app locally for testing:
# uvicorn service.main:app --reload

@app.post("/generate-visual", response_model=VisualConceptResponse, summary="Generate Visual Concept")
async def generate_visual_concept(request: VisualConceptRequest):
    """
    Generate Instagram caption and visual concept from campaign content using AI
    """
    print(f"Generating visual concept for: {request.campaign}")
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

CONCEPT NUMBER: {request.campaign}

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
            image_concept = request.campaign if request.campaign else "Professional marketing image"
            caption = request.campaign if request.campaign else "Marketing content"
            visual_description = request.campaign if request.campaign else "Professional marketing image"
        
        # Import the simple generator for image generation
        sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
        from visual_concept_agent.simple_generator import generate_visual_concept_simple
        
        # Generate the visual concept using the AI-generated description
        result = generate_visual_concept_simple(image_concept)
        
        # Add the caption and visual description to the response
        result['caption'] = caption
        result['visual_description'] = visual_description
        result['concept'] = f"Concept {request.campaign}"
        
        # Create the proper response structure for VisualConceptResponse
        import uuid
        import datetime
        
        response_data = {
            "success": result.get('success', False),
            "visual_concept": result.get('image_data', ''),  # Base64 image data
            "session_id": str(uuid.uuid4()),
            "timestamp": datetime.datetime.now().isoformat()
        }
        
        # Add additional data that frontend might need
        if result.get('caption'):
            response_data['caption'] = result['caption']
        if result.get('visual_description'):
            response_data['visual_description'] = result['visual_description']
        if result.get('filename'):
            response_data['filename'] = result['filename']
        
        return VisualConceptResponse(**response_data)
        
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
        
        session = await veo_session_service.create_session(
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
        script_runner = Runner(agent=script_writer_agent, app_name=APP_NAME, session_service=veo_session_service)
        
        # Run the script writer agent
        events = []
        async for event in script_runner.run_async(
            user_id=USER_ID,
            session_id=session_id,
            new_message=user_content
        ):
            events.append(event)
        
        # Extract the script from events - look for function call results and text responses
        script_responses = []
        function_call_scripts = []
        
        for event in events:
            if hasattr(event, 'content') and event.content and hasattr(event.content, 'parts') and event.content.parts:
                for part in event.content.parts:
                    # Look for function calls with create_veo_script
                    if hasattr(part, 'function_call') and part.function_call:
                        if part.function_call.name == 'create_veo_script':
                            script_content = part.function_call.args.get('request', '')
                            if script_content and script_content.strip():
                                function_call_scripts.append(script_content)
                                print(f"Found script in function call: {script_content[:200]}...")
                    
                    # Also look for function responses
                    if hasattr(part, 'function_response') and part.function_response:
                        if part.function_response.name == 'create_veo_script':
                            response_result = part.function_response.response.get('result', '')
                            if response_result and response_result.strip():
                                function_call_scripts.append(response_result)
                                print(f"Found script in function response: {response_result[:200]}...")
                    
                    # Look for text responses
                    if hasattr(part, 'text') and part.text:
                        if event.content.role == 'model':
                            response_text = part.text
                            if response_text and response_text.strip():
                                script_responses.append(response_text)
        
        # Prefer the function call script over text responses
        if function_call_scripts:
            final_script = function_call_scripts[-1]  # Use the last/most refined script
            print(f"Using function call script: {final_script[:200]}...")
        elif script_responses:
            final_script = script_responses[-1]
            print(f"Using text response script: {final_script[:200]}...")
        else:
            final_script = "Default script generation failed"
            print("No script found in events")
        
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