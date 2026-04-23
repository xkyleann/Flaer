# Flaer SaaS Setup Guide

## Quick Start

This guide will help you set up Flaer as a production-ready SaaS platform.

## Prerequisites

- Python 3.11+
- Node.js 18+
- PostgreSQL 15+ (or SQLite for development)
- Stripe account (for billing)

## Installation

### 1. Backend Setup

```bash
cd flaer/backend

# Create virtual environment
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Set up environment variables
cp .env.example .env
# Edit .env with your configuration
```

### 2. Environment Variables

Create a `.env` file in `flaer/backend/`:

```env
# Database
DATABASE_URL=postgresql://user:password@localhost:5432/flaer
# For development, you can use SQLite:
# DATABASE_URL=sqlite:///./flaer.db

# JWT Secret (generate with: python -c "import secrets; print(secrets.token_urlsafe(32))")
JWT_SECRET_KEY=your-secret-key-here

# Stripe (get from https://dashboard.stripe.com/apikeys)
STRIPE_SECRET_KEY=sk_test_...
STRIPE_WEBHOOK_SECRET=whsec_...
STRIPE_PRICE_STARTER=price_...
STRIPE_PRICE_PRO=price_...
STRIPE_PRICE_ENTERPRISE=price_...

# Frontend URL
FRONTEND_URL=http://localhost:5173

# Optional: Email service (SendGrid, Mailgun, etc.)
# SENDGRID_API_KEY=your-key
# EMAIL_FROM=noreply@flaer.io

# Optional: Monitoring
# SENTRY_DSN=your-sentry-dsn
```

### 3. Database Migration

```bash
# Initialize database
python -c "from database import init_db; init_db()"

# Or use Alembic for migrations (recommended for production)
alembic init alembic
alembic revision --autogenerate -m "Initial migration"
alembic upgrade head
```

### 4. Frontend Setup

```bash
cd flaer/frontend-svelte

# Install dependencies
npm install

# Set up environment variables
cp .env.example .env
# Edit .env with your API URL
```

Create `.env` in `flaer/frontend-svelte/`:

```env
VITE_API_URL=http://localhost:5001
VITE_STRIPE_PUBLISHABLE_KEY=pk_test_...
```

## Running the Application

### Development Mode

**Terminal 1 - Backend:**
```bash
cd flaer/backend
source venv/bin/activate
uvicorn main:app --reload --port 5001
```

**Terminal 2 - Frontend:**
```bash
cd flaer/frontend-svelte
npm run dev
```

Access the application at: http://localhost:5173

### Production Mode

See `PRODUCTION_READY_GUIDE.md` for deployment instructions.

## Stripe Setup

### 1. Create Stripe Account
1. Sign up at https://stripe.com
2. Get your API keys from Dashboard > Developers > API keys

### 2. Create Products & Prices
```bash
# Using Stripe CLI
stripe products create --name="Flaer Starter" --description="Starter plan"
stripe prices create --product=prod_xxx --unit-amount=4900 --currency=usd --recurring[interval]=month

stripe products create --name="Flaer Professional" --description="Professional plan"
stripe prices create --product=prod_xxx --unit-amount=19900 --currency=usd --recurring[interval]=month
```

### 3. Set Up Webhooks
1. Go to Dashboard > Developers > Webhooks
2. Add endpoint: `https://yourdomain.com/api/billing/webhook`
3. Select events:
   - `checkout.session.completed`
   - `customer.subscription.updated`
   - `customer.subscription.deleted`
   - `invoice.payment_failed`
   - `invoice.payment_succeeded`
4. Copy webhook secret to `.env`

## Database Schema

The SaaS implementation includes these tables:

- **organizations**: Tenant/customer data
- **users**: User accounts with organization relationship
- **data_centers**: Data center monitoring data
- **api_usage**: API call tracking for billing
- **invitations**: Team member invitations
- **audit_logs**: Security and compliance logging

## Features Implemented

### ✅ Multi-Tenancy
- Organization-based data isolation
- User roles (owner, admin, member, viewer)
- Team management

### ✅ Subscription Management
- 4 pricing tiers (Free, Starter, Professional, Enterprise)
- Stripe integration for payments
- Usage-based limits
- Trial period (14 days)

### ✅ Usage Tracking
- API call metering
- Data center limits
- User limits
- Feature access control

### ✅ Security
- JWT authentication
- OTP/2FA support
- Rate limiting
- Audit logging
- GDPR compliance ready

## API Endpoints

### Billing Endpoints (New)
```
POST   /api/billing/create-checkout     - Create Stripe checkout session
POST   /api/billing/create-portal       - Create customer portal session
POST   /api/billing/webhook             - Handle Stripe webhooks
GET    /api/billing/pricing             - Get pricing tiers
GET    /api/billing/usage               - Get current usage stats
```

### Organization Endpoints (New)
```
GET    /api/organizations/me            - Get current organization
PUT    /api/organizations/me            - Update organization
GET    /api/organizations/usage         - Get usage statistics
GET    /api/organizations/limits        - Get plan limits
```

### Team Management (New)
```
POST   /api/team/invite                 - Invite team member
GET    /api/team/members                - List team members
DELETE /api/team/members/:id            - Remove team member
PUT    /api/team/members/:id/role       - Update member role
```

## Testing

```bash
# Run backend tests
cd flaer/backend
pytest tests/ -v

# Run frontend tests
cd flaer/frontend-svelte
npm test
```

## Deployment Checklist

- [ ] Set up production database (PostgreSQL)
- [ ] Configure environment variables
- [ ] Set up Stripe in live mode
- [ ] Configure webhook endpoints
- [ ] Set up SSL/TLS certificates
- [ ] Configure domain and DNS
- [ ] Set up monitoring (Sentry, Datadog)
- [ ] Configure email service
- [ ] Set up backups
- [ ] Review security settings
- [ ] Test payment flow
- [ ] Create legal documents (Terms, Privacy Policy)

## Monitoring & Analytics

### Key Metrics to Track
- Monthly Recurring Revenue (MRR)
- Customer Acquisition Cost (CAC)
- Churn Rate
- Trial-to-Paid Conversion Rate
- Average Revenue Per User (ARPU)
- API Usage per Organization
- System Uptime

### Recommended Tools
- **Stripe Dashboard**: Revenue, subscriptions
- **Sentry**: Error tracking
- **Datadog/New Relic**: Performance monitoring
- **Google Analytics**: User behavior
- **Mixpanel/Amplitude**: Product analytics

## Support & Documentation

- Implementation Guide: `SAAS_IMPLEMENTATION_GUIDE.md`
- Production Guide: `PRODUCTION_READY_GUIDE.md`
- Testing Guide: `TESTING_GUIDE.md`
- API Documentation: http://localhost:5001/docs (when running)

## Troubleshooting

### Database Connection Issues
```bash
# Check PostgreSQL is running
pg_isready

# Test connection
psql -U user -d flaer -h localhost
```

### Stripe Webhook Issues
```bash
# Test webhooks locally with Stripe CLI
stripe listen --forward-to localhost:5001/api/billing/webhook
stripe trigger checkout.session.completed
```

### Import Errors
```bash
# Reinstall dependencies
pip install -r requirements.txt --force-reinstall
```

## Next Steps

1. **Customize Branding**: Update logos, colors, and copy
2. **Add Features**: Implement additional features from the roadmap
3. **Marketing**: Set up landing page, SEO, content marketing
4. **Customer Support**: Set up help desk (Intercom, Zendesk)
5. **Scale**: Monitor performance and scale infrastructure as needed

## Getting Help

- GitHub Issues: https://github.com/xkyleann/Flaer/issues
- Email: support@flaer.io
- Documentation: https://docs.flaer.io (coming soon)

---

**Ready to launch your SaaS!** 🚀

For detailed implementation steps, see `SAAS_IMPLEMENTATION_GUIDE.md`