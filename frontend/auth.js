// Authentication module - global approach
window.AuthManager = function() {
  let user = null;
  let authToken = null;
  let authStateCallbacks = [];
  
  // Initialize Firebase auth functions
  const initAuth = async () => {
    // Wait for Firebase auth functions to be available
    const authModule = await import('https://www.gstatic.com/firebasejs/10.7.0/firebase-auth.js');
    const { signInWithPopup, GoogleAuthProvider, signOut, onAuthStateChanged } = authModule;
    
    const auth = window.firebaseAuth;
    
    // Listen for auth state changes
    onAuthStateChanged(auth, (newUser) => {
      user = newUser;
      updateAuthToken();
      notifyAuthStateChanged(newUser);
    });
    
    return { signInWithPopup, GoogleAuthProvider, signOut, auth };
  };

  // Update authentication token
  const updateAuthToken = async () => {
    if (user) {
      try {
        authToken = await user.getIdToken();
      } catch (error) {
        console.error('Error getting auth token:', error);
        authToken = null;
      }
    } else {
      authToken = null;
    }
  };

  // Notify all callbacks about auth state changes
  const notifyAuthStateChanged = (user) => {
    authStateCallbacks.forEach(callback => callback(user));
  };

  // Public methods
  return {
    async init() {
      return await initAuth();
    },
    
    async signInWithGoogle() {
      const { signInWithPopup, GoogleAuthProvider, auth } = await initAuth();
      const provider = new GoogleAuthProvider();
      try {
        const result = await signInWithPopup(auth, provider);
        return result.user;
      } catch (error) {
        console.error('Error signing in with Google:', error);
        throw error;
      }
    },

    async signOut() {
      const { signOut, auth } = await initAuth();
      try {
        await signOut(auth);
      } catch (error) {
        console.error('Error signing out:', error);
        throw error;
      }
    },

    isAuthenticated() {
      return !!user && !!authToken;
    },

    getCurrentUser() {
      return user;
    },

    getAuthToken() {
      return authToken;
    },

    onAuthStateChanged(callback) {
      authStateCallbacks.push(callback);
    },

    getAuthHeaders() {
      if (!authToken) {
        throw new Error('User not authenticated');
      }
      return {
        'Authorization': `Bearer ${authToken}`,
        'Content-Type': 'application/json'
      };
    }
  };
};

// Create global instance
window.authManager = new window.AuthManager(); 