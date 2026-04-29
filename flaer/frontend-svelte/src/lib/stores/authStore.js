import { writable } from 'svelte/store';

const API_URL = 'http://127.0.0.1:8000';

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
}

// Made with Bob
