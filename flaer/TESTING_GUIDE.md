# Flaer Testing Guide

This guide covers how to test the Flaer application (backend API and frontend).

## Quick Start Testing

### 1. Test Backend API

#### Start the Backend Server
```bash
cd flaer/backend
python3 -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
pip install -r requirements.txt
python app.py
```

The backend should start at `http://127.0.0.1:5001`

#### Test API Endpoints

**Option A: Using curl (Command Line)**
```bash
# Health check
curl http://127.0.0.1:5001/api/health

# Portfolio data
curl http://127.0.0.1:5001/api/portfolio

# Regional pressure data
curl http://127.0.0.1:5001/api/regions

# Scenarios
curl http://127.0.0.1:5001/api/scenarios

# Recommended actions
curl http://127.0.0.1:5001/api/actions
```

**Option B: Using Browser**
Open these URLs in your browser:
- http://127.0.0.1:5001/api/health
- http://127.0.0.1:5001/api/portfolio
- http://127.0.0.1:5001/api/regions
- http://127.0.0.1:5001/api/scenarios
- http://127.0.0.1:5001/api/actions

**Option C: Using Python requests**
```python
import requests

# Test health endpoint
response = requests.get('http://127.0.0.1:5001/api/health')
print(response.json())

# Test portfolio endpoint
response = requests.get('http://127.0.0.1:5001/api/portfolio')
print(response.json())
```

### 2. Test Svelte Frontend

#### Start the Development Server
```bash
cd flaer/frontend-svelte
npm install  # First time only
npm run dev
```

The frontend should start at `http://localhost:5173` (or similar)

#### Manual Testing Checklist
- [ ] Open the local URL in your browser
- [ ] Check that the navigation menu works
- [ ] Verify the hero section displays correctly
- [ ] Test the features section
- [ ] Check the pricing cards
- [ ] Test the CTA (Call to Action) section
- [ ] Verify the footer links
- [ ] Test responsive design (resize browser window)
- [ ] Check browser console for errors (F12 → Console tab)

### 3. Test Static HTML Frontend

#### Option A: Direct File Opening
Simply open these files in your browser:
- `flaer/frontend/index.html` - Marketing website
- `flaer/frontend/dashboard.html` - Dashboard workspace

#### Option B: Local Server
```bash
cd flaer/frontend
python3 -m http.server 8080
```

Then open:
- http://127.0.0.1:8080 - Marketing website
- http://127.0.0.1:8080/dashboard.html - Dashboard

## Integration Testing

### Test Frontend-Backend Connection

1. **Start both servers:**
   - Terminal 1: Backend on port 5001
   - Terminal 2: Svelte frontend on port 5173

2. **Test API calls from frontend:**
   - Open browser DevTools (F12)
   - Go to Network tab
   - Interact with the frontend
   - Check if API calls to `http://127.0.0.1:5001/api/*` succeed
   - Verify response data in the Network tab

3. **Check CORS:**
   - Ensure no CORS errors in browser console
   - Backend has `flask-cors` enabled for cross-origin requests

## Automated Testing (Future Implementation)

### Backend Unit Tests (Recommended)

Create `flaer/backend/test_app.py`:
```python
import pytest
from app import app

@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

def test_health(client):
    response = client.get('/api/health')
    assert response.status_code == 200
    assert response.json['status'] == 'ok'

def test_portfolio(client):
    response = client.get('/api/portfolio')
    assert response.status_code == 200
    assert 'portfolio' in response.json

def test_regions(client):
    response = client.get('/api/regions')
    assert response.status_code == 200
    assert 'items' in response.json

def test_scenarios(client):
    response = client.get('/api/scenarios')
    assert response.status_code == 200
    assert 'items' in response.json

def test_actions(client):
    response = client.get('/api/actions')
    assert response.status_code == 200
    assert 'items' in response.json
```

Run tests:
```bash
pip install pytest
pytest test_app.py -v
```

### Frontend Component Tests (Recommended)

Install testing libraries:
```bash
cd flaer/frontend-svelte
npm install --save-dev @testing-library/svelte vitest jsdom
```

Create `flaer/frontend-svelte/src/lib/Navigation.test.js`:
```javascript
import { render } from '@testing-library/svelte';
import { describe, it, expect } from 'vitest';
import Navigation from './Navigation.svelte';

describe('Navigation', () => {
  it('renders navigation component', () => {
    const { container } = render(Navigation);
    expect(container).toBeTruthy();
  });
});
```

### End-to-End Tests (Advanced)

Using Playwright:
```bash
npm install --save-dev @playwright/test
npx playwright install
```

Create `flaer/frontend-svelte/tests/e2e.spec.js`:
```javascript
import { test, expect } from '@playwright/test';

test('homepage loads', async ({ page }) => {
  await page.goto('http://localhost:5173');
  await expect(page).toHaveTitle(/Flaer/);
});

test('can navigate to pricing', async ({ page }) => {
  await page.goto('http://localhost:5173');
  await page.click('text=Pricing');
  await expect(page.locator('text=Choose your plan')).toBeVisible();
});
```

## Performance Testing

### Backend Load Testing
```bash
# Install Apache Bench
# macOS: brew install httpd
# Ubuntu: apt-get install apache2-utils

# Test 1000 requests with 10 concurrent connections
ab -n 1000 -c 10 http://127.0.0.1:5001/api/health
```

### Frontend Performance
- Use Chrome DevTools Lighthouse (F12 → Lighthouse tab)
- Run audit for Performance, Accessibility, Best Practices, SEO
- Check bundle size: `npm run build` and inspect `dist/` folder

## Common Issues & Troubleshooting

### Backend Issues
- **Port already in use:** Change port in `app.py` or kill process on port 5001
- **Module not found:** Ensure virtual environment is activated and dependencies installed
- **CORS errors:** Verify `flask-cors` is installed and configured

### Frontend Issues
- **npm command not found:** Install Node.js from nodejs.org
- **Port already in use:** Vite will automatically try next available port
- **Build errors:** Delete `node_modules` and `package-lock.json`, then `npm install`

### Integration Issues
- **API calls fail:** Verify backend is running and URL is correct
- **CORS errors:** Check browser console, ensure backend CORS is enabled
- **Data not displaying:** Check Network tab in DevTools for failed requests

## Testing Checklist

### Before Deployment
- [ ] All API endpoints return expected data
- [ ] Frontend loads without console errors
- [ ] All navigation links work
- [ ] Forms submit correctly (if applicable)
- [ ] Responsive design works on mobile/tablet/desktop
- [ ] No CORS errors in production environment
- [ ] API error handling works (test with backend stopped)
- [ ] Loading states display correctly
- [ ] Performance metrics are acceptable (Lighthouse score > 90)

## Next Steps

1. **Add automated tests** for critical functionality
2. **Set up CI/CD pipeline** to run tests automatically
3. **Add monitoring** for production environment
4. **Implement error tracking** (e.g., Sentry)
5. **Add analytics** to track user behavior
6. **Create staging environment** for pre-production testing

## Resources

- Flask Testing: https://flask.palletsprojects.com/en/latest/testing/
- Svelte Testing Library: https://testing-library.com/docs/svelte-testing-library/intro/
- Vitest: https://vitest.dev/
- Playwright: https://playwright.dev/