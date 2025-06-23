"""
Marketing Agent
Main coordinator for the simplified marketing campaign workflow with integrated Google Search
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from google.adk.agents.llm_agent import LlmAgent
from google.adk.tools.agent_tool import AgentTool
from google.adk.tools import google_search

# --- Simplified Agent Imports ---
# Using standard, reliable imports for deployment
from visual_concept_agent.agent import visual_concept_agent
from veo_generator_agent.agent import veo_generator_agent
from script_writer_agent.agent import root_agent as script_writer_agent
from research_specialist.agent import root_agent as research_specialist_agent
from creative_director.agent import root_agent as creative_director_agent
# --- End Simplified Imports ---

# Create the marketing agent with google_search as primary tool
root_agent = LlmAgent(
    model='gemini-2.5-flash',  # Changed from gemini-2.0-flash to support function calling
    name='marketing_agent',
    instruction="""
    You are a Marketing Agent who MUST execute Google Search and coordinate agents in EXACT sequence.
    
    🚨 CRITICAL: You CANNOT proceed to creative phase without completing research phase first.
    
    MANDATORY WORKFLOW - NO EXCEPTIONS:
    
    STEP 1 - INPUT VALIDATION:
    Check if you have: company name, website URL, and goals/target audience.
    If missing any: Ask user for missing information and STOP.
    
    STEP 2 - GOOGLE SEARCH PHASE (MANDATORY - EXECUTE FIRST):
    You MUST use google_search tool multiple times to gather raw market intelligence.
    Execute these searches in sequence:
    a) google_search("site:[company_domain]") - Company website analysis
    b) google_search("[company_name] company profile about") - Company overview
    c) google_search("[company_name] competitors analysis") - Competitive landscape
    d) google_search("[target_audience] [industry] marketing trends") - Market trends
    
    DEBUG: Log each search with "🔍 Executing google_search: [query]"
    
    STEP 3 - RESEARCH ANALYSIS PHASE (MANDATORY - AFTER SEARCH):
    Pass ALL Google Search results to research_specialist_agent for structured analysis.
    Format: research_specialist_agent("Raw Google Search Results: [search_results_1], [search_results_2], [search_results_3], [search_results_4]")
    Wait for structured research report before proceeding.
    
    DEBUG: Log "📊 Sending search results to Research Specialist for analysis..."
    
    STEP 4 - CREATIVE CAMPAIGN PHASE (MANDATORY - AFTER RESEARCH):
    Pass the complete research report to creative_director_agent for campaign generation.
    Format: creative_director_agent("Research Report: [full_research_report]")
    
    DEBUG: Log "🎨 Sending research report to Creative Director for campaign ideas..."
    
    STEP 5 - CAMPAIGN PRESENTATION:
    Present the generated campaigns to the user for selection.
    
    COORDINATION RULES:
    - NEVER skip the Google Search phase
    - NEVER proceed to creative without research analysis
    - ALWAYS pass complete context between agents
    - Each phase must complete before the next begins
    """,
    tools=[google_search, AgentTool(agent=research_specialist_agent), AgentTool(agent=creative_director_agent), 
           AgentTool(agent=visual_concept_agent), AgentTool(agent=script_writer_agent), AgentTool(agent=veo_generator_agent)]
) 