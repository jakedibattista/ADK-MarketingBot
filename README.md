# ADK Marketing Platform

🚀 **AI-powered multi-agent marketing platform using Google ADK (Agent Development Kit)**

**COMPLETED PLATFORM** - Generate complete marketing campaigns with AI agents that research companies, create campaigns, design visuals, write video scripts, and produce marketing videos using Veo 2.0.

[*Repository updated by @jakedibattista - June 2025 as Cursor was confuigured to old account see architect diagram here*](https://lucid.app/lucidchart/ca9bc6d8-b971-41be-b6ea-280c99c5522d/edit?viewport_loc=-248%2C70%2C4488%2C2243%2C0_0&invitationId=inv_6db227c8-a569-4bb8-9656-cca22aae922f)

## 🎯 Platform Status: FULLY OPERATIONAL at https://adkchl.web.app/

### ✅ **Completed Features**
- **Campaign Generation**: 2 AI-generated marketing campaigns per request ✅
- **Image Generation**: AI-created Instagram-style visuals with captions ✅
- **Script Writing**: Professional cinematic scripts optimized for video ✅
- **Video Production**: Veo 2.0 generated marketing videos (5-second duration) ✅
- **Complete UI Flow**: Seamless user experience from input to final video ✅
- **Download Capability**: Users can download generated videos ✅
- **Error Handling**: Robust error handling and user feedback ✅

### ✅ **Technical Implementation**
- **Frontend**: Vanilla JavaScript with Firebase Auth
- **Backend**: FastAPI service with specialized endpoints
- **AI Integration**: Google ADK, Gemini models, Grok API, Veo 2.0
- **Image Generation**: Google Imagen 3.0 
- **Authentication**: Firebase Google Sign-In
- **Deployment**: Cloud Run + Firebase Hosting

## Architecture Overview

```
Firebase Frontend ──────► Cloud Run Service ──────► Multi-Agent System
     ↓                         ↓                           ↓
 Authentication           FastAPI Service              - Research Agent (Google Search)
 User Interface           Campaign Endpoints           - Creative Director (Grok API)  
 Campaign Forms           Visual Generation            - Visual Concept Agent (Imagen)
 Image Display            Script Generation            - Script Writer Agent (ADK)
 Video Player             Video Generation             - Veo 2.0 Generator Agent
```

**Key Principles:**
- ✅ **Complete Workflow**: Full campaign-to-video pipeline
- ✅ **ADK Compliance**: Proper agent architecture with specialized tools
- ✅ **Google Search Integration**: Research Agent uses built-in google_search tool
- ✅ **Grok API Integration**: Creative Director uses Grok for innovative campaigns
- ✅ **Veo 2.0 Integration**: Professional video generation
- ✅ **Modular Design**: Easy to maintain, test, and extend individual agents


**Solution:** Marketing Agent uses Gemini 2.5 Flash for Google Search + agent coordination.

## Agent Workflow

### **Complete 5-Agent System:**
1. **Marketing Agent** (Root Coordinator)
   - **Model**: Gemini 2.5 Flash (required for tools)
   - **Tools**: Google Search + 4 sub-agents
   - **Role**: Execute market research, coordinate workflow

2. **Research Specialist** (Intelligence Analyst)
   - **Model**: Gemini 1.5 Flash (cost-optimized)
   - **Role**: Transform raw search data into structured marketing intelligence

3. **Creative Director** (Campaign Generator)
   - **Model**: Gemini 1.5 Flash + Grok API
   - **Role**: Generate innovative campaigns based on research insights

4. **Visual Concept Agent** (Image Creator)
   - **Model**: Gemini 1.5 Flash + Imagen 3.0
   - **Role**: Create Instagram-style marketing images with captions

5. **Script Writer Agent** (Video Script Creator)
   - **Model**: Gemini 1.5 Flash with ADK tools
   - **Role**: Generate professional cinematic scripts for Veo 2.0

6. **Veo Generator Agent** (Video Producer)
   - **Model**: Veo 2.0
   - **Role**: Produce high-quality marketing videos from scripts

### **Successful Workflow Execution:**
```
Marketing Agent: 🔍 Executing google_search: site:tesla.com
Marketing Agent: 🔍 Executing google_search: Tesla company profile about
Marketing Agent: 📊 Sending search results to Research Specialist...
Research Specialist: 📊 RESEARCH ANALYST ACTIVATED
Creative Director: 🎨 CREATIVE DIRECTOR ACTIVATED - Formatting Grok response
Visual Concept Agent: 🖼️ Generating Instagram-style visual concepts...
Script Writer Agent: 📝 Creating cinematic video script...
Veo Generator: 🎬 Video generation completed in 41s
✅ Complete marketing campaign with video delivered!
```

## Quick Start

### 1. **Prerequisites**
```bash
# Required services:
- Google Cloud Project with Vertex AI enabled
- Firebase project for frontend hosting
- Docker for containerization
- ADK (Agent Development Kit) access
- Grok API access
```

### 2. **Environment Setup**
```bash
# Create .env file with required credentials
GOOGLE_API_KEY=your_google_api_key          # For Veo 2.0 and Imagen
GROK_API_KEY=your_grok_api_key              # For Creative Director
PROJECT_ID=adkchl                           # Google Cloud project
LOCATION=us-central1                        # Google Cloud region
```

### 3. **Complete Agent Architecture**
The system uses a **multi-agent workflow** optimized for full campaign generation:

```python
# Marketing Agent (Root) - Gemini 2.5 with Google Search
marketing_agent = LlmAgent(
    model='gemini-2.5-flash',
    tools=[google_search, research_agent, creative_agent, visual_agent, script_agent]
)

# Visual Concept Agent - Imagen 3.0 for image generation
visual_concept_agent = LlmAgent(
    model='gemini-1.5-flash',
    tools=[imagen_generator]
)

# Script Writer Agent - ADK tools for video scripts
script_writer_agent = LlmAgent(
    model='gemini-1.5-flash', 
    tools=[create_veo_script]
)

# Veo Generator - Video production
veo_generator = VeoAgent(
    model='veo-2.0',
    video_duration='5_seconds'
)
```

### 4. **Deployment**
```bash
# Build and deploy complete platform
gcloud builds submit --config=cloudbuild.yaml .

# Deploy frontend with full UI
cd frontend && firebase deploy --only hosting
```

## 🌐 **Complete API Endpoints**

### **Main Campaign Workflow**

#### **1. Complete Campaign Generation**
```bash
POST /hybrid-campaign
{
  "company": "Tesla",
  "website": "https://tesla.com",
  "goals": "Increase EV adoption",
  "target_audience": "tech-savvy millennials"
}
```
**Response**: Complete workflow with research report and 2 campaign concepts

#### **2. Visual Concept Generation**
```bash
POST /generate-visual
{
  "campaign": "1",
  "campaign_content": "[Selected campaign content]",
  "target_audience": "tech-savvy millennials"
}
```
**Response**: Instagram-style image with caption and visual description

#### **3. Script Generation**
```bash
POST /generate-script
{
  "campaign_content": "[Selected campaign]",
  "visual_concept": "[Selected visual concept]", 
  "company_name": "Tesla"
}
```
**Response**: Professional cinematic video script optimized for Veo 2.0

#### **4. Video Generation**
```bash
POST /generate-video-direct
{
  "script": "[Generated script]",
  "campaign_content": "[Campaign content]",
  "visual_concept": "[Visual concept]"
}
```
**Response**: High-quality marketing video with download URL

### **Legacy Endpoints**

#### **5. Research Only**
```bash
POST /research
{
  "company": "Tesla",
  "website": "https://tesla.com", 
  "goals": "Increase EV adoption",
  "target_audience": "tech-savvy millennials"
}
```

#### **6. Creative Development Only**
```bash
POST /creative
{
  "research_report": "[Complete research intelligence]",
  "company": "Tesla",
  "goals": "Increase EV adoption", 
  "target_audience": "tech-savvy millennials"
}
```

## Technical Implementation

### **Complete ADK Integration**
The system leverages Google's Agent Development Kit for:
- **Built-in Google Search**: Market intelligence gathering
- **Agent Coordination**: Structured multi-agent workflows
- **Session Management**: Conversation state and context
- **Tool Integration**: Seamless API connections
- **Function Calling**: Script generation and video tools

### **Key ADK Compliance**
- ✅ **Google Search in Root Agent**: Only Marketing Agent uses `google_search`
- ✅ **Gemini 2.5 for Search**: Required model for built-in tools
- ✅ **Sub-agent Coordination**: Specialized agents for each task
- ✅ **Single Tool per Agent**: Clean agent architecture
- ✅ **Proper Session Management**: Veo session service integration

### **Complete Workflow Architecture**
```
User Input → Marketing Agent (Search + Research) → Creative Director (Grok + Campaigns) → 
Visual Agent (Imagen + Images) → Script Writer (ADK + Scripts) → 
Veo Generator (Video Production) → Complete Campaign Package
```

## 🎬 **Video Generation Pipeline**

### **Veo 2.0 Integration**
- **Model**: `veo-2.0-generate-001`
- **Duration**: 5-second marketing videos
- **Quality**: High-definition output
- **Format**: MP4 with download capability
- **Processing Time**: ~40-60 seconds per video

### **Script Optimization**
Scripts are optimized for Veo 2.0 with:
- Multiple camera angles and movements
- Rich visual descriptions
- Natural brand integration
- 16:9 aspect ratio composition
- Cinematic lighting and mood
- NO visible text to avoid spelling errors

## 🖼️ **Image Generation Pipeline**

### **Imagen 3.0 Integration**
- **Model**: `imagen-3.0-generate-002`
- **Style**: Instagram-ready marketing visuals
- **Format**: Base64 encoded JPEG
- **Captions**: AI-generated with hashtags
- **Quality**: High-resolution marketing images

## 🔧 **Development Setup**

### **Local Development**
```bash
# Clone repository
git clone [repository-url]
cd "ADk hackathon"

# Install dependencies
pip install -r requirements.txt

# Set up environment variables
cp .env.example .env
# Edit .env with your credentials

# Run local development server
cd service && python main.py

# Run frontend locally
cd frontend && python -m http.server 8000
```

### **Testing the Complete Flow**
1. Open frontend at https://adkchl.web.app/
2. Sign in with Google
3. Enter company information
4. Wait for campaign generation (~30 seconds)
5. Select preferred campaign
6. Wait for image generation (~20 seconds)
7. Select preferred visual concept
8. Wait for script generation (~10 seconds)
9. Wait for video generation (~60 seconds)
10. Download completed marketing video

## 📊 **Performance Metrics**

### **Timing Benchmarks**
- **Campaign Generation**: 20-30 seconds ✅
- **Image Generation**: 15-25 seconds (parallel processing) ✅
- **Script Generation**: 5-15 seconds ✅
- **Video Generation**: 40-60 seconds ✅
- **Total Workflow**: 2-3 minutes end-to-end ✅

## 🚀 **Production Deployment**

### **Cloud Run Configuration**
```yaml
# cloudbuild.yaml
steps:
  - name: 'gcr.io/cloud-builders/docker'
    args: ['build', '-t', 'gcr.io/$PROJECT_ID/adk-marketing:latest', '.']
  - name: 'gcr.io/cloud-builders/docker'
    args: ['push', 'gcr.io/$PROJECT_ID/adk-marketing:latest']
  - name: 'gcr.io/cloud-builders/gcloud'
    args: [
      'run', 'deploy', 'adk-marketing',
      '--image', 'gcr.io/$PROJECT_ID/adk-marketing:latest',
      '--platform', 'managed',
      '--region', 'us-central1',
      '--allow-unauthenticated'
    ]
```

### **Firebase Hosting Configuration**
```json
{
  "hosting": {
    "public": "frontend",
    "ignore": ["firebase.json", "**/.*", "**/node_modules/**"],
    "rewrites": [{
      "source": "**",
      "destination": "/index.html"
    }]
  }
}
```

## 📈 **Future Enhancements**

### **Planned Features**
- **Multi-language Support**: Campaign generation in multiple languages
- **Advanced Analytics**: Campaign performance tracking
- **A/B Testing**: Multiple campaign variations
- **Extended Video Lengths**: 15-30 second video options
- **Custom Branding**: User-uploaded brand assets
- **Batch Processing**: Multiple campaigns simultaneously


