# ADK Marketing Platform - Development Rules

## 🏗️ **Architecture Overview**

**Current Architecture: Firebase Frontend → Cloud Run Service → ADK Multi-Agent System**
```
Firebase Frontend ──────► Cloud Run Service ──────► ADK Multi-Agent System
     ↓                         ↓                           ↓
 Authentication           FastAPI Service              - Marketing Coordinator
 User Interface           Agent Orchestration          - Research Specialist  
 Campaign Forms           /query endpoint              - Creative Director
                                                      - Script Writer Agent
                                                      - Veo Generator Agent
                                                      - Visual Concept Agent
```

**Key Principles:**
- ✅ **ADK-Powered Agents** - All agents built with Google's Agent Development Kit
- ✅ **Cloud Run Deployment** - Scalable containerized FastAPI service
- ✅ **Agent Coordination** - Marketing Agent orchestrates specialist agents
- ✅ **Veo 2.0 Integration** - Video generation using Veo 2.0 model
- ✅ **Real API Integrations** - Google Search, Grok API, Imagen, Veo

## 🛠️ **Technology Stack**

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
- **Tools**: `google.adk.tools` (google_search, FunctionTool)
- **Agents**: `google.adk.agents.llm_agent.LlmAgent`

## 🔧 **Development Guidelines**

### **1. ADK Agent Development**

#### **Agent Structure**
```python
from google.adk.agents.llm_agent import LlmAgent
from google.adk.tools.agent_tool import AgentTool

# Create ADK agent
root_agent = LlmAgent(
    model='gemini-1.5-flash',
    name='agent_name',
    instruction="""
    Clear, specific instructions for agent behavior.
    Define role, responsibilities, and coordination patterns.
    """,
    tools=[AgentTool(agent=other_agent), ...]
)
```

#### **Agent Coordination**
```python
# Marketing Agent coordinates other agents
from marketing_agent.agent import root_agent as marketing_agent
from research_specialist.agent import root_agent as research_specialist_agent
from creative_director.agent import root_agent as creative_director_agent

# Tools for agent coordination
tools=[
    AgentTool(agent=research_specialist_agent),
    AgentTool(agent=creative_director_agent),
    AgentTool(agent=visual_concept_agent),
    AgentTool(agent=script_writer_agent),
    AgentTool(agent=veo_generator_agent)
]
```

### **2. FastAPI Service Integration**

#### **Service Architecture**
```python
from fastapi import FastAPI
from google.adk.runners import Runner
from google.adk.sessions import InMemorySessionService
from marketing_agent.agent import root_agent

app = FastAPI()

# Create ADK runner
session_service = InMemorySessionService()
runner = Runner(agent=root_agent, app_name="adk_marketing_platform", session_service=session_service)

@app.post("/query")
async def query_agent(request: QueryRequest):
    # Create session
    session = await session_service.create_session(...)
    
    # Run agent via ADK Runner
    async for event in runner.run_async(
        user_id=USER_ID,
        session_id=session_id,
        new_message=user_content
    ):
        # Process agent events
```

#### **API Design Patterns**
- **Main Endpoint**: `/query` for agent orchestration
- **Direct Endpoints**: `/generate-visual`, `/generate-video-direct` for specific functions
- **Health Check**: `/` for service status
- **Request Models**: Pydantic models for validation

### **3. Tool Integration**

#### **Google Search (Built-in ADK Tool)**
```python
from google.adk.tools import google_search

# Research Specialist uses built-in Google Search
root_agent = LlmAgent(
    name='research_specialist',
    tools=[google_search]
)
```

#### **Custom API Tools (Grok, Veo)**
```python
from google.adk.tools import FunctionTool

# Create custom tool for external APIs
def grok_creative_assistant(query: str) -> str:
    # Grok API integration
    return response

grok_tool = FunctionTool(func=grok_creative_assistant)

# Creative Director uses Grok API
root_agent = LlmAgent(
    name='creative_director',
    tools=[grok_tool]
)
```

### **4. Veo 2.0 Video Generation**

#### **Implementation Pattern**
```python
from google import genai

def generate_veo_video_simple(script: str) -> Dict[str, Any]:
    client = genai.Client(api_key=GOOGLE_API_KEY)
    
    operation = client.models.generate_videos(
        model="veo-2.0-generate-001",  # Use Veo 2.0, not 3.0
        prompt=script,
        config=types.GenerateVideosConfig(
            person_generation="allow_adult",
            aspect_ratio="16:9"
        )
    )
    
    # Wait for completion and return results
```

#### **Video Specifications**
- **Model**: `veo-2.0-generate-001`
- **Duration**: ~5 seconds
- **Aspect Ratio**: 16:9 (only supported ratio)
- **Processing Time**: ~60 seconds average

## 📁 **File Organization**

### **ADK Agent Structure**
```
ADk hackathon/
├── Dockerfile                     # Cloud Run container
├── service/
│   └── main.py                   # FastAPI + ADK integration
├── marketing_agent/
│   └── agent.py                  # Root coordinator (LlmAgent)
├── research_specialist/
│   └── agent.py                  # Google Search agent
├── creative_director/
│   ├── agent.py                  # Grok API agent
│   └── tools.py                  # Grok integration
├── visual_concept_agent/
│   └── agent.py                  # Image generation
├── script_writer_agent/
│   └── agent.py                  # Veo script creation
├── veo_generator_agent/
│   ├── agent.py                  # Video coordination
│   └── simple_veo_generator.py   # Veo 2.0 integration
└── frontend/                     # Firebase frontend
```

### **Required Dependencies**
```python
# requirements.txt
fastapi
uvicorn
google-adk
google-genai
google-cloud-storage
pydantic
requests
```

## 🚀 **Deployment Process**

### **Container Configuration**
```dockerfile
FROM python:3.11-slim

WORKDIR /app

# Install ADK and dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy agent modules
COPY marketing_agent/ ./marketing_agent/
COPY research_specialist/ ./research_specialist/
COPY creative_director/ ./creative_director/
COPY visual_concept_agent/ ./visual_concept_agent/
COPY script_writer_agent/ ./script_writer_agent/
COPY veo_generator_agent/ ./veo_generator_agent/
COPY service/ ./service/

# Run FastAPI service
CMD ["uvicorn", "service.main:app", "--host", "0.0.0.0", "--port", "8080"]
```

### **Cloud Build Pipeline**
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

## 🔍 **Code Quality Standards**

### **ADK Agent Patterns**
```python
# ✅ GOOD: Proper ADK agent structure
from google.adk.agents.llm_agent import LlmAgent
from google.adk.tools.agent_tool import AgentTool

root_agent = LlmAgent(
    model='gemini-1.5-flash',
    name='descriptive_name',
    instruction="Clear, specific role definition",
    tools=[AgentTool(agent=specialist_agent)]
)

# ❌ BAD: Generic function without ADK structure
async def generic_function(query: str):
    return "placeholder response"
```

### **Tool Integration Standards**
```python
# ✅ GOOD: Use ADK built-in tools
from google.adk.tools import google_search

# ✅ GOOD: Create proper FunctionTool for external APIs
from google.adk.tools import FunctionTool

def external_api_call(query: str) -> str:
    # Proper API integration with error handling
    return response

tool = FunctionTool(func=external_api_call)

# ❌ BAD: Direct API calls without ADK integration
requests.post(url, data=query)
```

### **Error Handling**
```python
# ✅ GOOD: Comprehensive error handling
try:
    result = await runner.run_async(...)
    return process_result(result)
except Exception as e:
    logger.error(f"Agent execution failed: {e}")
    raise HTTPException(status_code=500, detail=str(e))

# ❌ BAD: No error handling
result = await runner.run_async(...)
return result
```

## 🧪 **Testing Requirements**

### **Agent Testing**
```python
# Test individual agents
from marketing_agent.agent import root_agent
from google.adk.runners import Runner

def test_marketing_agent():
    runner = Runner(agent=root_agent, ...)
    # Test agent responses
```

### **Integration Testing**
```bash
# Test complete workflows
python test_veo_workflow.py
python test_instagram_workflow.py
python test_simplified_workflow.py
```

### **Service Testing**
```bash
# Test FastAPI service locally
uvicorn service.main:app --reload --port 8000

# Test container
docker build -t adk-marketing-service .
docker run -p 8080:8080 adk-marketing-service
```

## 🔐 **Security Requirements**

### **Environment Variables**
```bash
# Required for service operation
GOOGLE_API_KEY=your_google_api_key    # Veo 2.0 and Imagen
GROK_API_KEY=your_grok_api_key        # Creative Director
PROJECT_ID=adkchl                     # Google Cloud project
```

### **Authentication Flow**
1. Frontend: Firebase Auth with Google Sign-In
2. API Calls: Firebase ID token in Authorization header
3. Backend: Verify Firebase token before processing
4. ADK: Use authenticated context for agent execution

### **API Security**
- CORS configured for Firebase frontend domain
- Request validation with Pydantic models
- Error responses without sensitive data exposure
- Environment variables for all credentials

## 📊 **Monitoring & Debugging**

### **Cloud Run Logs**
```bash
# View service logs
gcloud logs read --service=adk-marketing-platform --limit=50

# Follow real-time logs
gcloud logs tail --service=adk-marketing-platform
```

### **Agent Debugging**
```python
# Add debug logging in agents
import logging
logger = logging.getLogger(__name__)

# Log agent interactions
logger.info(f"Agent {agent_name} received: {query}")
logger.info(f"Agent {agent_name} responding: {response}")
```

### **Performance Monitoring**
- Monitor Cloud Run metrics (latency, memory, CPU)
- Track agent response times
- Monitor Veo 2.0 generation success rates
- Watch for API rate limits (Grok, Google APIs)

## 🎯 **Best Practices**

### **Agent Design**
- **Single Responsibility**: Each agent has one clear purpose
- **Clear Instructions**: Detailed, specific agent instructions
- **Tool Integration**: Use appropriate ADK tools for each task
- **Error Resilience**: Handle failures gracefully

### **Service Architecture**
- **Stateless Design**: Use ADK sessions for state management
- **Async Processing**: Use async/await for all I/O operations
- **Resource Efficiency**: Optimize for Cloud Run scaling
- **Monitoring**: Comprehensive logging and error tracking

### **Development Workflow**
1. **Local Testing**: Test agents individually with ADK Runner
2. **Container Testing**: Verify complete service in Docker
3. **Staging Deployment**: Test in Cloud Run staging environment
4. **Production Deployment**: Use Cloud Build for automated deployment
5. **Monitoring**: Watch logs and metrics after deployment
