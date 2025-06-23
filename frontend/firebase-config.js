// This file will be populated by your CI/CD pipeline or environment configuration.
// For local development, you can create a firebase-config.local.js and reference it.

const firebaseConfig = {
  // This configuration is now loaded dynamically and securely by Firebase Hosting
  // The content is provided by `/__/firebase/init.js`
};

// Service URL - configure this for your deployment
const serviceUrl = window.location.hostname === 'localhost' 
  ? "http://localhost:8080"  // Local development
  : "https://adk-marketing-platform-661519955445.us-central1.run.app";  // Production Cloud Run URL

// Firebase configuration - using global approach
// Wait for Firebase to be loaded
window.initializeFirebase = function() {
  const { initializeApp, getAuth } = window.firebaseImports;
  
  // Initialize Firebase
  const app = initializeApp(firebaseConfig);
  const auth = getAuth(app);
  
  // Make auth available globally
  window.firebaseAuth = auth;
  
  return { app, auth };
}; 