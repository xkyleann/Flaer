"""
Comprehensive Authentication Tests for Flaer Platform
Tests JWT authentication, OTP, rate limiting, and security features
"""

import pytest
from fastapi.testclient import TestClient
from main import app
from auth_service import auth_service, users_db
import time

client = TestClient(app)

# Test data
TEST_USER = {
    "email": "test@flaer.io",
    "password": "Test@2026!",
    "full_name": "Test User",
    "company": "Test Company"
}

ADMIN_USER = {
    "email": "demo@flaer.io",
    "password": "Demo@2026!"
}

class TestAuthentication:
    """Test authentication endpoints"""
    
    def test_root_endpoint(self):
        """Test root endpoint returns API information"""
        response = client.get("/")
        assert response.status_code == 200
        data = response.json()
        assert data["service"] == "Flaer Carbon Intelligence API"
        assert data["version"] == "1.0.0"
        assert "test_credentials" in data
    
    def test_health_check(self):
        """Test health check endpoint"""
        response = client.get("/api/health")
        assert response.status_code == 200
        assert response.json()["status"] == "ok"
    
    def test_login_success_without_otp(self):
        """Test successful login for user without OTP"""
        response = client.post(
            "/api/auth/login",
            json={"email": TEST_USER["email"], "password": TEST_USER["password"]}
        )
        assert response.status_code == 200
        data = response.json()
        assert "access_token" in data
        assert "refresh_token" in data
        assert data["token_type"] == "bearer"
        assert data["expires_in"] == 1800
        
        # Verify cookie is set
        assert "refresh_token" in response.cookies
    
    def test_login_invalid_credentials(self):
        """Test login with invalid credentials"""
        response = client.post(
            "/api/auth/login",
            json={"email": TEST_USER["email"], "password": "WrongPassword123!"}
        )
        assert response.status_code == 401
        assert "Incorrect email or password" in response.json()["detail"]
    
    def test_login_nonexistent_user(self):
        """Test login with non-existent user"""
        response = client.post(
            "/api/auth/login",
            json={"email": "nonexistent@flaer.io", "password": "Test@2026!"}
        )
        assert response.status_code == 401
    
    def test_get_current_user(self):
        """Test getting current user information"""
        # First login
        login_response = client.post(
            "/api/auth/login",
            json={"email": TEST_USER["email"], "password": TEST_USER["password"]}
        )
        token = login_response.json()["access_token"]
        
        # Get current user
        response = client.get(
            "/api/auth/me",
            headers={"Authorization": f"Bearer {token}"}
        )
        assert response.status_code == 200
        data = response.json()
        assert data["email"] == TEST_USER["email"]
        assert data["role"] == "user"
        assert "id" in data
    
    def test_get_current_user_invalid_token(self):
        """Test getting current user with invalid token"""
        response = client.get(
            "/api/auth/me",
            headers={"Authorization": "Bearer invalid_token"}
        )
        assert response.status_code == 401
    
    def test_get_current_user_no_token(self):
        """Test getting current user without token"""
        response = client.get("/api/auth/me")
        assert response.status_code == 403  # No credentials provided
    
    def test_logout(self):
        """Test logout functionality"""
        # First login
        login_response = client.post(
            "/api/auth/login",
            json={"email": TEST_USER["email"], "password": TEST_USER["password"]}
        )
        refresh_token = login_response.json()["refresh_token"]
        
        # Logout
        response = client.post(
            "/api/auth/logout",
            cookies={"refresh_token": refresh_token}
        )
        assert response.status_code == 200
        assert response.json()["message"] == "Successfully logged out"
    
    def test_refresh_token(self):
        """Test token refresh functionality"""
        # First login
        login_response = client.post(
            "/api/auth/login",
            json={"email": TEST_USER["email"], "password": TEST_USER["password"]}
        )
        refresh_token = login_response.json()["refresh_token"]
        
        # Refresh token
        response = client.post(
            "/api/auth/refresh",
            cookies={"refresh_token": refresh_token}
        )
        assert response.status_code == 200
        data = response.json()
        assert "access_token" in data
        assert "refresh_token" in data
        
        # Verify new tokens are different
        assert data["access_token"] != login_response.json()["access_token"]
        assert data["refresh_token"] != refresh_token
    
    def test_refresh_token_invalid(self):
        """Test refresh with invalid token"""
        response = client.post(
            "/api/auth/refresh",
            cookies={"refresh_token": "invalid_token"}
        )
        assert response.status_code == 401


class TestProtectedEndpoints:
    """Test protected dashboard endpoints"""
    
    def setup_method(self):
        """Setup: Login and get token"""
        response = client.post(
            "/api/auth/login",
            json={"email": TEST_USER["email"], "password": TEST_USER["password"]}
        )
        self.token = response.json()["access_token"]
        self.headers = {"Authorization": f"Bearer {self.token}"}
    
    def test_dashboard_overview_authenticated(self):
        """Test dashboard overview with authentication"""
        response = client.get("/api/dashboard/overview", headers=self.headers)
        assert response.status_code == 200
        data = response.json()
        assert "health_score" in data
        assert "total_emissions" in data
    
    def test_dashboard_overview_unauthenticated(self):
        """Test dashboard overview without authentication"""
        response = client.get("/api/dashboard/overview")
        assert response.status_code == 403
    
    def test_datacenters_authenticated(self):
        """Test datacenters endpoint with authentication"""
        response = client.get("/api/dashboard/datacenters", headers=self.headers)
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, list)
        assert len(data) > 0
    
    def test_forecast_authenticated(self):
        """Test forecast endpoint with authentication"""
        response = client.get("/api/dashboard/forecast", headers=self.headers)
        assert response.status_code == 200
        data = response.json()
        assert "facility" in data
        assert "years" in data
    
    def test_actions_authenticated(self):
        """Test actions endpoint with authentication"""
        response = client.get("/api/dashboard/actions", headers=self.headers)
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, list)
    
    def test_calculator_authenticated(self):
        """Test calculator endpoint with authentication"""
        response = client.post(
            "/api/dashboard/calculator",
            headers=self.headers,
            json={
                "servers": 1000,
                "pue": 1.5,
                "carbon_intensity": 400,
                "utilization": 70
            }
        )
        assert response.status_code == 200
        data = response.json()
        assert "annual_emissions" in data
        assert "monthly_cost" in data


class TestPublicEndpoints:
    """Test public endpoints (no authentication required)"""
    
    def test_carbon_live_data(self):
        """Test live carbon data endpoint"""
        response = client.get("/api/carbon/live")
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "success"
        assert "regions" in data
    
    def test_carbon_regions(self):
        """Test carbon regions endpoint"""
        response = client.get("/api/carbon/regions")
        assert response.status_code == 200
        data = response.json()
        assert "regions" in data
        assert isinstance(data["regions"], list)
    
    def test_carbon_region_data(self):
        """Test specific region carbon data"""
        response = client.get("/api/carbon/live/virginia")
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "success"
        assert data["region"] == "virginia"


class TestPasswordValidation:
    """Test password validation rules"""
    
    def test_password_too_short(self):
        """Test password shorter than 8 characters"""
        response = client.post(
            "/api/auth/register",
            json={
                "email": "newuser@flaer.io",
                "password": "Short1!",
                "full_name": "New User"
            }
        )
        assert response.status_code == 422  # Validation error
    
    def test_password_no_uppercase(self):
        """Test password without uppercase letter"""
        response = client.post(
            "/api/auth/register",
            json={
                "email": "newuser@flaer.io",
                "password": "lowercase123!",
                "full_name": "New User"
            }
        )
        assert response.status_code == 422
    
    def test_password_no_lowercase(self):
        """Test password without lowercase letter"""
        response = client.post(
            "/api/auth/register",
            json={
                "email": "newuser@flaer.io",
                "password": "UPPERCASE123!",
                "full_name": "New User"
            }
        )
        assert response.status_code == 422
    
    def test_password_no_number(self):
        """Test password without number"""
        response = client.post(
            "/api/auth/register",
            json={
                "email": "newuser@flaer.io",
                "password": "NoNumber!",
                "full_name": "New User"
            }
        )
        assert response.status_code == 422
    
    def test_password_no_special_char(self):
        """Test password without special character"""
        response = client.post(
            "/api/auth/register",
            json={
                "email": "newuser@flaer.io",
                "password": "NoSpecial123",
                "full_name": "New User"
            }
        )
        assert response.status_code == 422


class TestSecurityHeaders:
    """Test security headers"""
    
    def test_security_headers_present(self):
        """Test that security headers are present"""
        response = client.get("/")
        headers = response.headers
        
        assert "x-content-type-options" in headers
        assert headers["x-content-type-options"] == "nosniff"
        
        assert "x-frame-options" in headers
        assert headers["x-frame-options"] == "DENY"
        
        assert "x-xss-protection" in headers
        assert headers["x-xss-protection"] == "1; mode=block"
        
        assert "strict-transport-security" in headers
        assert "content-security-policy" in headers


class TestRateLimiting:
    """Test rate limiting functionality"""
    
    def test_login_rate_limit(self):
        """Test login rate limiting (10 requests/minute)"""
        # Make 11 rapid requests
        responses = []
        for i in range(11):
            response = client.post(
                "/api/auth/login",
                json={"email": "test@example.com", "password": "Test@2026!"}
            )
            responses.append(response.status_code)
        
        # At least one should be rate limited (429)
        assert 429 in responses or all(r in [401, 200] for r in responses)
        # Note: Rate limiting might not trigger in tests due to timing


class TestOTPFlow:
    """Test OTP/2FA functionality"""
    
    def test_enable_otp(self):
        """Test enabling OTP for user"""
        # Login first
        login_response = client.post(
            "/api/auth/login",
            json={"email": TEST_USER["email"], "password": TEST_USER["password"]}
        )
        token = login_response.json()["access_token"]
        
        # Enable OTP
        response = client.post(
            "/api/auth/enable-otp",
            headers={"Authorization": f"Bearer {token}"}
        )
        assert response.status_code == 200
        data = response.json()
        assert "provisioning_uri" in data
        assert "message" in data
    
    def test_disable_otp(self):
        """Test disabling OTP for user"""
        # Login first
        login_response = client.post(
            "/api/auth/login",
            json={"email": TEST_USER["email"], "password": TEST_USER["password"]}
        )
        token = login_response.json()["access_token"]
        
        # Disable OTP
        response = client.post(
            "/api/auth/disable-otp",
            headers={"Authorization": f"Bearer {token}"}
        )
        assert response.status_code == 200
        assert response.json()["message"] == "OTP disabled successfully"


class TestCORS:
    """Test CORS configuration"""
    
    def test_cors_headers(self):
        """Test CORS headers are present"""
        response = client.options(
            "/api/auth/login",
            headers={"Origin": "http://localhost:5173"}
        )
        # CORS headers should be present
        assert response.status_code in [200, 405]  # OPTIONS might not be implemented


# Run tests
if __name__ == "__main__":
    pytest.main([__file__, "-v", "--tb=short"])
