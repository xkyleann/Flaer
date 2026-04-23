# Flaer SaaS Implementation Guide

## Overview
Transform Flaer from a demo application into a production-ready SaaS platform for carbon intelligence and data center monitoring.

---

## 1. Multi-Tenancy Architecture

### Database Schema Changes
```sql
-- Add organizations/tenants table
CREATE TABLE organizations (
    id UUID PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    slug VARCHAR(100) UNIQUE NOT NULL,
    plan_tier VARCHAR(50) NOT NULL, -- free, starter, professional, enterprise
    created_at TIMESTAMP DEFAULT NOW(),
    subscription_status VARCHAR(50), -- trial, active, suspended, cancelled
    trial_ends_at TIMESTAMP,
    max_data_centers INT,
    max_users INT
);

-- Update users table
ALTER TABLE users ADD COLUMN organization_id UUID REFERENCES organizations(id);
ALTER TABLE users ADD COLUMN role VARCHAR(50); -- owner, admin, member, viewer

-- Add data centers table (currently in-memory)
CREATE TABLE data_centers (
    id UUID PRIMARY KEY,
    organization_id UUID REFERENCES organizations(id),
    name VARCHAR(255) NOT NULL,
    location VARCHAR(255),
    carbon_intensity FLOAT,
    capacity_mw INT,
    pue FLOAT,
    renewable_pct INT,
    created_at TIMESTAMP DEFAULT NOW()
);

-- Add usage tracking
CREATE TABLE api_usage (
    id UUID PRIMARY KEY,
    organization_id UUID REFERENCES organizations(id),
    endpoint VARCHAR(255),
    timestamp TIMESTAMP DEFAULT NOW(),
    response_time_ms INT
);
```

### Implementation Steps
1. **Replace in-memory storage** with PostgreSQL/MySQL
2. **Add organization context** to all API endpoints
3. **Implement data isolation** - users only see their org's data
4. **Add organization switching** for users in multiple orgs

---

## 2. Subscription & Billing System

### Pricing Tiers
```python
PRICING_TIERS = {
    "free": {
        "price": 0,
        "max_data_centers": 3,
        "max_users": 2,
        "api_calls_per_month": 1000,
        "features": ["basic_monitoring", "carbon_calculator"]
    },
    "starter": {
        "price": 49,  # USD/month
        "max_data_centers": 10,
        "max_users": 5,
        "api_calls_per_month": 10000,
        "features": ["basic_monitoring", "carbon_calculator", "forecasting", "email_alerts"]
    },
    "professional": {
        "price": 199,
        "max_data_centers": 50,
        "max_users": 20,
        "api_calls_per_month": 100000,
        "features": ["all_features", "priority_support", "custom_reports", "api_access"]
    },
    "enterprise": {
        "price": "custom",
        "max_data_centers": "unlimited",
        "max_users": "unlimited",
        "api_calls_per_month": "unlimited",
        "features": ["all_features", "dedicated_support", "sla", "white_label", "on_premise"]
    }
}
```

### Integration Options
1. **Stripe** (Recommended)
   - Easy integration
   - Handles subscriptions, invoicing, tax
   - Webhook support for events
   
2. **Paddle**
   - Merchant of record
   - Handles VAT/tax compliance
   - Good for global sales

### Implementation
```python
# backend/billing_service.py
import stripe
from datetime import datetime, timedelta

stripe.api_key = os.getenv("STRIPE_SECRET_KEY")

class BillingService:
    @staticmethod
    def create_checkout_session(organization_id: str, plan: str):
        """Create Stripe checkout session"""
        session = stripe.checkout.Session.create(
            customer_email=user.email,
            payment_method_types=['card'],
            line_items=[{
                'price': STRIPE_PRICE_IDS[plan],
                'quantity': 1,
            }],
            mode='subscription',
            success_url=f'{FRONTEND_URL}/billing/success',
            cancel_url=f'{FRONTEND_URL}/billing/cancel',
            metadata={'organization_id': organization_id}
        )
        return session
    
    @staticmethod
    def handle_webhook(payload, sig_header):
        """Handle Stripe webhooks"""
        event = stripe.Webhook.construct_event(
            payload, sig_header, STRIPE_WEBHOOK_SECRET
        )
        
        if event['type'] == 'checkout.session.completed':
            # Activate subscription
            pass
        elif event['type'] == 'invoice.payment_failed':
            # Suspend account
            pass
```

---

## 3. Database Migration

### Choose Database
- **PostgreSQL** (Recommended) - Best for complex queries, JSON support
- **MySQL** - Good alternative, wide support
- **MongoDB** - If you prefer NoSQL

### Setup with SQLAlchemy
```python
# backend/database.py
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://user:pass@localhost/flaer")

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
```

### Models
```python
# backend/models.py
from sqlalchemy import Column, String, Integer, Float, DateTime, ForeignKey, Boolean
from sqlalchemy.orm import relationship
from database import Base
import uuid

class Organization(Base):
    __tablename__ = "organizations"
    
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    name = Column(String, nullable=False)
    slug = Column(String, unique=True, nullable=False)
    plan_tier = Column(String, default="free")
    subscription_status = Column(String, default="trial")
    created_at = Column(DateTime, default=datetime.utcnow)
    
    users = relationship("User", back_populates="organization")
    data_centers = relationship("DataCenter", back_populates="organization")

class User(Base):
    __tablename__ = "users"
    
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    email = Column(String, unique=True, nullable=False)
    password_hash = Column(String, nullable=False)
    organization_id = Column(String, ForeignKey("organizations.id"))
    role = Column(String, default="member")
    
    organization = relationship("Organization", back_populates="users")

class DataCenter(Base):
    __tablename__ = "data_centers"
    
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    organization_id = Column(String, ForeignKey("organizations.id"))
    name = Column(String, nullable=False)
    location = Column(String)
    carbon_intensity = Column(Float)
    capacity_mw = Column(Integer)
    pue = Column(Float)
    
    organization = relationship("Organization", back_populates="data_centers")
```

---

## 4. Infrastructure & Deployment

### Cloud Providers (Choose One)

#### Option A: AWS
```yaml
# Recommended AWS Services
- EC2/ECS: Application hosting
- RDS: PostgreSQL database
- S3: File storage
- CloudFront: CDN
- Route53: DNS
- SES: Email service
- CloudWatch: Monitoring

# Estimated Monthly Cost
- Small: $100-200 (t3.small, db.t3.micro)
- Medium: $500-800 (t3.medium, db.t3.small)
- Large: $2000+ (t3.large+, db.m5.large)
```

#### Option B: DigitalOcean (Easier, Cheaper)
```yaml
# Recommended Services
- App Platform: $12-48/month
- Managed PostgreSQL: $15-60/month
- Spaces (S3): $5/month
- CDN: Included

# Total: ~$50-150/month for starter
```

#### Option C: Vercel + Supabase (Fastest Setup)
```yaml
# Vercel (Frontend)
- Free tier available
- Pro: $20/month

# Supabase (Backend + DB)
- Free tier: 500MB database
- Pro: $25/month
- Includes: PostgreSQL, Auth, Storage, Realtime

# Total: $0-45/month to start
```

### Docker Setup
```dockerfile
# Dockerfile
FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
```

```yaml
# docker-compose.yml
version: '3.8'

services:
  backend:
    build: ./backend
    ports:
      - "8000:8000"
    environment:
      - DATABASE_URL=postgresql://user:pass@db:5432/flaer
      - STRIPE_SECRET_KEY=${STRIPE_SECRET_KEY}
    depends_on:
      - db
  
  frontend:
    build: ./frontend-svelte
    ports:
      - "3000:3000"
    environment:
      - VITE_API_URL=http://backend:8000
  
  db:
    image: postgres:15
    environment:
      - POSTGRES_DB=flaer
      - POSTGRES_USER=user
      - POSTGRES_PASSWORD=pass
    volumes:
      - postgres_data:/var/lib/postgresql/data

volumes:
  postgres_data:
```

---

## 5. Essential SaaS Features

### A. User Onboarding
```python
# Onboarding flow
1. Sign up → Create organization
2. Choose plan (start with free trial)
3. Setup wizard:
   - Add first data center
   - Connect data sources
   - Set up alerts
4. Dashboard tour
5. Invite team members
```

### B. Team Management
```python
# backend/team_service.py
class TeamService:
    @staticmethod
    def invite_user(org_id: str, email: str, role: str):
        """Send invitation email"""
        token = generate_invite_token(org_id, email, role)
        send_email(
            to=email,
            subject="You've been invited to Flaer",
            template="invite",
            data={"token": token, "org_name": org.name}
        )
    
    @staticmethod
    def accept_invite(token: str):
        """Accept invitation and join organization"""
        data = verify_invite_token(token)
        # Create user or add to organization
```

### C. Usage Limits & Metering
```python
# backend/usage_service.py
class UsageService:
    @staticmethod
    async def check_limit(org_id: str, resource: str):
        """Check if organization is within limits"""
        org = get_organization(org_id)
        limits = PRICING_TIERS[org.plan_tier]
        
        if resource == "data_centers":
            current = count_data_centers(org_id)
            return current < limits["max_data_centers"]
        
        elif resource == "api_calls":
            current = count_api_calls_this_month(org_id)
            return current < limits["api_calls_per_month"]
    
    @staticmethod
    def track_usage(org_id: str, resource: str):
        """Track resource usage"""
        # Log to database for billing/analytics
```

### D. Email Notifications
```python
# backend/notification_service.py
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail

class NotificationService:
    @staticmethod
    def send_alert(user_email: str, alert_type: str, data: dict):
        """Send email alert"""
        templates = {
            "high_carbon": "Your data center {name} has high carbon intensity",
            "threshold_exceeded": "Carbon threshold exceeded at {location}",
            "forecast_warning": "Forecast shows increase in emissions"
        }
        
        message = Mail(
            from_email='alerts@flaer.io',
            to_emails=user_email,
            subject=f'Flaer Alert: {alert_type}',
            html_content=templates[alert_type].format(**data)
        )
        
        sg = SendGridAPIClient(os.getenv('SENDGRID_API_KEY'))
        sg.send(message)
```

---

## 6. Admin Dashboard

### Features Needed
1. **User Management**
   - View all users
   - Suspend/activate accounts
   - Change plans manually

2. **Analytics**
   - MRR (Monthly Recurring Revenue)
   - Churn rate
   - Active users
   - API usage stats

3. **Support Tools**
   - View user data
   - Impersonate users (for debugging)
   - Audit logs

### Implementation
```python
# backend/admin_routes.py
@app.get("/admin/stats")
async def admin_stats(current_user: Dict = Depends(require_admin)):
    """Get platform statistics"""
    return {
        "total_users": count_users(),
        "total_organizations": count_organizations(),
        "mrr": calculate_mrr(),
        "active_subscriptions": count_active_subscriptions(),
        "trial_conversions": calculate_trial_conversion_rate()
    }
```

---

## 7. Security Enhancements

### Additional Security Measures
```python
# 1. Rate limiting per organization
@app.middleware("http")
async def rate_limit_by_org(request: Request, call_next):
    org_id = get_org_from_request(request)
    if not check_rate_limit(org_id):
        raise HTTPException(429, "Rate limit exceeded")
    return await call_next(request)

# 2. API key authentication (for programmatic access)
class APIKeyAuth:
    @staticmethod
    def create_api_key(org_id: str, name: str):
        key = f"flaer_{secrets.token_urlsafe(32)}"
        # Store hashed version
        return key
    
    @staticmethod
    def verify_api_key(key: str):
        # Verify and return organization
        pass

# 3. Audit logging
def log_action(user_id: str, action: str, resource: str):
    """Log all important actions"""
    AuditLog.create(
        user_id=user_id,
        action=action,
        resource=resource,
        timestamp=datetime.utcnow(),
        ip_address=request.client.host
    )
```

---

## 8. Monitoring & Analytics

### Application Monitoring
```python
# Use Sentry for error tracking
import sentry_sdk
from sentry_sdk.integrations.fastapi import FastApiIntegration

sentry_sdk.init(
    dsn=os.getenv("SENTRY_DSN"),
    integrations=[FastApiIntegration()],
    traces_sample_rate=1.0
)

# Use Prometheus for metrics
from prometheus_client import Counter, Histogram

api_requests = Counter('api_requests_total', 'Total API requests')
request_duration = Histogram('request_duration_seconds', 'Request duration')
```

### Business Analytics
```python
# Track key metrics
- Sign-ups per day
- Trial-to-paid conversion rate
- Churn rate
- Average revenue per user (ARPU)
- Customer lifetime value (LTV)
- Net Promoter Score (NPS)
```

---

## 9. Legal & Compliance

### Required Documents
1. **Terms of Service**
2. **Privacy Policy** (GDPR compliant)
3. **Data Processing Agreement** (for enterprise)
4. **Cookie Policy**
5. **SLA** (Service Level Agreement for paid plans)

### GDPR Compliance
```python
# Implement data export
@app.get("/api/user/export-data")
async def export_user_data(current_user: Dict = Depends(get_current_user)):
    """Export all user data (GDPR requirement)"""
    return {
        "user": current_user,
        "data_centers": get_user_data_centers(current_user["id"]),
        "api_usage": get_user_api_usage(current_user["id"])
    }

# Implement data deletion
@app.delete("/api/user/delete-account")
async def delete_account(current_user: Dict = Depends(get_current_user)):
    """Delete user account and all data"""
    # Soft delete or hard delete based on requirements
    mark_for_deletion(current_user["id"])
```

---

## 10. Go-to-Market Strategy

### Launch Checklist
- [ ] Set up payment processing (Stripe/Paddle)
- [ ] Create pricing page
- [ ] Set up email service (SendGrid/Mailgun)
- [ ] Deploy to production
- [ ] Set up monitoring (Sentry, Datadog)
- [ ] Create help documentation
- [ ] Set up customer support (Intercom/Zendesk)
- [ ] Create demo video
- [ ] Launch on Product Hunt
- [ ] Start content marketing (blog, SEO)

### Marketing Channels
1. **Content Marketing**
   - Blog about carbon emissions, data centers
   - SEO for "carbon monitoring", "data center emissions"

2. **Direct Sales**
   - Target enterprise data center operators
   - Attend industry conferences

3. **Partnerships**
   - Cloud providers (AWS, Azure, GCP)
   - Data center operators
   - Sustainability consultants

---

## 11. Estimated Timeline

### Phase 1: MVP (4-6 weeks)
- Week 1-2: Database migration, multi-tenancy
- Week 3-4: Billing integration, subscription management
- Week 5-6: Testing, deployment, documentation

### Phase 2: Growth Features (4-6 weeks)
- Team management
- Advanced analytics
- API access
- Integrations

### Phase 3: Scale (Ongoing)
- Enterprise features
- White-label options
- Advanced AI/ML features
- Mobile apps

---

## 12. Cost Breakdown

### Initial Setup Costs
- Domain: $15/year
- SSL Certificate: Free (Let's Encrypt)
- Logo/Branding: $500-2000
- Legal docs: $500-1500

### Monthly Operating Costs (Starter)
- Hosting: $50-150
- Database: $25-50
- Email service: $15-30
- Monitoring: $0-50
- Payment processing: 2.9% + $0.30 per transaction
- **Total: ~$100-300/month**

### Break-even Analysis
- If pricing at $49/month (Starter plan)
- Need ~3-6 customers to break even
- Target: 100 customers = $4,900 MRR

---

## Next Steps

1. **Choose your stack** (Recommended: FastAPI + PostgreSQL + Svelte + Vercel/DigitalOcean)
2. **Set up database** and migrate data
3. **Implement billing** with Stripe
4. **Deploy to production**
5. **Launch with free tier** to get initial users
6. **Iterate based on feedback**

## Resources

- [Stripe Documentation](https://stripe.com/docs)
- [FastAPI Best Practices](https://fastapi.tiangolo.com/tutorial/)
- [SaaS Metrics Guide](https://www.saastr.com/)
- [GDPR Compliance Checklist](https://gdpr.eu/checklist/)

---

**Ready to build your SaaS? Start with Phase 1 and iterate!** 🚀