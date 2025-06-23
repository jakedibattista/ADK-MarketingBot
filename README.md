# ADK Marketing Platform

🚀 **AI-powered multi-agent marketing platform using Google ADK (Agent Development Kit)**

Generate complete marketing campaigns with AI agents that research companies, create campaigns, design visuals, write video scripts, and produce marketing videos.

## How It Works

**User Journey: Company Name → Complete Marketing Campaign**
```
1. User enters company name, website, and target audience
2. Marketing Agent (Gemini 2.5 Flash) performs multiple Google Search queries
3. Research Specialist analyzes search results into structured intelligence report
4. Creative Director generates campaign ideas using research + Grok API
5. Visual Concept Agent creates marketing images for selected campaign
6. Script Writer Agent crafts professional video scripts
7. Veo Generator Agent produces marketing videos
8. User receives complete campaign package with visuals and videos
```

## Architecture Overview

```
Firebase Frontend ──────► Cloud Run Service ──────► ADK Multi-Agent System
     ↓                         ↓                           ↓
 Authentication           FastAPI Service              - Marketing Coordinator (Gemini 2.5 Flash + Google Search)
 User Interface           Agent Orchestration          - Research Analyst (Gemini 1.5 Flash - Intelligence) 
 Campaign Forms           /query endpoint              - Creative Director (Gemini 1.5 Flash + Grok API)
                                                      - Script Writer Agent (Professional Scripts)
                                                      - Veo Generator Agent (Video Production)
                                                      - Visual Concept Agent (Marketing Images)
```

## 🚨 Critical Model Compatibility

**IMPORTANT: Gemini 2.0 Flash does NOT support function calling in ADK**

- ✅ **Gemini 2.5 Flash**: Full function calling support (Marketing Agent)
- ✅ **Gemini 1.5 Flash**: Full function calling support (Sub-agents)
- ❌ **Gemini 2.0 Flash**: NO function calling support (causes 400 errors)

**Error Fixed:**
```
400 INVALID_ARGUMENT: Tool use with function calling is unsupported
```

**Solution:** Marketing Agent now uses Gemini 2.5 Flash for Google Search + agent coordination.

## Agent Workflow

### **Sequential 3-Agent System:**
1. **Marketing Agent** (Root Coordinator)
   - **Model**: Gemini 2.5 Flash (required for tools)
   - **Tools**: Google Search + 5 sub-agents
   - **Role**: Execute market research, coordinate workflow

2. **Research Specialist** (Intelligence Analyst)
   - **Model**: Gemini 1.5 Flash (cost-optimized)
   - **Role**: Transform raw search data into structured marketing intelligence

3. **Creative Director** (Campaign Generator)
   - **Model**: Gemini 1.5 Flash + Grok API
   - **Role**: Generate innovative campaigns based on research insights

### **Expected Workflow Execution:**
```
Marketing Agent: 🔍 Executing google_search: site:tesla.com
Marketing Agent: 🔍 Executing google_search: Tesla company profile about
Marketing Agent: 🔍 Executing google_search: Tesla competitors analysis
Marketing Agent: 📊 Sending search results to Research Specialist for analysis...
Research Specialist: 📊 RESEARCH ANALYST ACTIVATED - Processing search results...
Research Specialist: 📋 MARKETING INTELLIGENCE REPORT COMPLETE
Marketing Agent: 🎨 Sending research report to Creative Director for campaign ideas...
Creative Director: 🔍 DEBUG: Starting Grok API call...
Creative Director: 📡 Grok API response status: 200
Marketing Agent: ✅ Campaign ideas generated successfully!
```

## Quick Start

### 1. **Prerequisites**
```bash
# Required services:
- Google Cloud Project with Vertex AI enabled
- Firebase project for frontend hosting
- Docker for containerization
- ADK (Agent Development Kit) access
```

### 2. **Environment Setup**
```bash
# Create .env file with required credentials
GOOGLE_API_KEY=your_google_api_key          # For Veo 2.0 and Imagen
GROK_API_KEY=your_grok_api_key              # For Creative Director
PROJECT_ID=adkchl                           # Google Cloud project
```

### 3. **Agent Architecture**
The system uses a **3-agent workflow** optimized for ADK limitations:

```python
# Marketing Agent (Root) - Gemini 2.0 with Google Search
marketing_agent = LlmAgent(
    model='gemini-2.0-flash',
    tools=[google_search, AgentTool(agent=research_specialist_agent), ...]
)

# Research Specialist (Analyst) - Gemini 1.5 for analysis
research_specialist = LlmAgent(
    model='gemini-1.5-flash',
    tools=[]  # Pure analysis agent
)

# Creative Director (Campaigns) - Gemini 1.5 with Grok API
creative_director = LlmAgent(
    model='gemini-1.5-flash',
    tools=[FunctionTool(func=grok_creative_assistant)]
)
```

### 4. **Deployment**
```bash
# Build and deploy to Cloud Run
gcloud builds submit --config=cloudbuild.yaml .

# Deploy frontend to Firebase
cd frontend && firebase deploy --only hosting
```

## Technical Implementation

### **ADK Integration**
The system leverages Google's Agent Development Kit for:
- **Built-in Google Search**: Market intelligence gathering
- **Agent Coordination**: Structured multi-agent workflows
- **Session Management**: Conversation state and context
- **Tool Integration**: Seamless API connections

### **Key ADK Compliance**
- ✅ **Google Search in Root Agent**: Only Marketing Agent uses `google_search`
- ✅ **Gemini 2.0 for Search**: Required model for built-in tools
- ✅ **Sub-agent Coordination**: Research and Creative as specialized analysts
- ✅ **Single Built-in Tool**: No tool conflicts in agent definitions

### **Workflow Optimization**
```
User Input → Marketing Agent (Search) → Research Specialist (Analysis) → 
Creative Director (Grok + Research) → Visual/Video Generation → Complete Campaign
```

## API Endpoints

### **Primary Endpoint**
```
POST /query
{
  "query": "Company: Tesla, Website: https://tesla.com, Goals: Target men in California"
}
```

**Response**: Complete marketing campaign with research-backed ideas

### **Specialized Endpoints**
- `POST /generate-visual` - Instagram content generation
- `POST /generate-script` - Veo 2.0 script creation  
- `POST /generate-video-direct` - Video generation

## Performance Metrics

### **System Performance**
- **Campaign Generation**: 30-60 seconds end-to-end
- **Google Search**: 6 queries executed per campaign
- **Research Analysis**: Structured intelligence reports
- **Video Generation**: 20-40 seconds with Veo 2.0

### **Quality Improvements**
- ✅ **Research-Backed Campaigns**: All ideas grounded in market data
- ✅ **Structured Intelligence**: Organized competitive analysis
- ✅ **Cost Optimization**: Efficient model usage (2.0 for search, 1.5 for analysis)
- ✅ **ADK Compliance**: No architectural limitations

## Success Stories

The enhanced 3-agent system delivers:
- **Higher Quality Campaigns**: Research-driven creative concepts
- **Better Market Fit**: Real competitive intelligence integration
- **Faster Execution**: Optimized agent coordination
- **Cost Efficiency**: Strategic model selection for each task

Ready to generate research-backed marketing campaigns that convert! 🚀

## Project Structure

```
ADk hackathon/
├── Dockerfile                     # Cloud Run container configuration
├── service/
│   └── main.py                   # FastAPI service with ADK integration
├── marketing_agent/
│   └── agent.py                  # Root marketing coordinator (ADK LlmAgent)
├── research_specialist/
│   └── agent.py                  # Company analysis agent (ADK + Google Search)
├── creative_director/
│   ├── agent.py                  # Creative strategy agent (ADK + Grok API)
│   └── tools.py                  # Grok API integration
├── visual_concept_agent/
│   ├── agent.py                  # ADK agent wrapper for image generation
│   ├── simple_generator.py       # Basic image generation (Imagen 3.0)
│   └── instagram_specialist.py   # Instagram content creation (Gemini + Imagen)
├── script_writer_agent/
│   ├── agent.py                  # Cinematic script creation agent (ADK)
│   └── tools.py                  # Veo 2.0 script optimization tools
├── veo_generator_agent/
│   ├── agent.py                  # Video generation coordinator (ADK)
│   └── simple_veo_generator.py   # Direct Veo 2.0 API integration
├── frontend/                     # Firebase-hosted frontend
│   ├── index.html               # Main application interface
│   ├── script.js                # API calls to Cloud Run service
│   ├── auth.js                  # Firebase authentication
│   └── firebase-config.js       # Firebase configuration
└── cloudbuild.yaml              # CI/CD pipeline configuration
```

## Technology Stack

### **Frontend**
- **Framework**: Vanilla JavaScript with Firebase SDK
- **Authentication**: Firebase Auth with Google Sign-In
- **Hosting**: Firebase Hosting
- **API Calls**: Direct calls to Cloud Run service endpoints

### **Backend (Cloud Run Service)**
- **Framework**: FastAPI with ADK integration
- **Agents**: Google ADK (Agent Development Kit)
- **AI Models**: Gemini 1.5 Flash, Veo 2.0, Imagen 3
- **Platform**: Google Cloud Run (Managed)
- **Storage**: Google Cloud Storage for generated assets

### **ADK Agent System**
- **Runner**: `google.adk.runners.Runner` for agent execution
- **Sessions**: `google.adk.sessions.InMemorySessionService`
- **Tools**: `google.adk.tools` (google_search, FunctionTool, AgentTool)
- **Agents**: `google.adk.agents.llm_agent.LlmAgent`

## Deployment

### **Automated CI/CD (Cloud Build)**
```yaml
# cloudbuild.yaml
steps:
  - name: 'gcr.io/cloud-builders/docker'
    args: ['build', '-t', 'gcr.io/$PROJECT_ID/adk-marketing-platform', '.']
  - name: 'gcr.io/cloud-builders/docker'
    args: ['push', 'gcr.io/$PROJECT_ID/adk-marketing-platform']
  - name: 'gcr.io/cloud-builders/gcloud'
    args: ['run', 'deploy', 'adk-marketing-platform', 
           '--image', 'gcr.io/$PROJECT_ID/adk-marketing-platform',
           '--region', 'us-central1', '--platform', 'managed']
```

### **Manual Deployment**
```bash
# Build and push container
docker build -t gcr.io/adkchl/adk-marketing-platform .
docker push gcr.io/adkchl/adk-marketing-platform

# Deploy to Cloud Run
gcloud run deploy adk-marketing-platform \
  --image gcr.io/adkchl/adk-marketing-platform \
  --region us-central1 \
  --allow-unauthenticated

# Deploy frontend
cd frontend && firebase deploy --only hosting
```

## Monitoring & Debugging

### **Cloud Run Logs**
```bash
# View service logs
gcloud logs read --service=adk-marketing-platform --limit=50
```

### **Frontend Debugging**
- Use browser developer tools for API call inspection
- Check Firebase Authentication status
- Monitor Cloud Run service responses

## Security

### **Authentication**
- Firebase Authentication with Google Sign-In
- Cloud Run service authentication via Firebase ID tokens
- API keys managed through environment variables

### **API Security**
- CORS configured for Firebase frontend domain
- Request validation in FastAPI endpoints
- Error handling without sensitive data exposure

## Cost Optimization

### **Cloud Run**
- Scales to zero when not in use
- Pay-per-request pricing model
- Efficient container resource allocation

### **AI Model Usage**
- Gemini 1.5 Flash for cost-effective agent processing
- Veo 2.0 for high-quality video generation
- Imagen 3 for marketing image creation

## Contributing

1. **Fork the repository**
2. **Create feature branch** (`git checkout -b feature/amazing-feature`)
3. **Test locally** with Docker and ADK
4. **Commit changes** (`git commit -m 'Add amazing feature'`)
5. **Push to branch** (`git push origin feature/amazing-feature`)
6. **Open Pull Request**

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Support

For questions about ADK (Agent Development Kit), refer to Google's ADK documentation.
For project-specific issues, please open a GitHub issue. 