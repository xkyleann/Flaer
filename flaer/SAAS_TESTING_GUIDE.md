# Flaer SaaS Testing Guide

## Quick Test Setup

### 1. Install Dependencies

```bash
cd flaer/backend

# Create virtual environment
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install all dependencies
pip install -r requirements.txt
```

### 2. Set Up Test Environment

```bash
# Copy environment template
cp .env.example .env

# Edit .env - use SQLite for testing
nano .env
```

Minimal `.env` for testing:
```env
DATABASE_URL=sqlite:///./test_flaer.db
JWT_SECRET_KEY=test-secret-key-change-in-production
STRIPE_SECRET_KEY=sk_test_dummy
FRONTEND_URL=http://localhost:5173
```

### 3. Initialize Database

```bash
# Run Python to initialize database
python3 << EOF
from database import init_db
init_db()
print("✅ Database initialized successfully!")
EOF
```

## Testing Methods

### Method 1: Quick Manual Test (Recommended for Start)

#### Step 1: Start the Backend

```bash
cd flaer/backend
source venv/bin/activate
uvicorn main:app --reload --port 5001
```

You should see:
```
INFO:     Uvicorn running on http://127.0.0.1:5001
INFO:     Application startup complete.
```

#### Step 2: Test API Endpoints

Open a new terminal and test with curl:

```bash
# Test health endpoint
curl http://localhost:5001/api/health

# Expected response:
# {"status":"ok","service":"flaer-api"}

# Test root endpoint
curl http://localhost:5001/

# Should return API information with endpoints list
```

#### Step 3: Test Authentication

```bash
# Register a new user
curl -X POST http://localhost:5001/api/auth/register \
  -H "Content-Type: application/json" \
  -d '{
    "email": "test@example.com",
    "password": "Test@2026!",
    "full_name": "Test User"
  }'

# Expected: Returns access_token and refresh_token

# Login
curl -X POST http://localhost:5001/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{
    "email": "test@flaer.io",
    "password": "Test@2026!"
  }'

# Save the access_token from response
```

#### Step 4: Test Protected Endpoints

```bash
# Replace YOUR_TOKEN with the access_token from login
TOKEN="your_access_token_here"

# Get dashboard overview
curl http://localhost:5001/api/dashboard/overview \
  -H "Authorization: Bearer $TOKEN"

# Get data centers
curl http://localhost:5001/api/dashboard/datacenters \
  -H "Authorization: Bearer $TOKEN"
```

#### Step 5: Test Frontend

```bash
# In a new terminal
cd flaer/frontend-svelte
npm install
npm run dev
```

Visit: http://localhost:5173

Test the following:
- [ ] Homepage loads
- [ ] Pricing page displays correctly
- [ ] Login form works
- [ ] Dashboard loads after login

### Method 2: Automated Testing with Pytest

```bash
cd flaer/backend
source venv/bin/activate

# Run all tests
pytest tests/ -v

# Run specific test file
pytest tests/test_auth.py -v

# Run with coverage
pytest tests/ --cov=. --cov-report=html

# View coverage report
open htmlcov/index.html  # On Mac
# or
xdg-open htmlcov/index.html  # On Linux
```

### Method 3: Interactive API Testing (Swagger UI)

1. Start the backend server
2. Open browser: http://localhost:5001/docs
3. You'll see interactive API documentation
4. Click "Try it out" on any endpoint to test

**Test Flow:**
1. POST `/api/auth/login` - Get access token
2. Click "Authorize" button at top
3. Enter: `Bearer your_access_token`
4. Now test any protected endpoint

### Method 4: Test with Postman/Insomnia

#### Import Collection

Create a new collection with these requests:

**1. Register User**
```
POST http://localhost:5001/api/auth/register
Content-Type: application/json

{
  "email": "newuser@example.com",
  "password": "SecurePass123!",
  "full_name": "New User",
  "company": "Test Company"
}
```

**2. Login**
```
POST http://localhost:5001/api/auth/login
Content-Type: application/json

{
  "email": "test@flaer.io",
  "password": "Test@2026!"
}
```

**3. Get Current User**
```
GET http://localhost:5001/api/auth/me
Authorization: Bearer {{access_token}}
```

**4. Get Dashboard**
```
GET http://localhost:5001/api/dashboard/overview
Authorization: Bearer {{access_token}}
```

## Testing SaaS Features

### Test Database Models

```bash
cd flaer/backend
python3
```

```python
from database import SessionLocal, init_db
from models import Organization, User, DataCenter
from datetime import datetime, timezone

# Initialize database
init_db()

# Create session
db = SessionLocal()

# Create test organization
org = Organization(
    name="Test Company",
    slug="test-company",
    plan_tier="starter",
    subscription_status="active"
)
db.add(org)
db.commit()

# Create test user
from auth_service import AuthService
user = User(
    email="testuser@example.com",
    password_hash=AuthService.get_password_hash("Test@2026!"),
    full_name="Test User",
    organization_id=org.id,
    role="owner"
)
db.add(user)
db.commit()

# Create test data center
dc = DataCenter(
    organization_id=org.id,
    name="Test DC",
    location="US East",
    carbon_intensity=350.0,
    capacity_mw=100,
    pue=1.3,
    renewable_pct=50
)
db.add(dc)
db.commit()

print(f"✅ Created organization: {org.name}")
print(f"✅ Created user: {user.email}")
print(f"✅ Created data center: {dc.name}")

# Query test
orgs = db.query(Organization).all()
print(f"\n📊 Total organizations: {len(orgs)}")

db.close()
```

### Test Billing Service

```python
from billing_service import billing_service

# Get pricing tiers
tiers = billing_service.get_pricing_tiers()
print("Pricing Tiers:", tiers.keys())

# Get tier limits
starter_limits = billing_service.get_tier_limits("starter")
print("Starter Limits:", starter_limits)

# Calculate trial end
trial_end = billing_service.calculate_trial_end()
print(f"Trial ends at: {trial_end}")
```

### Test Usage Service

```python
from usage_service import usage_service

# Mock organization data
org = {
    "plan_tier": "starter",
    "data_centers_count": 5,
    "users_count": 3,
    "api_calls_count": 5000
}

# Check limits
can_add_dc = usage_service.check_data_center_limit(org)
can_add_user = usage_service.check_user_limit(org)
can_make_api_call = usage_service.check_api_limit(org, 5000)

print(f"Can add data center: {can_add_dc}")
print(f"Can add user: {can_add_user}")
print(f"Can make API call: {can_make_api_call}")

# Get limits info
limits = usage_service.get_limits_info(org)
print("Limits Info:", limits)
```

## Testing Stripe Integration

### Test Mode Setup

1. Go to https://dashboard.stripe.com/test/apikeys
2. Get your test API keys
3. Update `.env`:
```env
STRIPE_SECRET_KEY=sk_test_your_key_here
```

### Test Checkout Flow

```python
from billing_service import billing_service

# Create test customer
customer_id = billing_service.create_customer(
    email="test@example.com",
    name="Test User",
    organization_id="org_123"
)
print(f"Customer ID: {customer_id}")

# Create checkout session (requires valid price_id)
session = billing_service.create_checkout_session(
    customer_id=customer_id,
    price_id="price_test_123",  # Replace with real test price ID
    organization_id="org_123",
    success_url="http://localhost:5173/success",
    cancel_url="http://localhost:5173/cancel"
)
print(f"Checkout URL: {session['url']}")
```

### Test Webhooks Locally

```bash
# Install Stripe CLI
# Mac: brew install stripe/stripe-cli/stripe
# Linux: Download from https://github.com/stripe/stripe-cli/releases

# Login to Stripe
stripe login

# Forward webhooks to local server
stripe listen --forward-to localhost:5001/api/billing/webhook

# In another terminal, trigger test events
stripe trigger checkout.session.completed
stripe trigger customer.subscription.updated
stripe trigger invoice.payment_succeeded
```

## Frontend Testing

### Test Pricing Page

```bash
cd flaer/frontend-svelte
npm run dev
```

Visit: http://localhost:5173

**Manual Tests:**
- [ ] All 4 pricing tiers display correctly
- [ ] Hover effects work on cards
- [ ] "Most Popular" badge shows on Starter plan
- [ ] CTA buttons are clickable
- [ ] Responsive design works (resize browser)
- [ ] Mobile view looks good (< 768px width)

### Test with Playwright (E2E)

```bash
cd flaer/frontend-svelte

# Install Playwright
npm install -D @playwright/test
npx playwright install

# Run tests
npm test
```

## Performance Testing

### Load Test with Apache Bench

```bash
# Install Apache Bench
# Mac: brew install httpd
# Ubuntu: sudo apt-get install apache2-utils

# Test health endpoint (100 requests, 10 concurrent)
ab -n 100 -c 10 http://localhost:5001/api/health

# Test with authentication
ab -n 100 -c 10 -H "Authorization: Bearer YOUR_TOKEN" \
  http://localhost:5001/api/dashboard/overview
```

### Load Test with Locust

```bash
pip install locust

# Create locustfile.py
cat > locustfile.py << 'EOF'
from locust import HttpUser, task, between

class FlaerUser(HttpUser):
    wait_time = between(1, 3)
    
    def on_start(self):
        # Login
        response = self.client.post("/api/auth/login", json={
            "email": "test@flaer.io",
            "password": "Test@2026!"
        })
        self.token = response.json()["access_token"]
    
    @task
    def get_dashboard(self):
        self.client.get("/api/dashboard/overview",
            headers={"Authorization": f"Bearer {self.token}"})
    
    @task
    def get_datacenters(self):
        self.client.get("/api/dashboard/datacenters",
            headers={"Authorization": f"Bearer {self.token}"})
EOF

# Run load test
locust -f locustfile.py --host=http://localhost:5001
```

Visit: http://localhost:8089 to control the test

## Troubleshooting

### Database Issues

```bash
# Reset database
rm test_flaer.db
python3 -c "from database import init_db; init_db()"
```

### Import Errors

```bash
# Reinstall dependencies
pip install -r requirements.txt --force-reinstall
```

### Port Already in Use

```bash
# Find process using port 5001
lsof -i :5001

# Kill process
kill -9 <PID>
```

### Stripe Test Cards

Use these test cards in Stripe checkout:
- **Success**: 4242 4242 4242 4242
- **Decline**: 4000 0000 0000 0002
- **3D Secure**: 4000 0025 0000 3155

Any future date, any CVC, any ZIP code.

## Test Checklist

### Backend
- [ ] Server starts without errors
- [ ] Health endpoint responds
- [ ] User registration works
- [ ] User login works
- [ ] Protected endpoints require auth
- [ ] Database models create correctly
- [ ] Billing service initializes
- [ ] Usage tracking works

### Frontend
- [ ] Development server starts
- [ ] Homepage loads
- [ ] Pricing page displays
- [ ] Login form works
- [ ] Dashboard loads
- [ ] Responsive design works

### Integration
- [ ] Frontend can call backend API
- [ ] Authentication flow works end-to-end
- [ ] CORS is configured correctly
- [ ] Error handling works

### SaaS Features
- [ ] Organizations can be created
- [ ] Users belong to organizations
- [ ] Usage limits are enforced
- [ ] Pricing tiers are correct
- [ ] Stripe integration works (test mode)

## Next Steps

1. ✅ Complete basic testing
2. Set up CI/CD pipeline
3. Add more automated tests
4. Test in staging environment
5. Perform security audit
6. Load test with expected traffic
7. Deploy to production

---

**Need help?** Check `SAAS_SETUP.md` for setup instructions or `SAAS_IMPLEMENTATION_GUIDE.md` for detailed implementation details.