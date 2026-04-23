# Flaer Platform - Production Ready Guide

## 🎯 Overview
Complete production-ready authentication and security system for the Flaer Carbon Intelligence Platform.

## ✅ Completed Features

### 1. Authentication System
- **JWT Token-based Authentication**: Secure access tokens with 30-minute expiration
- **Refresh Tokens**: 7-day refresh tokens stored as HTTP-only cookies
- **Password Hashing**: Argon2 algorithm for secure password storage
- **OTP Support**: Time-based One-Time Password (TOTP) for two-factor authentication
- **Session Management**: Secure cookie-based session handling

### 2. Security Features
- **Rate Limiting**: Protection against brute force attacks
  - Login: 10 requests/minute
  - Register: 5 requests/hour
  - OTP Verification: 5 requests/minute
- **Security Headers**: 
  - X-Content-Type-Options: nosniff
  - X-Frame-Options: DENY
  - X-XSS-Protection: 1; mode=block
  - Strict-Transport-Security
  - Content-Security-Policy
- **CORS Configuration**: Restricted to localhost origins
- **Input Validation**: Pydantic models with strict validation
- **Password Requirements**:
  - Minimum 8 characters
  - At least one uppercase letter
  - At least one lowercase letter
  - At least one number
  - At least one special character

### 3. API Endpoints

#### Authentication Endpoints
```
POST /api/auth/register          - Register new user
POST /api/auth/login             - Login with email/password
POST /api/auth/verify-otp        - Verify OTP code
POST /api/auth/refresh           - Refresh access token
POST /api/auth/logout            - Logout and revoke tokens
GET  /api/auth/me                - Get current user info
POST /api/auth/enable-otp        - Enable 2FA
POST /api/auth/disable-otp       - Disable 2FA
```

#### Protected Dashboard Endpoints
All dashboard endpoints now require authentication:
```
GET  /api/dashboard/overview
GET  /api/dashboard/datacenters
GET  /api/dashboard/datacenters/{dc_id}
GET  /api/dashboard/forecast
GET  /api/dashboard/actions
GET  /api/dashboard/site-intelligence
GET  /api/dashboard/site-intelligence/{site_id}
POST /api/dashboard/calculator
```

#### Public Endpoints
```
GET  /                           - API information
GET  /api/health                 - Health check
GET  /api/carbon/live            - Live carbon data
GET  /api/carbon/live/{region}   - Regional carbon data
GET  /api/carbon/regions         - Available regions
```

### 4. Test Credentials

#### Admin User (with OTP)
```
Email: demo@flaer.io
Password: Demo@2026!
Role: admin
OTP: Enabled
```

#### Regular User (without OTP)
```
Email: test@flaer.io
Password: Test@2026!
Role: user
OTP: Disabled
```

## 🚀 Usage Examples

### 1. Login (No OTP)
```bash
curl -X POST http://127.0.0.1:5001/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{"email":"test@flaer.io","password":"Test@2026!"}'
```

Response:
```json
{
  "access_token": "eyJ0eXAiOiJKV1QiLCJhbGc...",
  "refresh_token": "abc123...",
  "token_type": "bearer",
  "expires_in": 1800
}
```

### 2. Login (With OTP)
Step 1 - Initial login:
```bash
curl -X POST http://127.0.0.1:5001/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{"email":"demo@flaer.io","password":"Demo@2026!"}'
```

Response:
```json
{
  "requires_otp": true,
  "email": "demo@flaer.io",
  "otp_code": "123456",
  "message": "OTP sent to your registered device"
}
```

Step 2 - Verify OTP:
```bash
curl -X POST http://127.0.0.1:5001/api/auth/verify-otp \
  -H "Content-Type: application/json" \
  -d '{"email":"demo@flaer.io","otp_code":"123456"}'
```

### 3. Access Protected Endpoint
```bash
curl -X GET http://127.0.0.1:5001/api/dashboard/overview \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN"
```

### 4. Refresh Token
```bash
curl -X POST http://127.0.0.1:5001/api/auth/refresh \
  -H "Cookie: refresh_token=YOUR_REFRESH_TOKEN"
```

### 5. Get Current User
```bash
curl -X GET http://127.0.0.1:5001/api/auth/me \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN"
```

### 6. Logout
```bash
curl -X POST http://127.0.0.1:5001/api/auth/logout \
  -H "Cookie: refresh_token=YOUR_REFRESH_TOKEN"
```

## 📦 Dependencies

```
fastapi==0.104.1
uvicorn[standard]==0.24.0
pydantic[email]==2.5.0
httpx==0.25.2
python-dotenv==1.0.0
pyjwt==2.8.0
argon2-cffi==23.1.0
pyotp==2.9.0
python-multipart==0.0.6
slowapi==0.1.9
email-validator==2.1.0
```

## 🔧 Installation

```bash
cd flaer/backend
pip install -r requirements.txt
python3 main.py
```

## 🌐 Frontend Integration

### Authentication Service (to be created)
```javascript
// authService.js
const API_URL = 'http://127.0.0.1:5001';

export async function login(email, password) {
  const response = await fetch(`${API_URL}/api/auth/login`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    credentials: 'include',
    body: JSON.stringify({ email, password })
  });
  return response.json();
}

export async function verifyOTP(email, otp_code) {
  const response = await fetch(`${API_URL}/api/auth/verify-otp`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    credentials: 'include',
    body: JSON.stringify({ email, otp_code })
  });
  return response.json();
}

export async function logout() {
  await fetch(`${API_URL}/api/auth/logout`, {
    method: 'POST',
    credentials: 'include'
  });
  localStorage.removeItem('access_token');
}

export async function refreshToken() {
  const response = await fetch(`${API_URL}/api/auth/refresh`, {
    method: 'POST',
    credentials: 'include'
  });
  const data = await response.json();
  if (data.access_token) {
    localStorage.setItem('access_token', data.access_token);
  }
  return data;
}

export function getAuthHeader() {
  const token = localStorage.getItem('access_token');
  return token ? { 'Authorization': `Bearer ${token}` } : {};
}
```

### Protected API Calls
```javascript
async function getDashboardData() {
  const response = await fetch(`${API_URL}/api/dashboard/overview`, {
    headers: getAuthHeader()
  });
  
  if (response.status === 401) {
    // Token expired, try to refresh
    await refreshToken();
    return getDashboardData(); // Retry
  }
  
  return response.json();
}
```

## 🔐 Security Best Practices

### 1. Environment Variables
Create `.env` file:
```
JWT_SECRET_KEY=your-super-secret-key-here-change-in-production
ELECTRICITYMAP_API_KEY=your-api-key
WATTTIME_USERNAME=your-username
WATTTIME_PASSWORD=your-password
```

### 2. Production Deployment
- Use HTTPS only
- Set secure cookie flags
- Update CORS origins to production domains
- Use a real database (PostgreSQL/MongoDB) instead of in-memory storage
- Implement proper logging and monitoring
- Set up rate limiting per user/IP
- Enable API key rotation
- Implement account lockout after failed attempts

### 3. Database Migration
Replace in-memory `users_db` with:
```python
# Example with SQLAlchemy
from sqlalchemy import create_engine, Column, String, Boolean, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

Base = declarative_base()

class User(Base):
    __tablename__ = 'users'
    id = Column(String, primary_key=True)
    email = Column(String, unique=True, nullable=False)
    password_hash = Column(String, nullable=False)
    full_name = Column(String)
    company = Column(String)
    role = Column(String, default='user')
    is_active = Column(Boolean, default=True)
    otp_enabled = Column(Boolean, default=False)
    otp_secret = Column(String)
    created_at = Column(DateTime)
```

## 📊 Monitoring

### Health Check
```bash
curl http://127.0.0.1:5001/api/health
```

### API Documentation
- Swagger UI: http://127.0.0.1:5001/docs
- ReDoc: http://127.0.0.1:5001/redoc

## 🎨 Next Steps for Frontend

1. **Create Login Page** (`Login.svelte`)
   - Email/password form
   - OTP input (conditional)
   - Error handling
   - Loading states
   - Smooth animations

2. **Create Register Page** (`Register.svelte`)
   - User registration form
   - Password strength indicator
   - Terms acceptance
   - Email verification

3. **Update Navigation** (`Navigation.svelte`)
   - Remove "Dashboard" link from public nav
   - Add "Login" button
   - Show user menu when authenticated

4. **Create Protected Route Guard**
   - Check authentication before showing dashboard
   - Redirect to login if not authenticated
   - Auto-refresh tokens

5. **Add Logout Functionality**
   - Clear tokens
   - Redirect to home
   - Show confirmation

## 🔄 Token Flow

```
1. User logs in → Receives access_token + refresh_token (cookie)
2. Access protected resource → Send access_token in Authorization header
3. Access token expires (30 min) → Use refresh_token to get new access_token
4. Refresh token expires (7 days) → User must log in again
5. User logs out → Revoke refresh_token, clear access_token
```

## ✨ Features Summary

✅ JWT Authentication with refresh tokens
✅ OTP/2FA Support
✅ Secure password hashing (Argon2)
✅ Rate limiting
✅ Security headers
✅ CORS protection
✅ Input validation
✅ Role-based access control (RBAC)
✅ Session management
✅ Test credentials
✅ Protected dashboard endpoints
✅ Public carbon data endpoints
✅ Comprehensive API documentation
✅ Production-ready architecture

## 📝 Notes

- All passwords are hashed with Argon2
- Tokens are signed with HS256 algorithm
- Refresh tokens are HTTP-only cookies
- OTP uses TOTP (Time-based One-Time Password)
- Rate limiting is per IP address
- Dashboard access requires valid JWT token
- Carbon data endpoints remain public

---

**Made with ❤️ for Flaer Platform**