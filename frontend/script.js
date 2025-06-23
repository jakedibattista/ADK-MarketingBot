// --- Main Application ---

class MarketingApp {
    constructor() {
        // Make this instance globally accessible for onclick handlers
        window.marketingApp = this;
        
        this.currentUser = null;
        this.campaignData = null;
        this.selectedCampaign = null;
        this.serviceUrl = null; // Will be set in initializeApp
        
        // Add CSS for campaign selection buttons
        this.addButtonStyles();
        
        this.initializeApp();
    }

    addButtonStyles() {
        var style = document.createElement('style');
        style.textContent = `
            .select-campaign-btn {
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                color: white;
                border: none;
                padding: 12px 24px;
                border-radius: 8px;
                font-size: 16px;
                font-weight: bold;
                cursor: pointer;
                margin-top: 15px;
                width: 100%;
                transition: all 0.3s ease;
                box-shadow: 0 4px 15px rgba(102, 126, 234, 0.3);
            }
            
            .select-campaign-btn:hover {
                transform: translateY(-2px);
                box-shadow: 0 6px 20px rgba(102, 126, 234, 0.4);
                background: linear-gradient(135deg, #764ba2 0%, #667eea 100%);
            }
            
            .select-campaign-btn:active {
                transform: translateY(0);
                box-shadow: 0 2px 10px rgba(102, 126, 234, 0.3);
            }
            
            .select-concept-btn {
                background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
                color: white;
                border: none;
                padding: 12px 24px;
                border-radius: 8px;
                font-size: 16px;
                font-weight: bold;
                cursor: pointer;
                margin-top: 15px;
                width: 100%;
                transition: all 0.3s ease;
                box-shadow: 0 4px 15px rgba(240, 147, 251, 0.3);
            }
            
            .select-concept-btn:hover {
                transform: translateY(-2px);
                box-shadow: 0 6px 20px rgba(240, 147, 251, 0.4);
                background: linear-gradient(135deg, #f5576c 0%, #f093fb 100%);
            }
            
            .select-concept-btn:active {
                transform: translateY(0);
                box-shadow: 0 2px 10px rgba(240, 147, 251, 0.3);
            }
            
            .idea-card {
                margin-bottom: 20px;
                padding: 20px;
                border: 1px solid #e1e8ed;
                border-radius: 12px;
                background: white;
                box-shadow: 0 2px 8px rgba(0,0,0,0.1);
            }
            
            .concept-card {
                margin-bottom: 20px;
                padding: 20px;
                border: 1px solid #e1e8ed;
                border-radius: 12px;
                background: white;
                box-shadow: 0 2px 8px rgba(0,0,0,0.1);
            }
            
            .concept-image img {
                max-width: 100%;
                border-radius: 8px;
                margin: 10px 0;
            }
            
            .campaign-section {
                margin-bottom: 15px;
            }
            
            .campaign-name {
                font-size: 18px;
                font-weight: bold;
                color: #2c3e50;
                margin-bottom: 15px;
                padding-bottom: 10px;
                border-bottom: 2px solid #3498db;
            }
            
            .campaign-label {
                font-weight: bold;
                color: #34495e;
                margin-bottom: 5px;
                font-size: 14px;
            }
            
            .campaign-text {
                color: #555;
                line-height: 1.5;
                margin-bottom: 10px;
                padding-left: 20px;
                font-size: 14px;
            }
            
            .campaign-fallback {
                color: #555;
                line-height: 1.6;
                padding: 15px;
                background: #f8f9fa;
                border-radius: 8px;
                border-left: 4px solid #3498db;
                font-size: 14px;
            }
        `;
        document.head.appendChild(style);
    }

    initializeApp() {
        this.setupEventListeners();
        this.checkAuthState();
        this.loadConfig(); // Load configuration
    }

    setupEventListeners() {
        // Authentication
        var loginBtn = document.getElementById('loginBtn');
        var logoutBtn = document.getElementById('logoutBtn');
        
        if (loginBtn) {
            loginBtn.addEventListener('click', () => this.signInWithGoogle());
        }
        
        if (logoutBtn) {
            logoutBtn.addEventListener('click', () => this.signOut());
        }

        // Campaign form
        var campaignForm = document.getElementById('campaignForm');
        if (campaignForm) {
            campaignForm.addEventListener('submit', (e) => this.handleCampaignSubmit(e));
        }

        // Dynamic event listeners are removed as the new flow is one-shot
    }

    async loadConfig() {
        try {
            const response = await fetch('firebase-config.js');
            const text = await response.text();
            // This is a simplified and insecure way to parse the config.
            // In a real app, you would fetch a JSON file.
            const serviceUrlMatch = text.match(/serviceUrl: "(.*?)"/);
            if (serviceUrlMatch && serviceUrlMatch[1]) {
                this.serviceUrl = serviceUrlMatch[1];
                console.log('Service URL loaded:', this.serviceUrl);
            } else {
                // Fallback to getServiceUrl if not in config
                this.serviceUrl = this.getServiceUrl();
                console.warn("serviceUrl not found in config, using fallback.");
            }
        } catch (error) {
            console.error("Failed to load configuration, using fallback:", error);
            this.serviceUrl = this.getServiceUrl();
        }
    }

    getServiceUrl() {
        // This function is now a fallback.
        if (window.location.hostname === "localhost" || window.location.hostname === "127.0.0.1") {
            return "http://localhost:8080"; // Local Docker service
        } else {
            return "https://adk-marketing-platform-661519955445.us-central1.run.app"; 
        }
    }

    checkAuthState() {
        firebase.auth().onAuthStateChanged((user) => {
            if (user) {
                this.currentUser = user;
                this.showApp();
                this.updateUserInfo(user);
            } else {
                this.currentUser = null;
                this.showAuth();
            }
        });
    }

    async signInWithGoogle() {
        try {
            var provider = new firebase.auth.GoogleAuthProvider();
            provider.addScope('https://www.googleapis.com/auth/cloud-platform');
            
            var result = await firebase.auth().signInWithPopup(provider);
            console.log('Successfully signed in:', result.user.email);
        } catch (error) {
            console.error('Sign in failed:', error);
            this.showNotification('Sign in failed. Please try again.', 'error');
        }
    }

    async signOut() {
        try {
            await firebase.auth().signOut();
            console.log('Successfully signed out');
        } catch (error) {
            console.error('Sign out failed:', error);
        }
    }

    showAuth() {
        document.getElementById('authSection').style.display = 'block';
        document.getElementById('appSection').style.display = 'none';
    }

    showApp() {
        document.getElementById('authSection').style.display = 'none';
        document.getElementById('appSection').style.display = 'block';
    }

    updateUserInfo(user) {
        var userInfo = document.getElementById('userInfo');
        
        if (userInfo) {
            userInfo.textContent = `Welcome, ${user.displayName || user.email}!`;
        }
    }

    async handleCampaignSubmit(e) {
        e.preventDefault();
        
        var formData = new FormData(e.target);
        this.campaignData = {
            companyName: formData.get('companyName'),
            companyDomain: formData.get('companyDomain'),
            goalsAudience: formData.get('goalsAudience')
        };

        var submitBtn = e.target.querySelector('button[type="submit"]');
        var originalText = submitBtn.textContent;
        
        try {
            if (!this.serviceUrl) {
                this.showNotification("Configuration error: Service URL is not available. Please refresh and try again.", "error");
                submitBtn.textContent = originalText;
                submitBtn.disabled = false;
                return;
            }

            submitBtn.textContent = 'Processing...';
            submitBtn.disabled = true;
            this.clearResults();
            
            await this.runMarketingWorkflow();
            
        } catch (error) {
            console.error('Campaign generation failed:', error);
            this.showNotification('Campaign generation failed. Please try again.', 'error');
        } finally {
            submitBtn.textContent = originalText;
            submitBtn.disabled = false;
        }
    }
    
    clearResults() {
        document.getElementById('campaign-ideas').style.display = 'none';
        document.getElementById('visual-concepts').style.display = 'none';
        document.getElementById('video-generation').style.display = 'none';
        document.getElementById('ideas-container').innerHTML = '';
        document.getElementById('concepts-container').innerHTML = '';
        document.getElementById('video-container').innerHTML = '';
    }

    async runMarketingWorkflow() {
        this.showNotification('🚀 Starting complete marketing campaign generation...', 'info');
        
        try {
            var campaignRequest = `Company: ${this.campaignData.companyName}\nWebsite: ${this.campaignData.companyDomain}\nGoals/Target Audience: ${this.campaignData.goalsAudience}\n\nPlease generate a complete marketing campaign following the full workflow.`;

            var response = await fetch(this.serviceUrl + '/query', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    query: campaignRequest
                })
            });
            
            if (response.ok) {
                var data = await response.json();
                this.processAgentResponse(data.response);
            } else {
                var errorText = await response.text();
                throw new Error(`Cloud Run API call failed: ${errorText}`);
            }
        } catch (error) {
            console.error('Marketing workflow failed:', error);
            this.showNotification(`❌ Marketing workflow failed: ${error.message}`, 'error');
            throw error;
        }
    }
    
    processAgentResponse(content) {
        this.showNotification('✅ Agent workflow complete! Processing results...', 'success');
        
        if (content.includes('CAMPAIGN A:')) {
            this.processCampaignIdeas(content);
        }
        if (content.includes('VISUAL CONCEPT')) {
            this.processVisualConcepts(content);
        }
        if (content.includes('VIDEO GENERATION')) {
            this.processVideoGeneration(content);
        }
    }

    processCampaignIdeas(content) {
        var ideasContainer = document.getElementById('ideas-container');
        var ideasSection = document.getElementById('campaign-ideas');
        
        var ideasHTML = '';
        var campaignARegex = /🚀 \*\*CAMPAIGN A:([\s\S]*?)(?=🚀 \*\*CAMPAIGN B:|\n\n\n)/;
        var campaignBRegex = /🚀 \*\*CAMPAIGN B:([\s\S]*)/;

        var matchA = content.match(campaignARegex);
        var matchB = content.match(campaignBRegex);

        if (matchA) {
            var formattedA = this.formatCampaignContent(matchA[0]);
            ideasHTML += `
                <div class="idea-card">
                    <h3>CAMPAIGN A</h3>
                    <div class="campaign-content">${formattedA}</div>
                    <button class="select-campaign-btn" onclick="window.marketingApp.selectCampaign('A', \`${matchA[0].replace(/`/g, '\\`').replace(/\$/g, '\\$')}\`)">
                        🚀 Select Campaign A
                    </button>
                </div>
            `;
        }
        if (matchB) {
            var formattedB = this.formatCampaignContent(matchB[0]);
            ideasHTML += `
                <div class="idea-card">
                    <h3>CAMPAIGN B</h3>
                    <div class="campaign-content">${formattedB}</div>
                    <button class="select-campaign-btn" onclick="window.marketingApp.selectCampaign('B', \`${matchB[0].replace(/`/g, '\\`').replace(/\$/g, '\\$')}\`)">
                        🚀 Select Campaign B
                    </button>
                </div>
            `;
        }

        ideasContainer.innerHTML = ideasHTML;
        ideasSection.style.display = 'block';
    }
    
        formatCampaignContent(rawContent) {
        // Parse and format the campaign content for better readability
        var content = rawContent;
        
        // Extract campaign name - more flexible pattern
        var nameMatch = content.match(/🚀 \*\*CAMPAIGN [AB]:\s*(.+?)\*\*/);
        var campaignName = nameMatch ? nameMatch[1].trim() : '';
        
        // Extract big idea - more flexible pattern to handle line breaks
        var ideaMatch = content.match(/💡 \*\*The Big Idea:\*\*\s*(.+?)(?=🎯|\n\n|$)/s);
        var bigIdea = ideaMatch ? ideaMatch[1].trim() : '';
        
        // Extract target impact
        var targetMatch = content.match(/🎯 \*\*Target Impact:\*\*\s*(.+?)(?=📈|\n\n|$)/s);
        var targetImpact = targetMatch ? targetMatch[1].trim() : '';
        
        // Extract why it works
        var whyMatch = content.match(/📈 \*\*Why It Works:\*\*\s*(.+?)(?=⚡|\n\n|$)/s);
        var whyWorks = whyMatch ? whyMatch[1].trim() : '';
        
        // Extract bottom line
        var bottomMatch = content.match(/⚡ \*\*Bottom Line:\*\*\s*(.+?)(?=\n\n|$)/s);
        var bottomLine = bottomMatch ? bottomMatch[1].trim() : '';
        
        // If the structured format fails, show the raw content with basic formatting
        if (!bigIdea && !targetImpact && !whyWorks && !bottomLine) {
            return `<div class="campaign-fallback">${content.replace(/\*\*/g, '').replace(/\n/g, '<br>')}</div>`;
        }
        
        return `
            <div class="campaign-section">
                <h4 class="campaign-name">🚀 ${campaignName}</h4>
            </div>
            <div class="campaign-section">
                <div class="campaign-label">💡 The Big Idea</div>
                <div class="campaign-text">${bigIdea}</div>
            </div>
            <div class="campaign-section">
                <div class="campaign-label">🎯 Target Impact</div>
                <div class="campaign-text">${targetImpact}</div>
            </div>
            <div class="campaign-section">
                <div class="campaign-label">📈 Why It Works</div>
                <div class="campaign-text">${whyWorks}</div>
            </div>
            <div class="campaign-section">
                <div class="campaign-label">⚡ Bottom Line</div>
                <div class="campaign-text">${bottomLine}</div>
            </div>
        `;
    }

    async selectCampaign(campaignLetter, campaignContent) {
        this.showNotification(`✅ Selected Campaign ${campaignLetter}! Generating visual concepts...`, 'success');
        this.selectedCampaign = { letter: campaignLetter, content: campaignContent };
        
        try {
            var visualServiceUrl = this.serviceUrl + '/generate-visual';
            
            // Generate both concepts using AI with campaign content - make them distinctly different
            var [response1, response2] = await Promise.all([
                fetch(visualServiceUrl, {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ 
                        concept: "1 - Lifestyle/Aspirational Style: Focus on emotional connection, lifestyle moments, and aspirational imagery. Use warm, natural lighting and authentic human interactions.",
                        campaign_content: campaignContent 
                    })
                }),
                fetch(visualServiceUrl, {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ 
                        concept: "2 - Bold/Dynamic Style: Focus on product features, bold graphics, vibrant colors, and energetic compositions. Use dramatic lighting and striking visual elements.", 
                        campaign_content: campaignContent 
                    })
                })
            ]);
            
            // Check each response individually
            console.log('Response 1 status:', response1.status, response1.ok);
            console.log('Response 2 status:', response2.status, response2.ok);
            
            if (!response1.ok) {
                var error1 = await response1.text();
                console.error('Visual Concept 1 failed:', error1);
                throw new Error(`Visual Concept 1 generation failed: ${error1}`);
            }
            
            if (!response2.ok) {
                var error2 = await response2.text();
                console.error('Visual Concept 2 failed:', error2);
                throw new Error(`Visual Concept 2 generation failed: ${error2}`);
            }
            
            var data1 = await response1.json();
            var data2 = await response2.json();
            
            console.log('Visual Concept 1 data:', data1);
            console.log('Visual Concept 2 data:', data2);
            
            // Check if both concepts have the required data
            if (!data1.caption || !data1.image_data) {
                console.error('Visual Concept 1 missing data:', data1);
                throw new Error('Visual Concept 1 is missing required data');
            }
            
            if (!data2.caption || !data2.image_data) {
                console.error('Visual Concept 2 missing data:', data2);
                throw new Error('Visual Concept 2 is missing required data');
            }
            
            // Display using AI-generated captions
            this.displayVisualConcepts(data1, data2, data1.caption, data2.caption);
        } catch (error) {
            console.error('Visual concept generation failed:', error);
            this.showNotification(`❌ Visual generation failed: ${error.message}`, 'error');
        }
    }
    
    displayVisualConcepts(data1, data2, concept1, concept2) {
        var conceptsContainer = document.getElementById('concepts-container');
        var conceptsSection = document.getElementById('visual-concepts');
        
        var conceptsHTML = `
            <div class="concept-card">
                <h3>VISUAL CONCEPT 1</h3>
                <div class="concept-image"><img src="${data1.image_data}" alt="Visual Concept 1"></div>
                <p class="concept-description" style="font-style: italic; color: #666; line-height: 1.4; font-size: 14px;">${concept1}</p>
                <button class="select-concept-btn" onclick="window.marketingApp.selectVisualConcept('1', \`${concept1.replace(/`/g, '\\`')}\`, '${data1.image_data}')">
                    🎨 Select Concept 1
                </button>
            </div>
            <div class="concept-card">
                <h3>VISUAL CONCEPT 2</h3>
                <div class="concept-image"><img src="${data2.image_data}" alt="Visual Concept 2"></div>
                <p class="concept-description" style="font-style: italic; color: #666; line-height: 1.4; font-size: 14px;">${concept2}</p>
                <button class="select-concept-btn" onclick="window.marketingApp.selectVisualConcept('2', \`${concept2.replace(/`/g, '\\`')}\`, '${data2.image_data}')">
                    🎨 Select Concept 2
                </button>
            </div>
        `;
        
        conceptsContainer.innerHTML = conceptsHTML;
        conceptsSection.style.display = 'block';
        
        this.showNotification('✅ Visual concepts generated successfully!', 'success');
    }

    processVisualConcepts(content) {
        var conceptsContainer = document.getElementById('concepts-container');
        var conceptsSection = document.getElementById('visual-concepts');
        
        var conceptsHTML = '';
        // Updated regex to handle base64 data URLs
        var visualConceptsRegex = /🎨 \*\*VISUAL CONCEPT (\d+):\*\*([\s\S]*?)🖼️ \*\*Image:\*\* (data:image\/[^;\s]+;base64,[A-Za-z0-9+/=]+)/g;
        var match;
        var conceptIndex = 1;
        
        while ((match = visualConceptsRegex.exec(content)) !== null) {
            var conceptNumber = match[1];
            var conceptDescription = match[2].trim();
            var imageData = match[3];
            
            conceptsHTML += `
                <div class="concept-card">
                    <h3>VISUAL CONCEPT ${conceptNumber}</h3>
                    <div class="concept-image"><img src="${imageData}" alt="Visual Concept ${conceptNumber}"></div>
                    <p class="concept-description">${conceptDescription}</p>
                    <button class="select-concept-btn" onclick="window.marketingApp.selectVisualConcept('${conceptNumber}', \`${conceptDescription.replace(/`/g, '\\`').replace(/\$/g, '\\$')}\`, '${imageData}')">
                        🎨 Select Concept ${conceptNumber}
                    </button>
                </div>
            `;
            conceptIndex++;
        }
        
        conceptsContainer.innerHTML = conceptsHTML;
        conceptsSection.style.display = 'block';
    }

    async selectVisualConcept(conceptNumber, conceptDescription, imageUrl) {
        this.showNotification(`✅ Selected Visual Concept ${conceptNumber}! Generating professional script...`, 'success');
        this.selectedVisualConcept = { 
            number: conceptNumber, 
            description: conceptDescription, 
            imageUrl: imageUrl 
        };
        
        try {
            // Step 1: Generate professional script using Script Writer Agent
            this.showNotification('📝 Creating cinematic video script with Script Writer Agent...', 'info');
            
            var scriptResponse = await fetch(this.serviceUrl + '/generate-script', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({
                    campaign_content: this.selectedCampaign.content,
                    visual_concept: conceptDescription,
                    company_name: this.campaignData.companyName
                })
            });
            
            if (!scriptResponse.ok) {
                throw new Error(`Script generation failed: ${scriptResponse.status}`);
            }
            
            var scriptData = await scriptResponse.json();
            var campaignScript = scriptData.script;
            
            console.log('Generated professional script:', campaignScript);
            
            // Display the professional script
            this.displayScriptGeneration(campaignScript);
            
            // Step 2: Generate video using the professional script
            this.showNotification('🎬 Generating video with professional script...', 'info');
            
            var videoResponse = await fetch(this.serviceUrl + '/generate-video-direct', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({
                    script: campaignScript,
                    campaign_content: this.selectedCampaign.content,
                    visual_concept: conceptDescription
                })
            });
            
            if (videoResponse.ok) {
                var videoData = await videoResponse.json();
                console.log('Video generation response:', videoData);
                console.log('Video URL from response:', videoData.video_url);
                console.log('Response status:', videoData.success, videoData.status);
                console.log('Full response object keys:', Object.keys(videoData));
                console.log('Response success field:', videoData.success);
                console.log('Response error field:', videoData.error);
                
                // Add download button only if we have a valid video URL
                if (videoData.video_url && videoData.video_url !== 'undefined') {
                    console.log('Adding download button with URL:', videoData.video_url);
                    this.addVideoDownloadButton(videoData.video_url, campaignScript);
                }
                
                this.displayVideoResult(videoData, campaignScript);
            } else {
                var errorText = await videoResponse.text();
                console.error('Video response not OK:', videoResponse.status, errorText);
                throw new Error(`Video generation failed: ${errorText}`);
            }
            
        } catch (error) {
            console.error('Video generation failed:', error);
            this.showNotification(`❌ Video generation failed: ${error.message}`, 'error');
            
            // Fallback to basic script if Script Writer Agent fails
            var fallbackScript = `${this.selectedCampaign.content}. Visual concept: ${conceptDescription}. Company: ${this.campaignData.companyName}. Create a professional 8-second marketing video showing the campaign concept in action. NO visible text, words, letters, or typography to avoid spelling errors. Focus on visual storytelling with natural brand integration.`;
            
            // Still show the script even if video generation failed
            this.displayVideoResult({
                success: false,
                error: error.message,
                error_type: 'Generation Failed'
            }, fallbackScript);
        }
    }

    processVideoGeneration(content) {
        var videoContainer = document.getElementById('video-container');
        var videoSection = document.getElementById('video-generation');

        console.log('Processing video generation content:', content);

        // Check for Veo script in the response
        var scriptMatch = content.match(/🎬 \*\*VEO SCRIPT:\*\*([\s\S]*?)(?=🎥|⚙️|$)/);
        var scriptUsedMatch = content.match(/📝 \*\*Script Used:\*\*([\s\S]*?)(?=⚙️|🎥|$)/);
        var operationMatch = content.match(/⚙️ \*\*Operation:\*\* ([^\n]+)/);
        var statusMatch = content.match(/⏱️ \*\*Status:\*\*([\s\S]*?)(?=\n\n|$)/);
        var videoUrlMatch = content.match(/https:\/\/storage\.googleapis\.com\/[^\s)]+\.mp4/);
        
        var videoHTML = '<div class="video-result">';
        
        if (scriptMatch || scriptUsedMatch) {
            var script = scriptMatch ? scriptMatch[1].trim() : scriptUsedMatch[1].trim();
            videoHTML += `
                <h3>🎬 Video Script Generated</h3>
                <div class="script-content" style="background: #f8f9fa; padding: 15px; border-radius: 8px; margin: 10px 0; border-left: 4px solid #28a745;">
                    <strong>Veo 2.0 Script:</strong><br>
                    ${script.replace(/\n/g, '<br>')}
                </div>
            `;
        }
        
        if (operationMatch) {
            var operation = operationMatch[1];
            videoHTML += `
                <div class="operation-status" style="background: #e3f2fd; padding: 10px; border-radius: 5px; margin: 10px 0;">
                    <strong>⚙️ Generation Status:</strong> ${operation}<br>
                    <em>Video is being generated... This typically takes 60-90 seconds.</em>
                </div>
            `;
        }
        
        if (statusMatch) {
            var status = statusMatch[1].trim();
            var isError = status.toLowerCase().includes('failed') || status.toLowerCase().includes('error');
            var statusClass = isError ? '#f8d7da' : '#fff3cd';
            var statusIcon = isError ? '❌' : '⏱️';
            
            videoHTML += `
                <div class="status-info" style="background: ${statusClass}; padding: 10px; border-radius: 5px; margin: 10px 0;">
                    <strong>${statusIcon} Status:</strong><br>
                    ${status.replace(/\n/g, '<br>')}
                </div>
            `;
        }
        
        if (videoUrlMatch) {
            videoHTML += `
                <h3>🎉 Campaign Video Complete!</h3>
                <div class="video-player" style="margin: 15px 0;">
                    <video controls style="width: 100%; max-width: 600px; border-radius: 8px;">
                        <source src="${videoUrlMatch[0]}" type="video/mp4">
                        Your browser does not support the video tag.
                    </video>
                </div>
                <div class="video-details" style="background: #d4edda; padding: 10px; border-radius: 5px; margin: 10px 0;">
                    <strong>✅ Video Details:</strong><br>
                    • Duration: 8 seconds<br>
                    • Format: 16:9 aspect ratio<br>
                    • Features: Native audio generation<br>
                    • Model: Veo 2.0<br>
                    • URL: <a href="${videoUrlMatch[0]}" target="_blank">Download Video</a>
                </div>
            `;
        } else if (scriptMatch || scriptUsedMatch || operationMatch || statusMatch) {
            videoHTML += `
                <div class="waiting-message" style="background: #fff3cd; padding: 10px; border-radius: 5px; margin: 10px 0;">
                    <strong>⏳ Please wait...</strong><br>
                    Video generation is in progress. The video will appear here when ready.
                </div>
            `;
        } else {
            // Fallback for other content
            videoHTML += `
                <h3>🎬 Video Generation Started</h3>
                <div class="generation-content" style="background: #f8f9fa; padding: 15px; border-radius: 8px; margin: 10px 0;">
                    ${content.replace(/\n/g, '<br>')}
                </div>
            `;
        }
        
        videoHTML += '</div>';
        
        videoContainer.innerHTML = videoHTML;
        videoSection.style.display = 'block';
        
        // Show success notification
        if (videoUrlMatch) {
            this.showNotification('🎉 Campaign video generated successfully!', 'success');
        } else if (scriptMatch || scriptUsedMatch) {
            this.showNotification('📝 Video script created, generating video...', 'info');
        } else if (statusMatch && statusMatch[1].toLowerCase().includes('failed')) {
            this.showNotification('❌ Video generation failed. Check status for details.', 'error');
        }
    }

    displayScriptGeneration(script) {
        var videoSection = document.getElementById('video-section');
        if (!videoSection) {
            // Try to use existing video-container first
            var videoContainer = document.getElementById('video-container');
            if (videoContainer) {
                videoSection = document.createElement('div');
                videoSection.id = 'video-section';
                videoSection.className = 'video-section';
                videoContainer.appendChild(videoSection);
            } else {
                // Create video section if it doesn't exist
                videoSection = document.createElement('div');
                videoSection.id = 'video-section';
                videoSection.className = 'video-section';
                
                // Find a safe place to append it
                var mainContent = document.querySelector('.container');
                if (!mainContent) {
                    mainContent = document.body;
                }
                mainContent.appendChild(videoSection);
            }
        }
        
        videoSection.innerHTML = `
            <h3>📝 Generated Video Script</h3>
            <div class="script-display">
                <p><strong>Veo 2.0 Script:</strong></p>
                <div class="script-content">${script}</div>
            </div>
            <div class="video-generation-status">
                <p>🎬 Generating video with Veo 2.0... This may take up to 5 minutes.</p>
                <div class="loading-spinner"></div>
            </div>
        `;
        
        videoSection.scrollIntoView({ behavior: 'smooth' });
    }

    displayVideoResult(videoData, script) {
        console.log('Displaying video result:', videoData);
        
        // Find or create video section
        var videoSection = document.getElementById('video-section');
        if (!videoSection) {
            // Try to use existing video-container first
            var videoContainer = document.getElementById('video-container');
            if (videoContainer) {
                videoSection = document.createElement('div');
                videoSection.id = 'video-section';
                videoSection.className = 'video-section';
                videoContainer.appendChild(videoSection);
            } else {
                videoSection = document.createElement('div');
                videoSection.id = 'video-section';
                videoSection.className = 'video-section';
                
                // Find a safe place to append it
                var mainContent = document.querySelector('.container');
                if (!mainContent) {
                    mainContent = document.body;
                }
                mainContent.appendChild(videoSection);
            }
        }
        
        // Make sure the video section is visible
        videoSection.style.display = 'block';
        videoSection.style.visibility = 'visible';
        
        if (videoData.success && videoData.video_url) {
            // Successful video generation
            videoSection.innerHTML = `
                <div style="background: white; border-radius: 12px; padding: 24px; margin: 20px 0; box-shadow: 0 2px 8px rgba(0,0,0,0.1); border: 2px solid #4CAF50;">
                    <h3 style="color: #4CAF50; margin-top: 0;">🎬 Veo 2.0 Video Generated Successfully!</h3>
                    
                    <div class="script-display" style="background: #f8f9fa; border-radius: 8px; padding: 16px; margin: 16px 0; border-left: 4px solid #4285f4;">
                        <p><strong>Script Used:</strong></p>
                        <div class="script-content" style="font-family: 'Courier New', monospace; background: white; padding: 12px; border-radius: 6px; border: 1px solid #e1e5e9; white-space: pre-wrap; line-height: 1.5; max-height: 150px; overflow-y: auto;">${script}</div>
                    </div>
                    
                    <div class="video-info" style="background: #d4edda; border: 1px solid #c3e6cb; border-radius: 8px; padding: 16px; margin: 16px 0;">
                        <p style="margin: 8px 0; font-weight: 500;"><strong>✅ Status:</strong> ${videoData.status}</p>
                        <p style="margin: 8px 0; font-weight: 500;"><strong>⏱️ Generation Time:</strong> ${videoData.elapsed_time}s</p>
                        <p style="margin: 8px 0; font-weight: 500;"><strong>🎥 Model:</strong> ${videoData.model}</p>
                        <p style="margin: 8px 0; font-weight: 500;"><strong>📏 Features:</strong> ${videoData.features.duration}, ${videoData.features.aspect_ratio}</p>
                        ${videoData.video_count ? `<p style="margin: 8px 0; font-weight: 500;"><strong>🎞️ Videos Generated:</strong> ${videoData.video_count}</p>` : ''}
                    </div>
                    
                    <div class="video-container" style="background: #f0f8ff; border-radius: 8px; padding: 20px; margin: 16px 0; border: 2px dashed #4285f4; text-align: center;">
                        <h4 style="color: #4285f4; margin-top: 0;">🎬 Your Veo 2.0 Video is Ready!</h4>
                        <p style="margin: 12px 0;">Your video has been successfully created. Click the buttons below to access it:</p>
                        
                        <div class="video-actions" style="margin-top: 20px;">
                            <button onclick="window.open('${videoData.video_url}', '_blank')" style="
                                background: linear-gradient(90deg, #50e3c2, #4a90e2);
                                color: white;
                                border: none;
                                padding: 12px 20px;
                                border-radius: 8px;
                                font-size: 1rem;
                                font-weight: 500;
                                cursor: pointer;
                                margin-top: 15px;
                                transition: all 0.3s ease;
                                display: inline-block;
                                width: auto;
                            " onmouseover="this.style.transform='translateY(-2px)'; this.style.boxShadow='0 4px 15px rgba(0,0,0,0.1)'" onmouseout="this.style.transform='none'; this.style.boxShadow='none'">
                                📥 Download Video (.mp4)
                            </button>
                            <a href="${videoData.video_url}" target="_blank" class="download-btn" style="display: inline-block; background: #34a853; color: white; padding: 12px 24px; border-radius: 6px; text-decoration: none; font-weight: 500; margin: 0 8px;">🎥 Open in New Tab</a>
                        </div>
                        
                        <div style="margin-top: 16px; padding: 12px; background: #fff3cd; border-radius: 6px; font-size: 0.9em; color: #856404;">
                            <p style="margin: 0;"><strong>💡 Tip:</strong> Veo 2.0 videos require API authentication and may not play directly in browser. Use the download button to save the .mp4 file to your computer for viewing.</p>
                        </div>
                        
                        <div style="margin-top: 12px; font-size: 0.8em; color: #666; word-break: break-all;">
                            <p><strong>Video URL:</strong> ${videoData.video_url}</p>
                        </div>
                    </div>
                </div>
            `;
            
            this.showNotification('🎉 Video generated successfully! Scroll down to download.', 'success');
            
        } else if (videoData.status === 'timeout') {
            // Timeout but may still be processing
            videoSection.innerHTML = `
                <div style="background: white; border-radius: 12px; padding: 24px; margin: 20px 0; box-shadow: 0 2px 8px rgba(0,0,0,0.1); border: 2px solid #ff9800;">
                    <h3 style="color: #ff9800;">⏰ Video Generation Timeout</h3>
                    <div class="script-display" style="background: #f8f9fa; border-radius: 8px; padding: 16px; margin: 16px 0; border-left: 4px solid #4285f4;">
                        <p><strong>Script Used:</strong></p>
                        <div class="script-content" style="font-family: 'Courier New', monospace; background: white; padding: 12px; border-radius: 6px; border: 1px solid #e1e5e9; white-space: pre-wrap; line-height: 1.5; max-height: 150px; overflow-y: auto;">${script}</div>
                    </div>
                    <div class="video-timeout" style="background: #fff3cd; border: 1px solid #ffeaa7; border-radius: 8px; padding: 16px; margin: 16px 0;">
                        <p style="margin: 8px 0;"><strong>⚠️ Status:</strong> ${videoData.message}</p>
                        <p style="margin: 8px 0;"><strong>⏱️ Elapsed Time:</strong> ${videoData.elapsed_time}s</p>
                        <p style="margin: 8px 0;"><strong>🔄 Operation:</strong> ${videoData.operation_name}</p>
                        <p style="margin: 8px 0;">The video may still be processing in the background. Veo 2.0 videos can take up to 5 minutes to generate.</p>
                    </div>
                </div>
            `;
            
            this.showNotification('⏰ Video generation timed out but may still be processing', 'warning');
            
        } else {
            // Error in generation
            videoSection.innerHTML = `
                <div style="background: white; border-radius: 12px; padding: 24px; margin: 20px 0; box-shadow: 0 2px 8px rgba(0,0,0,0.1); border: 2px solid #f44336;">
                    <h3 style="color: #f44336;">❌ Video Generation Failed</h3>
                    <div class="script-display" style="background: #f8f9fa; border-radius: 8px; padding: 16px; margin: 16px 0; border-left: 4px solid #4285f4;">
                        <p><strong>Script Used:</strong></p>
                        <div class="script-content" style="font-family: 'Courier New', monospace; background: white; padding: 12px; border-radius: 6px; border: 1px solid #e1e5e9; white-space: pre-wrap; line-height: 1.5; max-height: 150px; overflow-y: auto;">${script}</div>
                    </div>
                    <div class="video-error" style="background: #f8d7da; border: 1px solid #f5c6cb; border-radius: 8px; padding: 16px; margin: 16px 0;">
                        <p style="margin: 8px 0; color: #721c24;"><strong>❌ Error:</strong> ${videoData.error || videoData.message || 'Unknown error'}</p>
                        <p style="margin: 8px 0; color: #721c24;"><strong>🔧 Error Type:</strong> ${videoData.error_type || 'Unknown'}</p>
                        ${videoData.operation_name ? `<p style="margin: 8px 0; color: #721c24;"><strong>🔄 Operation:</strong> ${videoData.operation_name}</p>` : ''}
                    </div>
                </div>
            `;
            
            this.showNotification(`❌ Video generation failed: ${videoData.error || 'Unknown error'}`, 'error');
        }
        
        // Scroll to the video section
        videoSection.scrollIntoView({ behavior: 'smooth', block: 'start' });
        
        // Add a small delay and scroll again to ensure visibility
        setTimeout(() => {
            videoSection.scrollIntoView({ behavior: 'smooth', block: 'start' });
        }, 100);
    }

    showNotification(message, type = 'info') {
        var notification = document.createElement('div');
        notification.className = `notification ${type}`;
        notification.textContent = message;
        notification.style.cssText = `
            position: fixed;
            top: 20px;
            right: 20px;
            padding: 12px 20px;
            background: ${type === 'success' ? '#d4edda' : type === 'error' ? '#f8d7da' : '#d1ecf1'};
            color: ${type === 'success' ? '#155724' : type === 'error' ? '#721c24' : '#0c5460'};
            border: 1px solid ${type === 'success' ? '#c3e6cb' : type === 'error' ? '#f5c6cb' : '#bee5eb'};
            border-radius: 6px;
            box-shadow: 0 2px 8px rgba(0,0,0,0.1);
            z-index: 1000;
            max-width: 300px;
            word-wrap: break-word;
        `;
        
        document.body.appendChild(notification);
        
        setTimeout(() => {
            if (notification.parentNode) {
                notification.parentNode.removeChild(notification);
            }
        }, 5000);
    }
    
    // Test function to verify video display is working
    testVideoDisplay() {
        console.log('Testing video display...');
        var mockVideoData = {
            success: true,
            status: 'completed',
            elapsed_time: 41,
            model: 'veo-2.0-generate-001',
            features: {
                duration: '8 seconds',
                aspect_ratio: '16:9'
            },
            video_count: 1,
            video_url: 'https://example.com/test-video.mp4'
        };
        
        var mockScript = 'Test script for video display verification. This is a mock script to test if the video result display is working properly.';
        
        this.displayVideoResult(mockVideoData, mockScript);
        this.showNotification('🧪 Test video display triggered', 'info');
    }

    addVideoDownloadButton(videoUrl, script) {
        // Find the visual concepts section to add the button after it
        var conceptsSection = document.getElementById('visual-concepts');
        if (!conceptsSection) {
            conceptsSection = document.querySelector('.container');
        }
        
        // Remove any existing video download section
        var existingVideoDownload = document.getElementById('video-download-section');
        if (existingVideoDownload) {
            existingVideoDownload.remove();
        }
        
        // Create the download section
        var downloadSection = document.createElement('div');
        downloadSection.id = 'video-download-section';
        downloadSection.style.cssText = `
            background: white;
            padding: 24px;
            margin: 20px 0;
            border-radius: 12px;
            box-shadow: 0 2px 8px rgba(0,0,0,0.1);
            border: 1px solid #e1e5e9;
            text-align: center;
        `;
        
        downloadSection.innerHTML = `
            <h3 style="margin: 0 0 16px 0; font-size: 20px; color: #333;">🎬 VIDEO GENERATED</h3>
            <p style="margin: 0 0 20px 0; font-size: 14px; color: #666; line-height: 1.4;">
                Your Veo 2.0 video has been successfully generated! Click the button below to download your marketing video.
            </p>
            
            <div style="text-align: center; margin: 20px 0;">
                <button onclick="window.open('${videoUrl}', '_blank')" style="
                    background: linear-gradient(90deg, #50e3c2, #4a90e2);
                    color: white;
                    border: none;
                    padding: 14px 28px;
                    border-radius: 8px;
                    font-size: 1rem;
                    font-weight: 500;
                    cursor: pointer;
                    transition: all 0.3s ease;
                    display: inline-block;
                    margin: 0 auto;
                " onmouseover="this.style.transform='translateY(-2px)'; this.style.boxShadow='0 4px 15px rgba(0,0,0,0.1)'" onmouseout="this.style.transform='none'; this.style.boxShadow='none'">
                    📥 Download Video (.mp4)
                </button>
            </div>
            
            <div style="margin-top: 20px; text-align: left;">
                <h4 style="margin: 0 0 12px 0; font-size: 16px; color: #333; text-align: center;">📝 Generated Video Script:</h4>
                <div style="
                    background: #f8f9fa;
                    color: #333;
                    padding: 16px;
                    border-radius: 6px;
                    font-family: 'Segoe UI', Arial, sans-serif;
                    line-height: 1.6;
                    font-size: 14px;
                    max-height: 300px;
                    overflow-y: auto;
                    border: 1px solid #e1e5e9;
                    text-align: left;
                ">${script}</div>
            </div>
            
            <p style="margin: 16px 0 0 0; font-size: 12px; color: #999;">
                💡 Note: Videos require API authentication. If the direct link doesn't work, try right-clicking and "Save As" to download.
            </p>
        `;
        
        // Insert after the concepts section
        if (conceptsSection.nextSibling) {
            conceptsSection.parentNode.insertBefore(downloadSection, conceptsSection.nextSibling);
        } else {
            conceptsSection.parentNode.appendChild(downloadSection);
        }
        
        // Scroll to the download section
        downloadSection.scrollIntoView({ behavior: 'smooth', block: 'center' });
        
        // Show success notification
        this.showNotification('🎉 Video ready! Download button added below.', 'success');
    }

    extractDetailedScript(fullResponse) {
        console.log('Extracting detailed script from:', fullResponse);
        
        // Look for patterns that indicate a detailed video script
        var scriptPatterns = [
            // Pattern 1: Look for "Veo 2.0 Video Script:" or similar headers
            /(?:Veo 2\.0 Video Script|VIDEO SCRIPT|Video Script)[:\s]*\n([\s\S]*?)(?=INSTAGRAM_CAPTION|$)/i,
            // Pattern 2: Look for scene/shot descriptions with timing
            /(\*\*Scene[:\s]*.*?\*\*[\s\S]*?(?:\*\*Shot \d+.*?\*\*[\s\S]*?)*)/i,
            // Pattern 3: Look for shot descriptions with timing like "Shot 1 (0-1.5 seconds)"
            /(\*\*Shot \d+.*?\*\*[\s\S]*?)(?=INSTAGRAM_CAPTION|$)/i,
            // Pattern 4: Look for content with camera movements and timing
            /(.*?(?:Camera Movement|Lighting and Mood|Audio).*?[\s\S]*?)(?=INSTAGRAM_CAPTION|$)/i,
            // Pattern 5: Look for "Scene 1", "Scene 2", etc. with timing
            /(.*Scene \d+.*[\s\S]*?)(?=INSTAGRAM_CAPTION|$)/i,
            // Pattern 6: Look for content that has "seconds" and scene descriptions
            /(.*\d+-\d+ seconds.*[\s\S]*?)(?=INSTAGRAM_CAPTION|$)/i
        ];
        
        for (var pattern of scriptPatterns) {
            var match = fullResponse.match(pattern);
            if (match && match[1] && match[1].trim().length > 100) {
                var script = match[1].trim();
                console.log('Found detailed script:', script);
                return script;
            }
        }
        
        // Fallback: If the response contains script-like content (shots, camera, timing)
        if (fullResponse.includes('Shot') && fullResponse.includes('Camera') && fullResponse.includes('seconds')) {
            console.log('Using full response as detailed script');
            return fullResponse;
        }
        
        // Fallback: If the response contains "Scene" and timing info
        if (fullResponse.includes('Scene') && fullResponse.includes('seconds')) {
            console.log('Using full response as scene-based script');
            return fullResponse;
        }
        
        // If no detailed script found, return null to use the original response
        console.log('No detailed script found');
        return null;
    }
}

// Initialize the app when the page loads
document.addEventListener('DOMContentLoaded', () => {
    new MarketingApp();
}); 