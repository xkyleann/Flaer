import { writable } from 'svelte/store';

// The local FastAPI service is started by start.sh on port 8000. Deployments
// can override this with VITE_API_URL at build time.
const API_URL = import.meta.env.VITE_API_URL || 'http://127.0.0.1:8000';

// Create auth store
function createAuthStore() {
  const { subscribe, set, update } = writable({
    user: null,
    token: null,
    isAuthenticated: false,
    loading: true
  });

  return {
    subscribe,
    
    // Initialize auth from localStorage
    init: () => {
      const token = localStorage.getItem('access_token');
      const userStr = localStorage.getItem('user_info');
      
      if (token && userStr) {
        try {
          const user = JSON.parse(userStr);
          set({ user, token, isAuthenticated: true, loading: false });
        } catch (e) {
          localStorage.removeItem('access_token');
          localStorage.removeItem('user_info');
          set({ user: null, token: null, isAuthenticated: false, loading: false });
        }
      } else {
        set({ user: null, token: null, isAuthenticated: false, loading: false });
      }
    },

    // The route guard must verify a saved browser token with the API. A value
    // placed in localStorage alone is never sufficient to unlock a dashboard.
    validateSession: async () => {
      const token = localStorage.getItem('access_token');
      if (!token) return false;

      try {
        const response = await fetch(`${API_URL}/api/auth/me`, {
          headers: { Authorization: `Bearer ${token}` },
          credentials: 'include'
        });
        if (!response.ok) throw new Error('Session is invalid');

        const user = await response.json();
        localStorage.setItem('user_info', JSON.stringify(user));
        set({ user, token, isAuthenticated: true, loading: false });
        return true;
      } catch {
        localStorage.removeItem('access_token');
        localStorage.removeItem('user_info');
        set({ user: null, token: null, isAuthenticated: false, loading: false });
        return false;
      }
    },
    
    // Login
    login: async (email, password) => {
      try {
        const response = await fetch(`${API_URL}/api/auth/login`, {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          credentials: 'include',
          body: JSON.stringify({ email, password })
        });
        
        const data = await response.json();
        
        if (!response.ok) {
          throw new Error(data.detail || 'Login failed');
        }
        
        // Check if OTP is required
        if (data.requires_otp) {
          return { requiresOTP: true, email, otpCode: data.otp_code };
        }
        
        // Store token and user info
        localStorage.setItem('access_token', data.access_token);
        
        // Get user info
        const userResponse = await fetch(`${API_URL}/api/auth/me`, {
          headers: { 'Authorization': `Bearer ${data.access_token}` }
        });
        
        const user = await userResponse.json();
        localStorage.setItem('user_info', JSON.stringify(user));
        
        set({ user, token: data.access_token, isAuthenticated: true, loading: false });
        
        return { success: true };
      } catch (error) {
        set({ user: null, token: null, isAuthenticated: false, loading: false });
        if (error instanceof TypeError && /fetch|load failed/i.test(error.message)) {
          throw new Error('Cannot reach the Flaer API. Start the backend on port 8000 and try again.');
        }
        throw error;
      }
    },
    
    // Verify OTP
    verifyOTP: async (email, otpCode) => {
      try {
        const response = await fetch(`${API_URL}/api/auth/verify-otp`, {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          credentials: 'include',
          body: JSON.stringify({ email, otp_code: otpCode })
        });
        
        const data = await response.json();
        
        if (!response.ok) {
          throw new Error(data.detail || 'OTP verification failed');
        }
        
        // Store token and user info
        localStorage.setItem('access_token', data.access_token);
        
        // Get user info
        const userResponse = await fetch(`${API_URL}/api/auth/me`, {
          headers: { 'Authorization': `Bearer ${data.access_token}` }
        });
        
        const user = await userResponse.json();
        localStorage.setItem('user_info', JSON.stringify(user));
        
        set({ user, token: data.access_token, isAuthenticated: true, loading: false });
        
        return { success: true };
      } catch (error) {
        throw error;
      }
    },
    
    // Register
    register: async (email, password, fullName, company) => {
      try {
        const response = await fetch(`${API_URL}/api/auth/register`, {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          credentials: 'include',
          body: JSON.stringify({
            email,
            password,
            full_name: fullName,
            company: company || null
          })
        });
        
        const data = await response.json();
        
        if (!response.ok) {
          throw new Error(data.detail || 'Registration failed');
        }
        
        // Store token and user info
        localStorage.setItem('access_token', data.access_token);
        
        // Get user info
        const userResponse = await fetch(`${API_URL}/api/auth/me`, {
          headers: { 'Authorization': `Bearer ${data.access_token}` }
        });
        
        const user = await userResponse.json();
        localStorage.setItem('user_info', JSON.stringify(user));
        
        set({ user, token: data.access_token, isAuthenticated: true, loading: false });
        
        return { success: true };
      } catch (error) {
        throw error;
      }
    },
    
    // Logout
    logout: async () => {
      try {
        await fetch(`${API_URL}/api/auth/logout`, {
          method: 'POST',
          credentials: 'include'
        });
      } catch (e) {
        // Ignore errors
      }
      
      localStorage.removeItem('access_token');
      localStorage.removeItem('user_info');
      set({ user: null, token: null, isAuthenticated: false, loading: false });
    },
    
    // Refresh token
    refreshToken: async () => {
      try {
        const response = await fetch(`${API_URL}/api/auth/refresh`, {
          method: 'POST',
          credentials: 'include'
        });
        
        if (!response.ok) {
          throw new Error('Token refresh failed');
        }
        
        const data = await response.json();
        localStorage.setItem('access_token', data.access_token);
        
        update(state => ({ ...state, token: data.access_token }));
        
        return data.access_token;
      } catch (error) {
        // If refresh fails, logout
        localStorage.removeItem('access_token');
        localStorage.removeItem('user_info');
        set({ user: null, token: null, isAuthenticated: false, loading: false });
        throw error;
      }
    },
    
    // Get auth header
    getAuthHeader: () => {
      const token = localStorage.getItem('access_token');
      return token ? { 'Authorization': `Bearer ${token}` } : {};
    }
  };
}

export const authStore = createAuthStore();

// Initialize on load
if (typeof window !== 'undefined') {
  authStore.init();

  // Auto-refresh token every 25 minutes (token expires in 30)
  setInterval(async () => {
    const token = localStorage.getItem('access_token');
    if (token) {
      try {
        await authStore.refreshToken();
      } catch {
        // refreshToken already handles logout on failure
      }
    }
  }, 25 * 60 * 1000);
}

// Made with Bob
