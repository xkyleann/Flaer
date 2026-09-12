"""
Database configuration and session management
"""
from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import sessionmaker
import os

# Database URL - defaults to SQLite for development
DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "sqlite:///./flaer.db"  # Change to PostgreSQL in production
)

# Create engine
engine = create_engine(
    DATABASE_URL,
    connect_args={"check_same_thread": False} if "sqlite" in DATABASE_URL else {}
)

# Create session factory
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base class for models
Base = declarative_base()

# Dependency to get database session
def get_db():
    """Get database session"""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Initialize database
def init_db():
    """Initialize database tables"""
    Base.metadata.create_all(bind=engine)


def init_tenant_database(seed_defaults: bool = True):
    """Create tenant-aware tables and optionally seed demo/test tenants."""
    init_db()
    if not seed_defaults:
        return

    from init_database import seed_default_tenants

    db = SessionLocal()
    try:
        seed_default_tenants(db)
    finally:
        db.close()

# Made with Bob
