"""
Creative Director Tools
Tools for creative strategy and campaign idea generation using Grok API
"""

import datetime
import json
import requests
import os
from typing import Dict, Any
from google.adk.tools import FunctionTool

# Load environment variables from .env file
try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    # If python-dotenv is not installed, continue without it
    pass

def grok_creative_assistant(
    research_report: str,
    goals_audience: str,
    company_name: str
) -> Dict[str, Any]:
    """
    Use Grok API to generate creative campaign ideas based on research.
    
    Args:
        research_report: Research insights from Research Specialist
        goals_audience: Campaign goals and target audience
        company_name: Name of the company
        
    Returns:
        Dict containing 2 creative campaign ideas from Grok
    """
    
    try:
        print("🔍 DEBUG: Starting Grok API call...")
        
        # Get API key from environment
        grok_api_key = os.getenv('GROK_API_KEY')
        print(f"🔑 DEBUG: GROK_API_KEY loaded: {grok_api_key[:15] if grok_api_key else 'None'}...")
        print(f"📏 DEBUG: API key length: {len(grok_api_key) if grok_api_key else 0}")
        
        if not grok_api_key:
            # Fallback to mock data if no API key is provided
            print("❌ DEBUG: Grok API key not provided, using mock data.")
            return _generate_mock_ideas(research_report, goals_audience, company_name)
        
        print("✅ DEBUG: API key found, proceeding with Grok API call...")
        
        # Prepare the prompt for Grok
        grok_prompt = f"""
        You are a creative director helping to develop marketing campaign ideas.
        
        Company: {company_name}
        Goals & Target Audience: {goals_audience}
        
        Research Report: {research_report}
        
        Based on this research, create exactly 2 distinct marketing campaign ideas that are:
        1. Current and relevant to the target audience
        2. Aligned with the company's strengths and market position
        3. Differentiated from competitors
        4. Actionable and implementable
        
        For each idea, provide:
        - Title (catchy, memorable name)
        - Description (2-3 sentences explaining the concept)
        - Target audience (specific demographic)
        - Approach (how you'll execute this idea)
        - Key messages (3-4 main points)
        - Content pillars (4 content themes)
        - Channels (best platforms for this idea)
        - Tone (communication style)
        
        Format your response as JSON with this structure:
        {{
            "campaign_ideas": [
                {{
                    "title": "Campaign Name",
                    "description": "Campaign description...",
                    "target_audience": "Specific audience...",
                    "approach": "Execution approach...",
                    "key_messages": ["Message 1", "Message 2", "Message 3"],
                    "content_pillars": ["Pillar 1", "Pillar 2", "Pillar 3", "Pillar 4"],
                    "channels": ["Channel 1", "Channel 2", "Channel 3"],
                    "tone": "Communication tone"
                }}
            ]
        }}
        """
        
        # Make API call to Grok
        print("🌐 DEBUG: Making Grok API request...")
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {grok_api_key}"
        }
        
        payload = {
            "messages": [
                {
                    "role": "user",
                    "content": grok_prompt
                }
            ],
            "model": "grok-3-latest",
            "stream": False,
            "temperature": 0.7
        }
        
        response = requests.post(
            "https://api.x.ai/v1/chat/completions",
            headers=headers,
            json=payload,
            timeout=30
        )
        
        print(f"📡 DEBUG: Grok API response status: {response.status_code}")
        
        if response.status_code == 200:
            print("✅ DEBUG: Grok API call successful!")
            grok_response = response.json()
            content = grok_response.get('choices', [{}])[0].get('message', {}).get('content', '')
            print(f"📝 DEBUG: Grok response length: {len(content)} chars")
            
            # Try to parse JSON from Grok's response
            try:
                # Extract JSON from the response (Grok might include extra text)
                start_idx = content.find('{')
                end_idx = content.rfind('}') + 1
                if start_idx != -1 and end_idx != -1:
                    json_content = content[start_idx:end_idx]
                    parsed_ideas = json.loads(json_content)
                    
                    return {
                        "status": "success",
                        "company_name": company_name,
                        "generated_date": datetime.datetime.now().isoformat(),
                        "grok_analysis": {
                            "api_used": "grok-3-latest",
                            "model_response": "Successfully generated creative ideas",
                            "research_incorporated": True
                        },
                        "campaign_ideas": parsed_ideas.get("campaign_ideas", []),
                        "source": "Grok API (X.AI)"
                    }
                else:
                    raise ValueError("No JSON found in Grok response")
                    
            except (json.JSONDecodeError, ValueError) as e:
                # If JSON parsing fails, fall back to mock data
                print(f"Failed to parse Grok JSON response: {e}")
                return _generate_mock_ideas(research_report, goals_audience, company_name)
        
        else:
            print(f"❌ DEBUG: Grok API error: {response.status_code} - {response.text}")
            print("🔄 DEBUG: Falling back to mock data due to API error")
            return _generate_mock_ideas(research_report, goals_audience, company_name)
            
    except Exception as e:
        print(f"💥 DEBUG: Grok API call failed with exception: {e}")
        print("🔄 DEBUG: Falling back to mock data due to exception")
        import traceback
        traceback.print_exc()
        return _generate_mock_ideas(research_report, goals_audience, company_name)

def _generate_mock_ideas(research_report: str, goals_audience: str, company_name: str) -> Dict[str, Any]:
    """Generate mock ideas when Grok API is unavailable"""
    
    # Parse research to make ideas more relevant
    is_tesla = "tesla" in company_name.lower()
    is_tech = "technology" in research_report.lower() or "tech" in goals_audience.lower()
    is_family_focused = "family" in goals_audience.lower() or "dad" in goals_audience.lower()
    
    creative_ideas = {
        "status": "success",
        "company_name": company_name,
        "generated_date": datetime.datetime.now().isoformat(),
        "grok_analysis": {
            "api_used": "mock_fallback",
            "model_response": "Using fallback mock data (Grok API unavailable)",
            "research_incorporated": True
        },
        "campaign_ideas": [],
        "source": "Mock Data (Grok API unavailable)"
    }
    
    if is_family_focused and is_tesla:
        creative_ideas["campaign_ideas"] = [
            {
                "title": "Future Family Adventures",
                "description": "Position Tesla as the perfect vehicle for modern families who want to explore the world while teaching their kids about sustainability. Show real families using Tesla for weekend adventures, road trips, and daily life moments that matter.",
                "target_audience": "Working dads aged 30-45 who value family time and environmental responsibility",
                "approach": "Emotional storytelling with real family moments, emphasizing both adventure and responsibility",
                "key_messages": [
                    "Create memories while creating a better future",
                    "Adventure without compromise",
                    "Teaching kids about sustainability through action"
                ],
                "content_pillars": [
                    "Family adventure stories",
                    "Environmental education moments", 
                    "Safety and reliability features",
                    "Community of Tesla families"
                ],
                "channels": ["Instagram", "YouTube", "Facebook", "TikTok"],
                "tone": "Warm, authentic, inspiring, family-focused"
            },
            {
                "title": "Dad's Smart Choice",
                "description": "Showcase Tesla as the intelligent choice for forward-thinking fathers who research every decision. Focus on the practical benefits, cost savings, and tech features that make dads feel confident about their choice.",
                "target_audience": "Tech-savvy fathers who are primary decision makers for family purchases",
                "approach": "Data-driven storytelling with peer validation and expert endorsements",
                "key_messages": [
                    "The smart dad's choice backed by data",
                    "Technology that makes family life easier",
                    "Investment in your family's future"
                ],
                "content_pillars": [
                    "Cost analysis and savings calculators",
                    "Safety ratings and awards",
                    "Technology features and benefits",
                    "Dad testimonials and reviews"
                ],
                "channels": ["LinkedIn", "YouTube", "Reddit", "Tech blogs"],
                "tone": "Informative, confident, peer-to-peer, trustworthy"
            }
        ]
    elif is_tech:
        creative_ideas["campaign_ideas"] = [
            {
                "title": "Innovation Leadership Story",
                "description": f"Position {company_name} as the company that doesn't just follow trends but creates the future. Show how their innovations solve real problems and improve people's lives in unexpected ways.",
                "target_audience": "Tech professionals and early adopters who value cutting-edge solutions",
                "approach": "Thought leadership content with behind-the-scenes innovation stories",
                "key_messages": [
                    "We don't follow the future, we create it",
                    "Innovation with purpose and impact",
                    "Technology that serves humanity"
                ],
                "content_pillars": [
                    "Innovation process and R&D insights",
                    "Problem-solving case studies",
                    "Future vision and roadmap",
                    "Customer impact stories"
                ],
                "channels": ["LinkedIn", "Medium", "Tech conferences", "YouTube"],
                "tone": "Visionary, intelligent, purposeful, inspiring"
            },
            {
                "title": "Human-Centered Technology",
                "description": f"Show how {company_name}'s technology enhances human connection and experiences rather than replacing them. Focus on the human stories behind the technology.",
                "target_audience": "Professionals who want technology that enhances rather than complicates their lives",
                "approach": "Human-centered storytelling with technology as the enabler",
                "key_messages": [
                    "Technology that brings people together",
                    "Simplifying complexity for better experiences",
                    "Empowering human potential"
                ],
                "content_pillars": [
                    "User experience stories",
                    "Community and connection features",
                    "Accessibility and inclusion",
                    "Work-life balance benefits"
                ],
                "channels": ["Instagram", "TikTok", "YouTube", "Podcasts"],
                "tone": "Human, relatable, empowering, optimistic"
            }
        ]
    else:
        # Generic but high-quality ideas
        creative_ideas["campaign_ideas"] = [
            {
                "title": "Authentic Leadership",
                "description": f"Position {company_name} as an authentic leader that stays true to its values while pushing boundaries. Show the company's journey, challenges, and commitment to excellence.",
                "target_audience": "Consumers who value authenticity and quality over flashy marketing",
                "approach": "Authentic storytelling with transparency and genuine moments",
                "key_messages": [
                    "Real leadership, real results",
                    "Committed to excellence in everything we do",
                    "Building trust through transparency"
                ],
                "content_pillars": [
                    "Company culture and values",
                    "Quality and craftsmanship",
                    "Customer relationships",
                    "Industry leadership"
                ],
                "channels": ["LinkedIn", "YouTube", "Company blog", "Industry publications"],
                "tone": "Authentic, confident, reliable, professional"
            },
            {
                "title": "Community Impact",
                "description": f"Showcase how {company_name} and its customers are making a positive impact in their communities. Focus on real stories of change and improvement.",
                "target_audience": "Socially conscious consumers who want to support companies that make a difference",
                "approach": "Impact storytelling with measurable outcomes and community voices",
                "key_messages": [
                    "Together we create positive change",
                    "Your choice makes a difference",
                    "Building stronger communities"
                ],
                "content_pillars": [
                    "Community partnership stories",
                    "Customer impact initiatives",
                    "Sustainability efforts",
                    "Social responsibility programs"
                ],
                "channels": ["Instagram", "Facebook", "Local media", "Community events"],
                "tone": "Inspiring, inclusive, community-focused, hopeful"
            }
        ]
    
    creative_ideas["next_steps"] = [
        "Select one campaign idea for visual concept development",
        "Develop detailed creative brief and messaging framework",
        "Create visual concept guidelines and style direction",
        "Plan content calendar and production timeline"
    ]
    
    return creative_ideas

# Create FunctionTool wrapper for the grok_creative_assistant
grok_creative_assistant_tool = FunctionTool(func=grok_creative_assistant) 