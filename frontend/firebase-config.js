// This file will be populated by your CI/CD pipeline or environment configuration.
// For local development, you can create a firebase-config.local.js and reference it.

// Firebase Configuration
// SECURITY NOTE: This Firebase API key is safe to be public as it only allows
// Firebase Authentication and is restricted by Firebase Security Rules
const firebaseConfig = {
    apiKey: "AIzaSyCFZkSE50Zh9kzioNE1RfWfNO4gGUkqs7I",
    authDomain: "adkchl.firebaseapp.com",
    projectId: "adkchl",
    storageBucket: "adkchl.firebasestorage.app",
    messagingSenderId: "661519955445",
    appId: "1:661519955445:web:86bb0f5aee5b2221019cbc"
};

// Initialize Firebase
firebase.initializeApp(firebaseConfig);

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