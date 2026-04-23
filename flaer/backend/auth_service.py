"""
Authentication Service with JWT, OTP, and Security Features
Production-ready authentication system for Flaer platform
"""

import os
import secrets
import hashlib
import hmac
from datetime import datetime, timedelta
from typing import Optional, Dict, Any
import jwt
from argon2 import PasswordHasher
from argon2.exceptions import VerifyMismatchError
import pyotp
from pydantic import BaseModel, EmailStr, validator
import re

# Security Configuration
SECRET_KEY = os.getenv("JWT_SECRET_KEY", secrets.token_urlsafe(32))
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30
REFRESH_TOKEN_EXPIRE_DAYS = 7
OTP_EXPIRE_MINUTES = 5

# Password hashing with Argon2
ph = PasswordHasher()

# Models
class UserCreate(BaseModel):
    email: EmailStr
    password: str
    full_name: str
    company: Optional[str] = None
    
    @validator('password')
    def validate_password(cls, v):
        if len(v) < 8:
            raise ValueError('Password must be at least 8 characters')
        if not re.search(r'[A-Z]', v):
            raise ValueError('Password must contain uppercase letter')
        if not re.search(r'[a-z]', v):
            raise ValueError('Password must contain lowercase letter')
        if not re.search(r'\d', v):
            raise ValueError('Password must contain number')
        if not re.search(r'[!@#$%^&*(),.?":{}|<>]', v):
            raise ValueError('Password must contain special character')
        return v

class UserLogin(BaseModel):
    email: EmailStr
    password: str

class OTPVerify(BaseModel):
    email: EmailStr
    otp_code: str

class TokenResponse(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"
    expires_in: int

class User(BaseModel):
    id: str
    email: EmailStr
    full_name: str
    company: Optional[str]
    role: str
    is_active: bool
    otp_enabled: bool
    created_at: datetime

# In-memory user database (replace with real database in production)
# Initialize with None, will be populated on first access
users_db: Dict[str, Dict[str, Any]] = {}

def _initialize_users():
    """Initialize default users with hashed passwords"""
    if not users_db:
        users_db["demo@flaer.io"] = {
            "id": "user_001",
            "email": "demo@flaer.io",
            "password_hash": ph.hash("Demo@2026!"),
            "full_name": "Demo User",
            "company": "Flaer Demo",
            "role": "admin",
            "is_active": True,
            "otp_enabled": True,
            "otp_secret": pyotp.random_base32(),
            "created_at": datetime.utcnow().isoformat()
        }
        users_db["test@flaer.io"] = {
            "id": "user_002",
            "email": "test@flaer.io",
            "password_hash": ph.hash("Test@2026!"),
            "full_name": "Test User",
            "company": "Test Company",
            "role": "user",
            "is_active": True,
            "otp_enabled": False,
            "otp_secret": None,
            "created_at": datetime.utcnow().isoformat()
        }

# OTP storage (temporary, expires after 5 minutes)
otp_storage: Dict[str, Dict[str, Any]] = {}

# Refresh token storage (in production, use Redis or database)
refresh_tokens: Dict[str, Dict[str, Any]] = {}

class AuthService:
    """Authentication service with JWT, OTP, and security features"""
    
    @staticmethod
    def verify_password(plain_password: str, hashed_password: str) -> bool:
        """Verify password against hash"""
        try:
            ph.verify(hashed_password, plain_password)
            return True
        except VerifyMismatchError:
            return False
    
    @staticmethod
    def get_password_hash(password: str) -> str:
        """Hash password"""
        return ph.hash(password)
    
    @staticmethod
    def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
        """Create JWT access token"""
        to_encode = data.copy()
        if expires_delta:
            expire = datetime.utcnow() + expires_delta
        else:
            expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
        
        to_encode.update({
            "exp": expire,
            "iat": datetime.utcnow(),
            "type": "access"
        })
        
        encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
        return encoded_jwt
    
    @staticmethod
    def create_refresh_token(user_id: str) -> str:
        """Create refresh token"""
        token_id = secrets.token_urlsafe(32)
        expire = datetime.utcnow() + timedelta(days=REFRESH_TOKEN_EXPIRE_DAYS)
        
        refresh_tokens[token_id] = {
            "user_id": user_id,
            "expires_at": expire,
            "created_at": datetime.utcnow()
        }
        
        return token_id
    
    @staticmethod
    def verify_token(token: str) -> Optional[Dict[str, Any]]:
        """Verify JWT token"""
        try:
            payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
            return payload
        except jwt.ExpiredSignatureError:
            return None
        except jwt.JWTError:
            return None
    
    @staticmethod
    def verify_refresh_token(token: str) -> Optional[str]:
        """Verify refresh token and return user_id"""
        if token not in refresh_tokens:
            return None
        
        token_data = refresh_tokens[token]
        if datetime.utcnow() > token_data["expires_at"]:
            del refresh_tokens[token]
            return None
        
        return token_data["user_id"]
    
    @staticmethod
    def revoke_refresh_token(token: str) -> bool:
        """Revoke refresh token"""
        if token in refresh_tokens:
            del refresh_tokens[token]
            return True
        return False
    
    @staticmethod
    def generate_otp(email: str) -> str:
        """Generate OTP for user"""
        user = users_db.get(email)
        if not user or not user.get("otp_enabled"):
            return None
        
        # Generate time-based OTP
        totp = pyotp.TOTP(user["otp_secret"], interval=300)  # 5 minutes
        otp_code = totp.now()
        
        # Store OTP with expiration
        otp_storage[email] = {
            "code": otp_code,
            "expires_at": datetime.utcnow() + timedelta(minutes=OTP_EXPIRE_MINUTES),
            "attempts": 0
        }
        
        return otp_code
    
    @staticmethod
    def verify_otp(email: str, otp_code: str) -> bool:
        """Verify OTP code"""
        if email not in otp_storage:
            return False
        
        otp_data = otp_storage[email]
        
        # Check expiration
        if datetime.utcnow() > otp_data["expires_at"]:
            del otp_storage[email]
            return False
        
        # Check attempts (max 3)
        if otp_data["attempts"] >= 3:
            del otp_storage[email]
            return False
        
        # Verify code
        if otp_data["code"] == otp_code:
            del otp_storage[email]
            return True
        
        # Increment attempts
        otp_data["attempts"] += 1
        return False
    
    @staticmethod
    def authenticate_user(email: str, password: str) -> Optional[Dict[str, Any]]:
        """Authenticate user with email and password"""
        _initialize_users()  # Ensure users are initialized
        user = users_db.get(email)
        if not user:
            return None
        
        if not user["is_active"]:
            return None
        
        if not AuthService.verify_password(password, user["password_hash"]):
            return None
        
        return user
    
    @staticmethod
    def get_user_by_id(user_id: str) -> Optional[Dict[str, Any]]:
        """Get user by ID"""
        _initialize_users()  # Ensure users are initialized
        for user in users_db.values():
            if user["id"] == user_id:
                return user
        return None
    
    @staticmethod
    def get_user_by_email(email: str) -> Optional[Dict[str, Any]]:
        """Get user by email"""
        _initialize_users()  # Ensure users are initialized
        return users_db.get(email)
    
    @staticmethod
    def create_user(user_data: UserCreate) -> Dict[str, Any]:
        """Create new user"""
        if user_data.email in users_db:
            raise ValueError("User already exists")
        
        user_id = f"user_{secrets.token_hex(8)}"
        
        new_user = {
            "id": user_id,
            "email": user_data.email,
            "password_hash": AuthService.get_password_hash(user_data.password),
            "full_name": user_data.full_name,
            "company": user_data.company,
            "role": "user",
            "is_active": True,
            "otp_enabled": False,
            "otp_secret": None,
            "created_at": datetime.utcnow().isoformat()
        }
        
        users_db[user_data.email] = new_user
        return new_user
    
    @staticmethod
    def enable_otp(email: str) -> str:
        """Enable OTP for user and return secret"""
        user = users_db.get(email)
        if not user:
            raise ValueError("User not found")
        
        otp_secret = pyotp.random_base32()
        user["otp_enabled"] = True
        user["otp_secret"] = otp_secret
        
        # Generate provisioning URI for QR code
        totp = pyotp.TOTP(otp_secret)
        provisioning_uri = totp.provisioning_uri(
            name=email,
            issuer_name="Flaer Platform"
        )
        
        return provisioning_uri
    
    @staticmethod
    def disable_otp(email: str) -> bool:
        """Disable OTP for user"""
        user = users_db.get(email)
        if not user:
            return False
        
        user["otp_enabled"] = False
        user["otp_secret"] = None
        return True

# Create auth service instance
auth_service = AuthService()

# Made with Bob
