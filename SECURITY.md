# ADK Marketing Platform - Security Guide

## 🔐 Security Overview

This document outlines security best practices and configurations for the ADK Marketing Platform.

## ⚠️ **CRITICAL: API Key Security**

### **NEVER COMMIT THESE TO GIT:**
- Google Cloud API Keys
- Grok API Keys  
- Service Account JSON files
- Any `.env` files
- Private keys or certificates

### **SAFE TO BE PUBLIC:**
- Firebase configuration (with proper security rules)
- Project IDs
- Firebase Auth domain
- Public documentation

## 🔑 **API Key Management**

### **Backend API Keys (SENSITIVE)**
These must NEVER be exposed publicly:

```bash
# .env file (NEVER commit this)
GOOGLE_API_KEY=your_google_cloud_api_key_here    # For Vertex AI, Gemini, Veo 2.0
GROK_API_KEY=your_grok_api_key_here              # For Creative Director agent
```

**Usage**: Backend services only, via environment variables
**Deployment**: Cloud Run environment variables
**Restrictions**: Server-side only, full API access

### **Frontend API Keys (PUBLIC)**
Firebase configuration is safe to be public when properly configured:

```javascript
// firebase-config.js - Safe to be public
const firebaseConfig = {
    apiKey: "AIzaSyCFZkSE50Zh9kzioNE1RfWfNO4gGUkqs7I",  // Firebase API key
    authDomain: "adkchl.firebaseapp.com",
    projectId: "adkchl",
    // ... other Firebase config
};
```

**Why it's safe**:
- Only allows Firebase Authentication
- Restricted by Firebase Security Rules
- Cannot access Google Cloud APIs
- Domain-restricted in Firebase console

## 🛡️ **Security Configurations**

### **1. Firebase Security Rules**
```javascript
// Firestore Security Rules
rules_version = '2';
service cloud.firestore {
  match /databases/{database}/documents {
    // Only authenticated users can read/write their own data
    match /users/{userId} {
      allow read, write: if request.auth != null && request.auth.uid == userId;
    }
    
    // Public read for campaign templates, authenticated write
    match /campaigns/{campaignId} {
      allow read: if true;
      allow write: if request.auth != null;
    }
  }
}
```

### **2. Google Cloud API Key Restrictions**
Configure API key restrictions in Google Cloud Console:

```bash
# Create restricted API key for backend
gcloud alpha services api-keys create \
  --display-name="ADK Marketing Backend" \
  --api-target=service=aiplatform.googleapis.com \
  --api-target=service=generativelanguage.googleapis.com \
  --restrictions-server-key-allowed-ips="0.0.0.0/0"  # Or specific Cloud Run IPs
```

### **3. Cloud Run Security**
```yaml
# cloudbuild.yaml security settings
steps:
  - name: 'gcr.io/cloud-builders/gcloud'
    args: [
      'run', 'deploy', 'adk-marketing',
      '--no-allow-unauthenticated',  # Require authentication
      '--set-env-vars', 'ENVIRONMENT=production',
      '--vpc-connector', 'your-vpc-connector'  # Private networking
    ]
```

## 🚨 **Security Incident Response**

### **If API Key is Exposed:**

1. **Immediate Actions** (within 5 minutes):
   ```bash
   # Revoke compromised key
   gcloud alpha services api-keys delete [COMPROMISED_KEY_ID] --project=[PROJECT_ID]
   
   # Create new key
   gcloud alpha services api-keys create --display-name="Emergency Replacement"
   ```

2. **Assess Impact**:
   - Check Cloud Billing for unusual charges
   - Review Cloud Logging for unauthorized usage
   - Monitor API quotas and usage patterns

3. **Update Deployments**:
   ```bash
   # Update Cloud Run with new key
   gcloud run services update adk-marketing \
     --set-env-vars GOOGLE_API_KEY=[NEW_KEY]
   ```

4. **Prevent Future Exposure**:
   - Audit all repositories for hardcoded keys
   - Update `.gitignore` to prevent future commits
   - Implement pre-commit hooks to scan for secrets

## 🔍 **Security Monitoring**

### **Cloud Logging Queries**
Monitor for suspicious activity:

```sql
-- Unusual API usage patterns
resource.type="cloud_run_revision"
jsonPayload.message=~"API key"
severity>=WARNING

-- Failed authentication attempts
resource.type="firebase_auth"
jsonPayload.eventType="auth.signInFailure"
```

### **Billing Alerts**
Set up billing alerts for:
- Daily spending > $50
- Monthly spending > $500
- Unusual API usage spikes

### **Quota Monitoring**
Monitor API quotas for:
- Vertex AI API calls
- Gemini API requests
- Veo 2.0 video generation
- Firebase Authentication

## 📋 **Security Checklist**

### **Pre-Deployment**
- [ ] No hardcoded API keys in code
- [ ] Environment variables properly configured
- [ ] `.gitignore` includes all sensitive files
- [ ] Firebase Security Rules configured
- [ ] API key restrictions applied
- [ ] CORS properly configured

### **Post-Deployment**
- [ ] Billing alerts configured
- [ ] Logging and monitoring enabled
- [ ] API usage within expected limits
- [ ] Authentication working correctly
- [ ] No exposed credentials in logs

### **Regular Maintenance**
- [ ] Rotate API keys quarterly
- [ ] Review Firebase Security Rules
- [ ] Audit Cloud IAM permissions
- [ ] Update dependencies for security patches
- [ ] Review access logs monthly

## 🛠️ **Security Tools**

### **Pre-commit Hooks**
```bash
# Install git-secrets to prevent credential commits
git secrets --install
git secrets --register-aws
git secrets --add 'AIzaSy[0-9A-Za-z_-]{33}'  # Google API key pattern
```

### **Environment Validation**
```python
# security_check.py
import os
import re

def validate_environment():
    """Ensure no API keys are hardcoded"""
    sensitive_patterns = [
        r'AIzaSy[0-9A-Za-z_-]{33}',  # Google API key
        r'sk-[0-9A-Za-z]{48}',       # OpenAI API key
        r'xai-[0-9A-Za-z]{48}'       # Grok API key
    ]
    
    # Check all Python files for hardcoded keys
    # ... implementation
```

## 📞 **Security Contact**

### **Incident Reporting**
- **High Severity**: Immediate Slack/email notification
- **Medium Severity**: Daily security review
- **Low Severity**: Weekly security audit

### **Security Resources**
- [Google Cloud Security Best Practices](https://cloud.google.com/security/best-practices)
- [Firebase Security Documentation](https://firebase.google.com/docs/rules)
- [OWASP API Security Top 10](https://owasp.org/www-project-api-security/)

---

**Remember**: Security is everyone's responsibility. When in doubt, ask the security team before proceeding. 