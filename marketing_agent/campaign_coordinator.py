"""
Campaign Coordinator Agent
Implements ADK Sequential Pipeline Pattern for the marketing campaign workflow:
Marketing Agent (Search) → Research Agent (Analysis) → Creative Agent (Grok)
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from google.adk.agents.llm_agent import LlmAgent
from google.adk.agents.sequential_agent import SequentialAgent
from google.adk.tools.agent_tool import AgentTool

# Import specialized agents
from marketing_agent.agent import root_agent as marketing_search_agent
from research_specialist.agent import root_agent as research_analysis_agent  
from creative_director.agent import root_agent as creative_campaign_agent

# Create AgentTools for sub-agents (proper ADK pattern)
marketing_tool = AgentTool(agent=marketing_search_agent)
research_tool = AgentTool(agent=research_analysis_agent)
creative_tool = AgentTool(agent=creative_campaign_agent)

# Coordinator agent that orchestrates the workflow
coordinator_agent = LlmAgent(
    model='gemini-2.5-flash',
    name='campaign_coordinator',
    instruction="""
    You are the Campaign Coordinator that orchestrates a 3-stage marketing campaign development workflow.
    
    Your workflow follows this EXACT sequence:
    1. **Marketing Intelligence** - Delegate to marketing search agent
    2. **Research Analysis** - Delegate to research analysis agent 
    3. **Creative Development** - Delegate to creative campaign agent
    
    WORKFLOW PROCESS:
    
    STAGE 1 - MARKETING INTELLIGENCE:
    - Use the marketing_search_agent to gather comprehensive market data
    - Ensure all Google searches are completed and data is collected
    - Pass raw search results to next stage
    
    STAGE 2 - RESEARCH ANALYSIS:  
    - Use the research_analysis_agent to process the raw search data
    - Extract insights, opportunities, and strategic recommendations
    - Create structured intelligence report for creative development
    
    STAGE 3 - CREATIVE DEVELOPMENT:
    - Use the creative_campaign_agent with the research intelligence
    - Generate 2 distinct campaign concepts using Grok API
    - Ensure campaigns are research-backed and strategically sound
    
    COORDINATION RULES:
    - ALWAYS follow the sequence: Marketing → Research → Creative
    - Pass data between stages using session state
    - Ensure each stage completes before moving to next
    - Provide final consolidated results with all stages included
    
    FINAL OUTPUT FORMAT:
    Return a complete campaign package containing:
    - Market intelligence summary
    - Research analysis insights  
    - 2 creative campaign concepts
    - Implementation recommendations
    """,
    tools=[marketing_tool, research_tool, creative_tool]
)

# Sequential Pipeline Agent (ADK best practice)
campaign_pipeline = SequentialAgent(
    name='campaign_development_pipeline',
    sub_agents=[
        marketing_search_agent,    # Stage 1: Google Search & Data Collection
        research_analysis_agent,   # Stage 2: Data Analysis & Insights  
        creative_campaign_agent    # Stage 3: Campaign Generation
    ]
)

# Export the coordinator for use in FastAPI service
root_agent = coordinator_agent 