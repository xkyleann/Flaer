"""
Database models for SaaS multi-tenancy
"""
from sqlalchemy import Column, String, Integer, Float, DateTime, ForeignKey, Boolean, Text
from sqlalchemy.orm import relationship
from database import Base
from datetime import datetime, timezone
import uuid


def generate_uuid():
    """Generate UUID string"""
    return str(uuid.uuid4())


class Organization(Base):
    """Organization/Tenant model"""
    __tablename__ = "organizations"
    
    id = Column(String, primary_key=True, default=generate_uuid)
    name = Column(String(255), nullable=False)
    slug = Column(String(100), unique=True, nullable=False)
    plan_tier = Column(String(50), default="free")  # free, starter, professional, enterprise
    subscription_status = Column(String(50), default="trial")  # trial, active, suspended, cancelled
    stripe_customer_id = Column(String(255), nullable=True)
    stripe_subscription_id = Column(String(255), nullable=True)
    trial_ends_at = Column(DateTime, nullable=True)
    max_data_centers = Column(Integer, default=3)
    max_users = Column(Integer, default=2)
    api_calls_limit = Column(Integer, default=1000)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))
    updated_at = Column(DateTime, default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc))
    
    # Relationships
    users = relationship("User", back_populates="organization", cascade="all, delete-orphan")
    data_centers = relationship("DataCenter", back_populates="organization", cascade="all, delete-orphan")
    api_usage = relationship("APIUsage", back_populates="organization", cascade="all, delete-orphan")
    
    def __repr__(self):
        return f"<Organization {self.name} ({self.plan_tier})>"


class User(Base):
    """User model with organization relationship"""
    __tablename__ = "users"
    
    id = Column(String, primary_key=True, default=generate_uuid)
    email = Column(String(255), unique=True, nullable=False, index=True)
    password_hash = Column(String(255), nullable=False)
    full_name = Column(String(255), nullable=False)
    organization_id = Column(String, ForeignKey("organizations.id"), nullable=False)
    role = Column(String(50), default="member")  # owner, admin, member, viewer
    is_active = Column(Boolean, default=True)
    otp_enabled = Column(Boolean, default=False)
    otp_secret = Column(String(255), nullable=True)
    last_login = Column(DateTime, nullable=True)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))
    updated_at = Column(DateTime, default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc))
    
    # Relationships
    organization = relationship("Organization", back_populates="users")
    
    def __repr__(self):
        return f"<User {self.email} ({self.role})>"


class DataCenter(Base):
    """Data center model"""
    __tablename__ = "data_centers"
    
    id = Column(String, primary_key=True, default=generate_uuid)
    organization_id = Column(String, ForeignKey("organizations.id"), nullable=False)
    name = Column(String(255), nullable=False)
    location = Column(String(255), nullable=False)
    risk_level = Column(String(50), default="medium")  # high, medium, low
    carbon_intensity = Column(Float, nullable=False)
    capacity_mw = Column(Integer, nullable=False)
    pue = Column(Float, nullable=False)
    renewable_pct = Column(Integer, default=0)
    wue = Column(Float, nullable=True)
    cue = Column(Float, nullable=True)
    annual_water = Column(String(50), nullable=True)
    annual_co2 = Column(String(50), nullable=True)
    forecast_2035 = Column(String(50), nullable=True)
    csrd_exposure = Column(String(50), nullable=True)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))
    updated_at = Column(DateTime, default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc))
    
    # Relationships
    organization = relationship("Organization", back_populates="data_centers")
    
    def __repr__(self):
        return f"<DataCenter {self.name} ({self.location})>"


class APIUsage(Base):
    """API usage tracking for billing and limits"""
    __tablename__ = "api_usage"
    
    id = Column(String, primary_key=True, default=generate_uuid)
    organization_id = Column(String, ForeignKey("organizations.id"), nullable=False)
    endpoint = Column(String(255), nullable=False)
    method = Column(String(10), nullable=False)
    status_code = Column(Integer, nullable=False)
    response_time_ms = Column(Integer, nullable=False)
    user_id = Column(String, nullable=True)
    ip_address = Column(String(50), nullable=True)
    timestamp = Column(DateTime, default=lambda: datetime.now(timezone.utc), index=True)
    
    # Relationships
    organization = relationship("Organization", back_populates="api_usage")
    
    def __repr__(self):
        return f"<APIUsage {self.endpoint} at {self.timestamp}>"


class Invitation(Base):
    """Team invitation model"""
    __tablename__ = "invitations"
    
    id = Column(String, primary_key=True, default=generate_uuid)
    organization_id = Column(String, ForeignKey("organizations.id"), nullable=False)
    email = Column(String(255), nullable=False)
    role = Column(String(50), default="member")
    token = Column(String(255), unique=True, nullable=False)
    invited_by = Column(String, nullable=False)  # user_id
    status = Column(String(50), default="pending")  # pending, accepted, expired
    expires_at = Column(DateTime, nullable=False)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))
    
    def __repr__(self):
        return f"<Invitation {self.email} ({self.status})>"


class AuditLog(Base):
    """Audit log for security and compliance"""
    __tablename__ = "audit_logs"
    
    id = Column(String, primary_key=True, default=generate_uuid)
    organization_id = Column(String, ForeignKey("organizations.id"), nullable=False)
    user_id = Column(String, nullable=False)
    action = Column(String(100), nullable=False)  # created, updated, deleted, accessed
    resource_type = Column(String(100), nullable=False)  # user, data_center, organization
    resource_id = Column(String, nullable=True)
    details = Column(Text, nullable=True)
    ip_address = Column(String(50), nullable=True)
    user_agent = Column(String(255), nullable=True)
    timestamp = Column(DateTime, default=lambda: datetime.now(timezone.utc), index=True)
    
    def __repr__(self):
        return f"<AuditLog {self.action} {self.resource_type} at {self.timestamp}>"

# Made with Bob
