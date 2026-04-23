#!/usr/bin/env python3
"""
Database initialization script for Flaer SaaS platform.
Creates all tables and optionally seeds with sample data.
"""

import sys
from pathlib import Path

# Add backend directory to path
sys.path.insert(0, str(Path(__file__).parent))

from database import engine, Base, get_db
from models import Organization, User, DataCenter
from datetime import datetime, timedelta
import bcrypt

def init_database(seed_data=False):
    """Initialize database tables"""
    print("🔧 Creating database tables...")
    
    # Create all tables
    Base.metadata.create_all(bind=engine)
    
    print("✅ Database tables created successfully!")
    print("\nCreated tables:")
    print("  - organizations")
    print("  - users")
    print("  - data_centers")
    print("  - subscriptions")
    print("  - api_usage")
    print("  - invitations")
    print("  - audit_logs")
    
    if seed_data:
        print("\n🌱 Seeding sample data...")
        seed_sample_data()

def seed_sample_data():
    """Add sample data for testing"""
    db = next(get_db())
    
    try:
        # Check if data already exists
        existing_org = db.query(Organization).first()
        if existing_org:
            print("⚠️  Sample data already exists. Skipping seed.")
            return
        
        # Create sample organization
        org = Organization(
            name="Acme Corporation",
            slug="acme-corp",
            plan_tier="professional",
            subscription_status="active"
        )
        db.add(org)
        db.flush()
        
        # Create sample admin user
        password_hash = bcrypt.hashpw("admin123".encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
        admin = User(
            email="admin@acme.com",
            password_hash=password_hash,
            full_name="Admin User",
            role="admin",
            organization_id=org.id,
            is_active=True,
            email_verified=True
        )
        db.add(admin)
        
        # Create sample data center
        dc = DataCenter(
            name="US East Data Center",
            location="Virginia, USA",
            latitude=37.4316,
            longitude=-78.6569,
            provider="AWS",
            organization_id=org.id,
            carbon_intensity=450.5,
            energy_consumption=1250.0,
            renewable_percentage=35.0
        )
        db.add(dc)
        
        db.commit()
        
        print("✅ Sample data created:")
        print(f"  - Organization: {org.name} (ID: {org.id})")
        print(f"  - Admin User: {admin.email} (password: admin123)")
        print(f"  - Data Center: {dc.name}")
        print(f"  - Subscription: {org.plan_tier} tier (stored in organization)")
        
    except Exception as e:
        db.rollback()
        print(f"❌ Error seeding data: {e}")
    finally:
        db.close()

def reset_database():
    """Drop all tables and recreate them"""
    print("⚠️  WARNING: This will delete all data!")
    response = input("Are you sure you want to reset the database? (yes/no): ")
    
    if response.lower() == 'yes':
        print("🗑️  Dropping all tables...")
        Base.metadata.drop_all(bind=engine)
        print("✅ Tables dropped")
        init_database(seed_data=True)
    else:
        print("❌ Reset cancelled")

if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description="Initialize Flaer database")
    parser.add_argument("--seed", action="store_true", help="Seed with sample data")
    parser.add_argument("--reset", action="store_true", help="Reset database (WARNING: deletes all data)")
    
    args = parser.parse_args()
    
    if args.reset:
        reset_database()
    else:
        init_database(seed_data=args.seed)
        
    print("\n✨ Database setup complete!")
    print("\nNext steps:")
    print("1. Start backend: cd backend && uvicorn main:app --reload")
    print("2. Start frontend: cd frontend-svelte && npm run dev")
    print("3. Visit: http://localhost:5173")
    
    if args.seed:
        print("\n🔑 Test credentials:")
        print("   Email: admin@acme.com")
        print("   Password: admin123")

