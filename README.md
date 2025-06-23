# ADK Marketing Platform

🚀 **AI-powered multi-agent marketing platform using Google ADK (Agent Development Kit)**

Generate complete marketing campaigns with AI agents that research companies, create campaigns, design visuals, write video scripts, and produce marketing videos.

## How It Works

**User Journey: Company Name → Complete Marketing Campaign**
```
1. User enters company name
2. Research Specialist analyzes company
3. Creative Director generates campaign ideas  
4. Visual Concept Agent creates marketing images
5. Script Writer Agent crafts video scripts
6. Veo Generator Agent produces marketing videos
7. User receives complete campaign package
```

## Architecture Overview

```
Firebase Frontend ──────► Cloud Run Service ──────► ADK Multi-Agent System
     ↓                         ↓                           ↓
 Authentication           FastAPI Service              - Marketing Coordinator
 User Interface           Agent Orchestration          - Research Specialist  
 Campaign Forms           /query endpoint              - Creative Director
                                                      - Visual Concept Agent
                                                      - Script Writer Agent
                                                      - Veo Generator Agent
```

## The Agent Workflow (Sequential)

### 1. 🔍 **Research Specialist Agent**
**Purpose**: Company and market intelligence gathering
**Technology**: ADK + Built-in Google Search tool
**Process**:
- Takes company name from user
- Uses Google Search to find company information
- Analyzes business model, target audience, competitors
- Provides comprehensive company profile

```python
from google.adk.tools import google_search

root_agent = LlmAgent(
    name='research_specialist',
    instruction="Research companies using Google Search...",
    tools=[google_search]  # Built-in ADK tool
)
```

### 2. 🎨 **Creative Director Agent** 
**Purpose**: Campaign ideation and creative strategy
**Technology**: ADK + Grok API integration
**Process**:
- Takes company research from Research Specialist
- Uses Grok API for innovative, out-of-the-box thinking
- Generates multiple campaign concepts (A, B, C options)
- Provides creative briefs with target audience and messaging

```python
from google.adk.tools import FunctionTool

def grok_creative_assistant(query: str) -> str:
    """Grok API integration for creative campaign generation"""
    headers = {"Authorization": f"Bearer {GROK_API_KEY}"}
    response = requests.post(GROK_API_URL, headers=headers, json={
        "messages": [{"role": "user", "content": query}],
        "model": "grok-beta"
    })
    return response.json()["choices"][0]["message"]["content"]

root_agent = LlmAgent(
    name='creative_director',
    instruction="Generate innovative marketing campaigns using Grok...",
    tools=[FunctionTool(func=grok_creative_assistant)]
)
```

### 3. 📸 **Visual Concept Agent**
**Purpose**: Marketing image generation and Instagram content
**Technology**: Multi-layered system with Imagen 3.0 + Gemini
**Architecture**:
```
visual_concept_agent/
├── agent.py                  # ADK agent coordinator
├── simple_generator.py       # Basic image generation
└── instagram_specialist.py   # Social media content creation
```

**Process**:
1. **Simple Generator**: Creates marketing images from text descriptions
2. **Instagram Specialist**: Generates complete Instagram posts (captions + visuals)
3. **ADK Agent**: Coordinates visual generation within the agent system

```python
# Instagram Specialist Process
def generate_instagram_content(campaign_content: str, concept_number: int):
    # 1. Generate Instagram caption with emojis/hashtags using Gemini
    # 2. Create visual description for image generation
    # 3. Call simple_generator.py to create actual image
    # 4. Return complete Instagram post package
```

### 4. ✍️ **Script Writer Agent**
**Purpose**: Cinematic video script creation for Veo 2.0
**Technology**: ADK + Veo 2.0 optimization tools
**Process**:
- Takes approved campaign and visual concept
- Creates detailed cinematic scripts optimized for Veo 2.0
- Includes camera angles, lighting, timing, brand integration
- Outputs ~5-second video scripts with rich descriptions

```python
# Script Writer Output Example
script = """
[OPENING SHOT]: Wide establishing shot of modern office space with natural lighting.
[CAMERA MOVEMENT]: Smooth dolly-in to medium shot of professional using tablet.
[CLOSE-UP]: Detail shot of tablet screen showing intuitive interface.
[LIGHTING]: Golden hour warmth with soft shadows.
[BRAND INTEGRATION]: Natural logo placement as user interacts.
[FINAL MOMENT]: Confident user walking away, camera pulls back.
Duration: ~5 seconds. Aspect ratio: 16:9.
"""
```

### 5. 🎬 **Veo Generator Agent**
**Purpose**: AI video generation from scripts
**Technology**: ADK + Veo 2.0 direct API integration
**Process**:
1. Takes detailed script from Script Writer Agent
2. Enhances script to avoid text overlays (prevents spelling errors)
3. Calls Veo 2.0 API via `simple_veo_generator.py`
4. Returns video URL with generation details

```python
# Veo 2.0 Implementation
from google import genai

def generate_veo_video_simple(script: str):
    client = genai.Client(api_key=GOOGLE_API_KEY)
    
    operation = client.models.generate_videos(
        model="veo-2.0-generate-001",
        prompt=script,
        config=types.GenerateVideosConfig(
            person_generation="allow_adult",
            aspect_ratio="16:9"
        )
    )
    # Wait for completion and return video URL
```

**Video Specifications**:
- **Model**: Veo 2.0 (`veo-2.0-generate-001`)
- **Duration**: ~5 seconds per video
- **Aspect Ratio**: 16:9 (only supported ratio)
- **Processing Time**: ~60 seconds average
- **Quality**: High-definition marketing videos

### 6. 🎯 **Marketing Agent (Coordinator)**
**Purpose**: Orchestrates the entire workflow
**Technology**: ADK LlmAgent with AgentTool coordination
**Process**:
- Receives user query with company name
- Coordinates all specialist agents in sequence
- Manages context and handoffs between agents
- Delivers final campaign package to user

```python
from google.adk.tools.agent_tool import AgentTool

root_agent = LlmAgent(
    name='marketing_agent',
    instruction="Coordinate marketing campaign generation...",
    tools=[
        AgentTool(agent=research_specialist_agent),
        AgentTool(agent=creative_director_agent),
        AgentTool(agent=visual_concept_agent),
        AgentTool(agent=script_writer_agent),
        AgentTool(agent=veo_generator_agent)
    ]
)
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

### 3. **Deploy Service**
```bash
# Build and deploy to Cloud Run
docker build -t adk-marketing-service .
docker tag adk-marketing-service gcr.io/adkchl/adk-marketing-platform:latest
docker push gcr.io/adkchl/adk-marketing-platform:latest

# Deploy to Cloud Run
gcloud run deploy adk-marketing-platform \
  --image gcr.io/adkchl/adk-marketing-platform:latest \
  --platform managed \
  --region us-central1 \
  --allow-unauthenticated
```

### 4. **Deploy Frontend**
```bash
cd frontend
firebase deploy --only hosting
```

### 5. **Access the Platform**
- **Frontend**: https://adkchl.web.app
- **API Service**: Your Cloud Run service URL
- **Authentication**: Firebase Google Sign-In

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

## API Endpoints

### **Cloud Run Service**
```
POST   /query                    # Main agent query endpoint
POST   /generate-visual          # Direct visual concept generation
POST   /generate-video-direct    # Direct video generation
GET    /                         # Health check
```

### **Frontend Integration**
```javascript
// Call Cloud Run service from frontend
const response = await fetch(`${SERVICE_URL}/query`, {
    method: 'POST',
    headers: {
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${idToken}`
    },
    body: JSON.stringify({ query: userInput })
});
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