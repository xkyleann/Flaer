# 🌍 Flaer - Data Center Carbon Intelligence Platform

**Enterprise SaaS platform for tracking, analyzing, and reducing data center carbon emissions.**

[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)
[![Python 3.11+](https://img.shields.io/badge/python-3.11+-blue.svg)](https://www.python.org/downloads/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.104+-green.svg)](https://fastapi.tiangolo.com/)
[![Svelte](https://img.shields.io/badge/Svelte-4.0+-orange.svg)](https://svelte.dev/)

---

## 🚀 Features

### Core Platform
- **Real-time Carbon Tracking** - Monitor data center emissions across global locations
- **AI-Powered Insights** - Machine learning predictions for carbon reduction
- **Interactive Dashboard** - Beautiful, responsive UI built with Svelte
- **Global Mapping** - Visualize data centers on interactive world map
- **Forecasting & Analytics** - Predict future emissions and trends

### SaaS Features
- **Multi-Tenancy** - Organization-based data isolation
- **Subscription Tiers** - Free, Starter ($49), Professional ($199), Enterprise (custom)
- **Usage Tracking** - API call metering and rate limiting
- **Stripe Integration** - Automated billing and subscription management
- **Role-Based Access** - Admin, manager, and viewer roles
- **Audit Logging** - Complete compliance and security tracking

---

## 📁 Project Structure

```
flaer/
├── backend/                    # FastAPI backend
│   ├── main.py                # Main API application
│   ├── auth_service.py        # JWT authentication
│   ├── database.py            # SQLAlchemy setup
│   ├── models.py              # Database models
│   ├── billing_service.py     # Stripe integration
│   ├── usage_service.py       # Usage tracking & limits
│   ├── carbon_data_service.py # Carbon data API
│   ├── init_database.py       # Database initialization
│   ├── requirements.txt       # Python dependencies
│   └── tests/                 # Backend tests
│
├── frontend-svelte/           # Svelte frontend
│   ├── src/
│   │   ├── App.svelte        # Main app component
│   │   ├── lib/              # Reusable components
│   │   │   ├── Dashboard.svelte
│   │   │   ├── Pricing.svelte
│   │   │   ├── Login.svelte
│   │   │   └── ...
│   │   └── stores/           # State management
│   ├── tests/                # E2E tests (Playwright)
│   └── package.json          # Node dependencies
│
└── README.md                 # This file
```

---

## 🛠️ Quick Start

### Prerequisites

- **Python 3.11 or 3.12** (NOT 3.13 - SQLAlchemy compatibility issue)
- **Node.js 18+** and npm
- **Git**

### 1. Clone Repository

```bash
git clone https://github.com/xkyleann/Flaer.git
cd Flaer/flaer
```

### 2. Backend Setup

```bash
# Navigate to backend
cd backend

# Create virtual environment (use Python 3.11 or 3.12)
python3 -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Configure environment
cp .env.example .env
# Edit .env and set SECRET_KEY and other variables

# Initialize database with sample data
python init_database.py --seed

# Start backend server
uvicorn main:app --reload
```

Backend runs at: **http://localhost:8000**
API docs at: **http://localhost:8000/docs**

### 3. Frontend Setup

```bash
# Navigate to frontend (new terminal)
cd frontend-svelte

# Install dependencies
npm install

# Start development server
npm run dev
```

Frontend runs at: **http://localhost:5173**

### 4. Login with Sample Account

```
Email: admin@acme.com
Password: admin123
```

---

## 🎯 API Endpoints

### Authentication
- `POST /auth/register` - Register new user
- `POST /auth/login` - Login and get JWT token
- `POST /auth/refresh` - Refresh access token
- `GET /auth/me` - Get current user info

### Organizations
- `GET /api/organizations` - List organizations
- `POST /api/organizations` - Create organization
- `GET /api/organizations/{id}` - Get organization details

### Data Centers
- `GET /api/data-centers` - List data centers
- `POST /api/data-centers` - Add data center
- `GET /api/data-centers/{id}` - Get data center details

### Carbon Data
- `GET /api/carbon/intensity` - Get carbon intensity data
- `GET /api/carbon/forecast` - Get emissions forecast

### Billing (Stripe)
- `POST /api/billing/create-checkout` - Create Stripe checkout
- `POST /api/billing/webhook` - Stripe webhook handler
- `GET /api/billing/subscription` - Get subscription status

---

## 💳 Subscription Tiers

| Feature | Free | Starter | Professional | Enterprise |
|---------|------|---------|--------------|------------|
| **Price** | $0/mo | $49/mo | $199/mo | Custom |
| **API Calls** | 100/mo | 10,000/mo | 100,000/mo | Unlimited |
| **Data Centers** | 5 | 50 | Unlimited | Unlimited |
| **Users** | 2 | 10 | 50 | Unlimited |
| **Support** | Community | Email | Priority | Dedicated |
| **SLA** | - | 99% | 99.9% | 99.99% |

---

## 🧪 Testing

### Backend Tests

```bash
cd backend
pytest tests/ -v
```

### Frontend E2E Tests

```bash
cd frontend-svelte
npx playwright test
```

### Manual Testing

See detailed testing guide in the repository for step-by-step instructions.

---

## 🗄️ Database

### Initialize Database

```bash
cd backend

# Create tables only
python init_database.py

# Create tables with sample data
python init_database.py --seed

# Reset database (⚠️ deletes all data)
python init_database.py --reset
```

### Database Schema

- **organizations** - Multi-tenant organizations
- **users** - User accounts with roles
- **data_centers** - Data center tracking
- **api_usage** - API call metering
- **invitations** - User invitation system
- **audit_logs** - Security and compliance

### Supported Databases

- **SQLite** (development) - Default, no setup required
- **PostgreSQL** (production) - Recommended for production

---

## 🔐 Security

- **JWT Authentication** - Secure token-based auth
- **Password Hashing** - bcrypt with salt
- **Rate Limiting** - Prevent API abuse
- **SQL Injection Protection** - Parameterized queries
- **CORS Configuration** - Controlled cross-origin access
- **Audit Logging** - Track all sensitive operations

---

## 🚀 Deployment

### Backend (FastAPI)

**Recommended: Railway, Render, or AWS**

```bash
# Install production dependencies
pip install gunicorn

# Run with Gunicorn
gunicorn main:app -w 4 -k uvicorn.workers.UvicornWorker
```

### Frontend (Svelte)

**Recommended: Vercel, Netlify, or Cloudflare Pages**

```bash
# Build for production
npm run build

# Preview production build
npm run preview
```

### Environment Variables

Required for production:

```env
DATABASE_URL=postgresql://user:pass@host/db
SECRET_KEY=your-secret-key-min-32-chars
STRIPE_SECRET_KEY=sk_live_...
STRIPE_PUBLISHABLE_KEY=pk_live_...
STRIPE_WEBHOOK_SECRET=whsec_...
FRONTEND_URL=https://your-domain.com
```

---

## 📊 Tech Stack

### Backend
- **FastAPI** - Modern Python web framework
- **SQLAlchemy** - SQL toolkit and ORM
- **Pydantic** - Data validation
- **JWT** - Authentication tokens
- **Stripe** - Payment processing
- **Pytest** - Testing framework

### Frontend
- **Svelte** - Reactive UI framework
- **Vite** - Build tool and dev server
- **Playwright** - E2E testing
- **Chart.js** - Data visualization
- **Leaflet** - Interactive maps

### Database
- **PostgreSQL** - Production database
- **SQLite** - Development database

---

## 🤝 Contributing

Contributions are welcome! Please follow these steps:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

---

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## 🔗 Links

- **GitHub**: https://github.com/xkyleann/Flaer
- **Documentation**: See repository docs/
- **Issues**: https://github.com/xkyleann/Flaer/issues
- **Discussions**: https://github.com/xkyleann/Flaer/discussions

---

## 📧 Support

- **Email**: support@flaer.io
- **Documentation**: Check repository docs
- **Community**: GitHub Discussions

---

## 🎉 Acknowledgments

Built with ❤️ for a sustainable future. Inspired by the AIrth project.

**Flaer** - Making data centers carbon-intelligent, one insight at a time.