# Flaer Platform - Testing Guide

## 📋 Overview

Comprehensive testing suite for the Flaer Carbon Intelligence Platform, including backend API tests (pytest) and frontend E2E tests (Playwright).

## 🧪 Backend Tests (Pytest)

### Setup

```bash
cd flaer/backend
pip install -r requirements.txt
```

### Running Tests

```bash
# Run all tests
pytest tests/test_auth.py -v

# Run specific test class
pytest tests/test_auth.py::TestAuthentication -v

# Run with coverage
pytest tests/test_auth.py --cov=. --cov-report=html

# Run in parallel
pytest tests/test_auth.py -n auto
```

### Test Coverage

#### Authentication Tests
- ✅ Root endpoint returns API information
- ✅ Health check endpoint
- ✅ Login success without OTP
- ✅ Login with invalid credentials
- ✅ Login with non-existent user
- ✅ Get current user information
- ✅ Get current user with invalid token
- ✅ Get current user without token
- ✅ Logout functionality
- ✅ Token refresh
- ✅ Refresh with invalid token

#### Protected Endpoints Tests
- ✅ Dashboard overview with authentication
- ✅ Dashboard overview without authentication
- ✅ Data centers endpoint authenticated
- ✅ Forecast endpoint authenticated
- ✅ Actions endpoint authenticated
- ✅ Calculator endpoint authenticated

#### Public Endpoints Tests
- ✅ Live carbon data (no auth required)
- ✅ Carbon regions list
- ✅ Specific region carbon data

#### Password Validation Tests
- ✅ Password too short (< 8 chars)
- ✅ Password without uppercase letter
- ✅ Password without lowercase letter
- ✅ Password without number
- ✅ Password without special character

#### Security Tests
- ✅ Security headers present
- ✅ Rate limiting functionality
- ✅ OTP enable/disable
- ✅ CORS configuration

### Test Results Example

```
tests/test_auth.py::TestAuthentication::test_root_endpoint PASSED
tests/test_auth.py::TestAuthentication::test_health_check PASSED
tests/test_auth.py::TestAuthentication::test_login_success_without_otp PASSED
tests/test_auth.py::TestAuthentication::test_login_invalid_credentials PASSED
tests/test_auth.py::TestAuthentication::test_get_current_user PASSED
tests/test_auth.py::TestAuthentication::test_logout PASSED
tests/test_auth.py::TestAuthentication::test_refresh_token PASSED
tests/test_auth.py::TestProtectedEndpoints::test_dashboard_overview_authenticated PASSED
tests/test_auth.py::TestProtectedEndpoints::test_dashboard_overview_unauthenticated PASSED
tests/test_auth.py::TestPublicEndpoints::test_carbon_live_data PASSED
tests/test_auth.py::TestPasswordValidation::test_password_too_short PASSED
tests/test_auth.py::TestSecurityHeaders::test_security_headers_present PASSED
tests/test_auth.py::TestOTPFlow::test_enable_otp PASSED

========================= 30 passed in 2.45s =========================
```

## 🎭 Frontend Tests (Playwright)

### Setup

```bash
cd flaer/frontend-svelte

# Install Playwright
npm install -D @playwright/test @types/node

# Install browsers
npx playwright install
```

### Running Tests

```bash
# Run all tests
npx playwright test

# Run in headed mode (see browser)
npx playwright test --headed

# Run specific test file
npx playwright test tests/auth.spec.ts

# Run in debug mode
npx playwright test --debug

# Run with UI mode
npx playwright test --ui

# Generate test report
npx playwright show-report
```

### Test Coverage

#### Authentication Flow
- ✅ Display login page
- ✅ Login successfully with valid credentials
- ✅ Show error with invalid credentials
- ✅ Validate email format
- ✅ Require password
- ✅ Logout successfully

#### Protected Routes
- ✅ Redirect to login when accessing dashboard without auth
- ✅ Access dashboard with valid token
- ✅ Maintain session after page reload

#### Token Refresh
- ✅ Refresh token automatically when expired

#### Registration
- ✅ Display registration page
- ✅ Validate password requirements
- ✅ Show password strength indicator

#### Navigation
- ✅ Hide dashboard link when not authenticated
- ✅ Show dashboard link when authenticated

#### API Integration
- ✅ Make authenticated API calls
- ✅ Handle 401 unauthorized responses

#### Security
- ✅ Not expose sensitive data in localStorage
- ✅ Use HTTPS in production

### Test Configuration

The `playwright.config.ts` file configures:
- Test directory: `./tests`
- Base URL: `http://localhost:5173`
- Browsers: Chromium, Firefox, WebKit
- Screenshots on failure
- Trace on first retry
- Automatic dev server startup

## 🔍 Manual Testing Checklist

### Authentication Flow
- [ ] Register new user with valid data
- [ ] Register with weak password (should fail)
- [ ] Login with correct credentials
- [ ] Login with incorrect credentials (should fail)
- [ ] Enable OTP for account
- [ ] Login with OTP enabled
- [ ] Verify OTP code
- [ ] Disable OTP
- [ ] Logout

### Dashboard Access
- [ ] Access dashboard without login (should redirect)
- [ ] Access dashboard with valid token
- [ ] Token expires after 30 minutes
- [ ] Refresh token works
- [ ] Logout clears tokens

### API Endpoints
- [ ] Public endpoints work without auth
- [ ] Protected endpoints require auth
- [ ] Invalid token returns 401
- [ ] Expired token triggers refresh

### Security
- [ ] Security headers present
- [ ] Rate limiting works
- [ ] CORS configured correctly
- [ ] Passwords are hashed
- [ ] Tokens are signed
- [ ] Refresh tokens are HTTP-only cookies

## 📊 Test Data

### Test Users

```javascript
// Regular user (no OTP)
{
  email: "test@flaer.io",
  password: "Test@2026!",
  role: "user"
}

// Admin user (with OTP)
{
  email: "demo@flaer.io",
  password: "Demo@2026!",
  role: "admin",
  otp_enabled: true
}
```

### API Endpoints

```
# Public
GET  /                           - API info
GET  /api/health                 - Health check
GET  /api/carbon/live            - Live carbon data
GET  /api/carbon/regions         - Available regions

# Authentication
POST /api/auth/register          - Register
POST /api/auth/login             - Login
POST /api/auth/verify-otp        - Verify OTP
POST /api/auth/refresh           - Refresh token
POST /api/auth/logout            - Logout
GET  /api/auth/me                - Current user

# Protected
GET  /api/dashboard/overview     - Dashboard data
GET  /api/dashboard/datacenters  - Data centers
GET  /api/dashboard/forecast     - Forecast
GET  /api/dashboard/actions      - Actions
POST /api/dashboard/calculator   - Calculator
```

## 🐛 Debugging Tests

### Backend Tests

```bash
# Run with verbose output
pytest tests/test_auth.py -vv

# Run with print statements
pytest tests/test_auth.py -s

# Run specific test
pytest tests/test_auth.py::TestAuthentication::test_login_success_without_otp -v

# Stop on first failure
pytest tests/test_auth.py -x

# Show local variables on failure
pytest tests/test_auth.py -l
```

### Frontend Tests

```bash
# Debug mode (step through tests)
npx playwright test --debug

# Headed mode (see browser)
npx playwright test --headed

# Slow motion
npx playwright test --headed --slow-mo=1000

# Specific browser
npx playwright test --project=chromium

# Generate trace
npx playwright test --trace on

# View trace
npx playwright show-trace trace.zip
```

## 📈 Continuous Integration

### GitHub Actions Example

```yaml
name: Tests

on: [push, pull_request]

jobs:
  backend-tests:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - uses: actions/setup-python@v4
        with:
          python-version: '3.11'
      - name: Install dependencies
        run: |
          cd flaer/backend
          pip install -r requirements.txt
      - name: Run tests
        run: |
          cd flaer/backend
          pytest tests/test_auth.py -v

  frontend-tests:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - uses: actions/setup-node@v3
        with:
          node-version: '18'
      - name: Install dependencies
        run: |
          cd flaer/frontend-svelte
          npm ci
      - name: Install Playwright
        run: |
          cd flaer/frontend-svelte
          npx playwright install --with-deps
      - name: Run tests
        run: |
          cd flaer/frontend-svelte
          npx playwright test
      - uses: actions/upload-artifact@v3
        if: always()
        with:
          name: playwright-report
          path: flaer/frontend-svelte/playwright-report/
```

## 🎯 Test Best Practices

### Backend Tests
1. Use fixtures for common setup
2. Test both success and failure cases
3. Verify response status codes
4. Check response data structure
5. Test edge cases
6. Mock external dependencies
7. Use descriptive test names

### Frontend Tests
1. Use data-testid attributes
2. Wait for elements properly
3. Test user interactions
4. Verify navigation
5. Check error messages
6. Test responsive design
7. Use page object pattern

## 📝 Adding New Tests

### Backend Test Template

```python
class TestNewFeature:
    """Test new feature"""
    
    def test_feature_success(self):
        """Test successful feature operation"""
        response = client.post("/api/new-endpoint", json={...})
        assert response.status_code == 200
        assert "expected_key" in response.json()
    
    def test_feature_failure(self):
        """Test feature with invalid input"""
        response = client.post("/api/new-endpoint", json={...})
        assert response.status_code == 400
```

### Frontend Test Template

```typescript
test.describe('New Feature', () => {
  test('should perform action', async ({ page }) => {
    await page.goto('/feature');
    await page.click('[data-testid="action-button"]');
    await expect(page.locator('.result')).toBeVisible();
  });
});
```

## 🔧 Troubleshooting

### Common Issues

**Backend tests fail with "Connection refused"**
- Ensure backend server is not running
- Tests use TestClient which doesn't need server

**Frontend tests timeout**
- Increase timeout in playwright.config.ts
- Check if dev server starts correctly
- Verify BASE_URL is correct

**Rate limiting affects tests**
- Tests might trigger rate limits
- Use separate test database
- Reset rate limits between tests

**OTP tests fail**
- OTP codes are time-based
- Ensure system time is correct
- Use mock time in tests

## 📚 Resources

- [Pytest Documentation](https://docs.pytest.org/)
- [Playwright Documentation](https://playwright.dev/)
- [FastAPI Testing](https://fastapi.tiangolo.com/tutorial/testing/)
- [Svelte Testing](https://svelte.dev/docs/testing)

---

**Test Coverage Goal**: 80%+ for critical paths
**Test Execution Time**: < 5 minutes for full suite
**CI/CD Integration**: Required for all PRs