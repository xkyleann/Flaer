# Database Setup Guide for Flaer SaaS

## Important: Python Version Compatibility

⚠️ **SQLAlchemy 2.0 has compatibility issues with Python 3.13**

### Recommended Setup:

**Option 1: Use Python 3.11 or 3.12 (Recommended)**
```bash
# Install Python 3.12 using pyenv
brew install pyenv
pyenv install 3.12.0
pyenv local 3.12.0

# Create virtual environment
cd flaer/backend
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Initialize database
python init_database.py --seed
```

**Option 2: Use SQLite without full SaaS features (Current Setup)**
The app will work without the database for basic features. The SaaS features (multi-tenancy, billing, usage tracking) require the database.

## Database Initialization

Once you have Python 3.11/3.12 installed:

### 1. Basic Setup (Create Tables Only)
```bash
cd flaer/backend
python init_database.py
```

### 2. Setup with Sample Data
```bash
python init_database.py --seed
```

This creates:
- **Organization**: Acme Corporation (Professional tier)
- **Admin User**: admin@acme.com / admin123
- **Data Center**: US East Data Center
- **Subscription**: Active professional plan

### 3. Reset Database (⚠️ Deletes All Data)
```bash
python init_database.py --reset
```

## Database Schema

The database includes these tables:

### Core Tables:
- **organizations** - Multi-tenant organizations with subscription info
- **users** - User accounts linked to organizations
- **data_centers** - Data center tracking per organization

### SaaS Tables:
- **api_usage** - API call tracking and rate limiting
- **invitations** - User invitation system
- **audit_logs** - Security and compliance logging

## Environment Configuration

Create `.env` file in `backend/` directory:

```env
# Database
DATABASE_URL=sqlite:///./flaer.db
# For PostgreSQL: postgresql://user:password@localhost/flaer

# JWT Authentication
SECRET_KEY=your-secret-key-here-change-in-production
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30

# Stripe (for billing)
STRIPE_SECRET_KEY=sk_test_your_stripe_key
STRIPE_PUBLISHABLE_KEY=pk_test_your_stripe_key
STRIPE_WEBHOOK_SECRET=whsec_your_webhook_secret

# Email (for invitations)
SMTP_HOST=smtp.gmail.com
SMTP_PORT=587
SMTP_USER=your-email@gmail.com
SMTP_PASSWORD=your-app-password
```

## Verify Database Setup

```bash
# Check if database file was created
ls -la flaer.db

# Test database connection
python -c "from database import engine; print('✅ Database connected:', engine.url)"

# Run tests
pytest tests/
```

## Production Database Setup

For production, use PostgreSQL:

```bash
# Install PostgreSQL
brew install postgresql@14

# Create database
createdb flaer_production

# Update .env
DATABASE_URL=postgresql://user:password@localhost/flaer_production

# Run migrations
alembic upgrade head
```

## Troubleshooting

### Issue: SQLAlchemy import error with Python 3.13
**Solution**: Use Python 3.11 or 3.12

### Issue: Database file not found
**Solution**: Run `python init_database.py` first

### Issue: Permission denied
**Solution**: Check file permissions: `chmod 644 flaer.db`

### Issue: Table already exists
**Solution**: Use `--reset` flag to recreate tables

## Next Steps

After database setup:

1. **Start Backend**:
   ```bash
   cd backend
   uvicorn main:app --reload
   ```

2. **Start Frontend**:
   ```bash
   cd frontend-svelte
   npm run dev
   ```

3. **Test Login**:
   - Visit: http://localhost:5173
   - Email: admin@acme.com
   - Password: admin123

4. **View Pricing**:
   - Visit: http://localhost:5173/#pricing
   - See all 4 subscription tiers

## Database Backup

```bash
# Backup SQLite database
cp flaer.db flaer.db.backup

# Backup PostgreSQL
pg_dump flaer_production > backup.sql
```

## Migration Management

```bash
# Create new migration
alembic revision --autogenerate -m "description"

# Apply migrations
alembic upgrade head

# Rollback migration
alembic downgrade -1