#!/usr/bin/env python3
"""
Database initialization for Flaer SaaS tenants.
Creates all tables and seeds isolated demo/test client organizations.
"""

import argparse
import os
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

from auth_service import AuthService
from database import Base, SessionLocal, engine
from models import DataCenter, Organization, User


DEFAULT_TENANTS = [
    {
        "id": "demo_org",
        "name": "Flaer Demo",
        "slug": "flaer-demo",
        "plan_tier": "enterprise",
        "subscription_status": "active",
        "users": [
            {
                "id": "user_001",
                "email": "demo@flaer.io",
                "password": "Demo@2026!",
                "full_name": "Demo User",
                "role": "admin",
            }
        ],
        "data_centers": [
            {
                "name": "N. Virginia",
                "location": "US East",
                "risk_level": "high",
                "carbon_intensity": 412,
                "capacity_mw": 150,
                "pue": 1.42,
                "renewable_pct": 48,
                "wue": 1.8,
                "cue": 0.58,
                "annual_water": "2.4M m3",
                "annual_co2": "124K tCO2e",
                "forecast_2035": "+18%",
                "csrd_exposure": "High",
            },
            {
                "name": "Singapore",
                "location": "APAC",
                "risk_level": "high",
                "carbon_intensity": 408,
                "capacity_mw": 120,
                "pue": 1.38,
                "renewable_pct": 35,
                "wue": 2.1,
                "cue": 0.62,
                "annual_water": "1.8M m3",
                "annual_co2": "98K tCO2e",
                "forecast_2035": "+12%",
                "csrd_exposure": "Medium",
            },
            {
                "name": "Stockholm",
                "location": "Nordic",
                "risk_level": "low",
                "carbon_intensity": 22,
                "capacity_mw": 200,
                "pue": 1.08,
                "renewable_pct": 98,
                "wue": 0.4,
                "cue": 0.02,
                "annual_water": "0.3M m3",
                "annual_co2": "8K tCO2e",
                "forecast_2035": "-5%",
                "csrd_exposure": "Low",
            },
        ],
    },
    {
        "id": "test_org",
        "name": "Test Company",
        "slug": "test-company",
        "plan_tier": "starter",
        "subscription_status": "trial",
        "users": [
            {
                "id": "user_002",
                "email": "test@flaer.io",
                "password": "Test@2026!",
                "full_name": "Test User",
                "role": "member",
            }
        ],
        "data_centers": [],
    },
]


def init_database(seed_data: bool = False):
    """Create all tenant-aware tables."""
    Base.metadata.create_all(bind=engine)

    if seed_data:
        db = SessionLocal()
        try:
            seed_default_tenants(db)
        finally:
            db.close()


def seed_default_tenants(db):
    """Upsert default tenants, users, and demo data centers."""
    for tenant in DEFAULT_TENANTS:
        organization = db.get(Organization, tenant["id"])
        if not organization:
            organization = Organization(
                id=tenant["id"],
                name=tenant["name"],
                slug=tenant["slug"],
                plan_tier=tenant["plan_tier"],
                subscription_status=tenant["subscription_status"],
            )
            db.add(organization)
        else:
            organization.name = tenant["name"]
            organization.slug = tenant["slug"]
            organization.plan_tier = tenant["plan_tier"]
            organization.subscription_status = tenant["subscription_status"]

        for user_data in tenant["users"]:
            user = db.get(User, user_data["id"])
            if not user:
                user = User(
                    id=user_data["id"],
                    email=user_data["email"],
                    password_hash=AuthService.get_password_hash(user_data["password"]),
                    full_name=user_data["full_name"],
                    role=user_data["role"],
                    organization_id=tenant["id"],
                    is_active=True,
                )
                db.add(user)
            else:
                user.email = user_data["email"]
                user.full_name = user_data["full_name"]
                user.role = user_data["role"]
                user.organization_id = tenant["id"]
                user.is_active = True

        for dc_data in tenant["data_centers"]:
            existing_dc = db.query(DataCenter).filter(
                DataCenter.organization_id == tenant["id"],
                DataCenter.name == dc_data["name"],
            ).first()
            if existing_dc:
                for key, value in dc_data.items():
                    setattr(existing_dc, key, value)
                existing_dc.is_active = True
            else:
                db.add(DataCenter(organization_id=tenant["id"], **dc_data))

    db.commit()


def reset_database(seed_data: bool = True):
    """Drop all tables and recreate them. This deletes all local data."""
    Base.metadata.drop_all(bind=engine)
    init_database(seed_data=seed_data)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Initialize Flaer tenant database")
    parser.add_argument("--seed", action="store_true", help="Seed demo/test tenants")
    parser.add_argument("--reset", action="store_true", help="Drop and recreate all tables")
    args = parser.parse_args()

    if os.getenv("ENVIRONMENT", "development").strip().lower() == "production" and (args.seed or args.reset):
        parser.error("Demo/test seeding and database resets are disabled in production.")

    if args.reset:
        reset_database(seed_data=True)
    else:
        init_database(seed_data=args.seed)

    print("Database setup complete.")
    if args.seed or args.reset:
        print("Seeded tenants: demo_org has facilities, test_org is planner-only.")
