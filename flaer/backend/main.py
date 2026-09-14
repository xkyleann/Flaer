from dotenv import load_dotenv
load_dotenv()

from fastapi import FastAPI, HTTPException, Depends, status, Response, Cookie, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Union
from enum import Enum
from datetime import datetime, timedelta
import sys
import os
from contextlib import asynccontextmanager
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded
from ai_assistant_service import create_ai_assistant, FlaerAI
from database import get_db, init_tenant_database
from sqlalchemy.orm import Session
from carbon_data_service import carbon_service
from auth_service import (
    auth_service, UserCreate, UserLogin, OTPVerify, TokenResponse,
    User, AuthService, is_production
)
from data_center_service import (
    data_center_service, DataCenterCreate, DataCenterUpdate, DataCenterResponse
)

# Rate limiter
limiter = Limiter(key_func=get_remote_address, enabled="pytest" not in sys.modules)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Ensure tenant tables and default client records exist."""
    init_tenant_database(seed_defaults=not is_production())
    yield

# FastAPI app with metadata
app = FastAPI(
    title="Flaer Carbon Intelligence API",
    description="RESTful API for carbon intelligence dashboard with real-time data center monitoring, emissions forecasting, and site analysis",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
    lifespan=lifespan
)

# Add rate limiter
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

# Security headers middleware
@app.middleware("http")
async def add_security_headers(request, call_next):
    response = await call_next(request)
    response.headers["X-Content-Type-Options"] = "nosniff"
    response.headers["X-Frame-Options"] = "DENY"
    response.headers["X-XSS-Protection"] = "1; mode=block"
    response.headers["Strict-Transport-Security"] = "max-age=31536000; includeSubDomains"
    # Skip strict CSP on docs routes so Swagger UI CDN assets can load
    if request.url.path not in ("/docs", "/redoc", "/openapi.json"):
        response.headers["Content-Security-Policy"] = "default-src 'self'"
    return response

# CORS middleware
allowed_origins = [
    origin.strip()
    for origin in os.getenv(
        "CORS_ORIGINS",
        "http://localhost:5173,http://127.0.0.1:5173",
    ).split(",")
    if origin.strip()
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=allowed_origins,
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE"],
    allow_headers=["*"],
)

# Security
security = HTTPBearer()

# Authentication dependency
async def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(security)) -> Dict:
    """Verify JWT token and return current user"""
    token = credentials.credentials
    payload = AuthService.verify_token(token)
    
    if not payload:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired token",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    user_id = payload.get("sub")
    if not user_id:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token payload",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    user = AuthService.get_user_by_id(str(user_id))
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User not found",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    if not user["is_active"]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="User account is inactive"
        )
    
    return user

# Admin role dependency
async def require_admin(current_user: Dict = Depends(get_current_user)) -> Dict:
    """Require admin role"""
    if current_user["role"] != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Admin access required"
        )
    return current_user

# Pydantic Models
class RiskLevel(str, Enum):
    high = "high"
    medium = "medium"
    low = "low"

class TrendDirection(str, Enum):
    up = "up"
    down = "down"

class PriorityLevel(str, Enum):
    high = "high"
    medium = "medium"
    strategic = "strategic"

class OTPRequiredResponse(BaseModel):
    requires_otp: bool
    email: str
    otp_code: str
    message: str

class DashboardOverview(BaseModel):
    health_score: int = Field(..., ge=0, le=100, description="Portfolio health score")
    total_emissions: float = Field(..., description="Total emissions in million tCO2e")
    carbon_intensity: int = Field(..., description="Average carbon intensity in gCO2/kWh")
    renewable_energy: int = Field(..., ge=0, le=100, description="Renewable energy percentage")
    trajectory_2030: str = Field(..., description="2030 trajectory status")
    facilities_count: int = Field(..., description="Total number of facilities")
    optimized_count: int = Field(..., description="Number of optimized facilities")
    watch_count: int = Field(..., description="Number of facilities under watch")
    critical_count: int = Field(..., description="Number of critical facilities")

class DataCenter(BaseModel):
    id: str = Field(..., description="Unique identifier")
    name: str = Field(..., description="Data center name")
    location: str = Field(..., description="Geographic location")
    risk: RiskLevel = Field(..., description="Risk level assessment")
    co2: str = Field(..., description="CO2 emissions per kWh")
    trend: TrendDirection = Field(..., description="Emissions trend direction")
    carbon_intensity: int = Field(..., description="Carbon intensity in gCO2/kWh")
    capacity_mw: int = Field(..., description="Capacity in megawatts")
    pue: float = Field(..., description="Power Usage Effectiveness")
    renewable_pct: int = Field(..., ge=0, le=100, description="Renewable energy percentage")
    wue: float = Field(..., description="Water Usage Effectiveness")
    cue: float = Field(..., description="Carbon Usage Effectiveness")
    annual_water: str = Field(..., description="Annual water consumption")
    annual_co2: str = Field(..., description="Annual CO2 emissions")
    forecast_2035: str = Field(..., description="2035 forecast change")
    csrd_exposure: str = Field(..., description="CSRD compliance exposure level")

class ForecastData(BaseModel):
    facility: str = Field(..., description="Facility name")
    scenario: str = Field(..., description="Climate scenario")
    years: List[int] = Field(..., description="Forecast years")
    bau_emissions: List[int] = Field(..., description="Business-as-usual emissions")
    optimized_emissions: List[int] = Field(..., description="Optimized pathway emissions")
    threshold: int = Field(..., description="Regulatory threshold")
    potential_reduction: int = Field(..., description="Potential reduction percentage")
    cost_avoidance: int = Field(..., description="Cost avoidance in million USD")
    sbti_status: str = Field(..., description="SBTi alignment status")

class PriorityAction(BaseModel):
    priority: PriorityLevel = Field(..., description="Priority level")
    title: str = Field(..., description="Action title")
    description: str = Field(..., description="Detailed description")
    reduction: str = Field(..., description="Annual CO2 reduction")
    cost: str = Field(..., description="Implementation cost")
    confidence: int = Field(..., ge=0, le=100, description="Confidence score")

class SiteFactor(BaseModel):
    name: str = Field(..., description="Factor name")
    score: int = Field(..., ge=0, le=100, description="Factor score")
    note: str = Field(..., description="Detailed assessment note")

class SiteIntelligence(BaseModel):
    name: str = Field(..., description="Site location name")
    score: int = Field(..., ge=0, le=100, description="Overall suitability score")
    rating: str = Field(..., description="Rating description")
    summary: str = Field(..., description="Executive summary")
    recommendation: str = Field(..., description="Recommendation level")
    factors: List[SiteFactor] = Field(..., description="Evaluation factors")

class CalculatorInput(BaseModel):
    servers: int = Field(..., ge=100, le=10000, description="Number of servers")
    pue: float = Field(..., ge=1.0, le=2.0, description="Power Usage Effectiveness")
    carbon_intensity: int = Field(..., ge=50, le=800, description="Grid carbon intensity in gCO2/kWh")
    utilization: int = Field(..., ge=20, le=100, description="Average utilization percentage")

class CalculatorResult(BaseModel):
    annual_emissions: float = Field(..., description="Annual emissions in tCO2e")
    monthly_cost: float = Field(..., description="Monthly energy cost in thousands")
    scope2_intensity: int = Field(..., description="Scope 2 intensity in gCO2/kWh")
    trees_equivalent: int = Field(..., description="Trees needed to offset")
    cars_equivalent: int = Field(..., description="Cars driven for 1 year equivalent")

# Data
DASHBOARD_OVERVIEW = DashboardOverview(
    health_score=72,
    total_emissions=2.4,
    carbon_intensity=284,
    renewable_energy=64,
    trajectory_2030="on_track",
    facilities_count=47,
    optimized_count=12,
    watch_count=18,
    critical_count=2
)

DATA_CENTERS = [
    DataCenter(
        id="virginia", name="N. Virginia", location="US East", risk=RiskLevel.high,
        co2="412 g", trend=TrendDirection.up, carbon_intensity=412, capacity_mw=150,
        pue=1.42, renewable_pct=48, wue=1.8, cue=0.58, annual_water="2.4M m³",
        annual_co2="124K tCO₂e", forecast_2035="+18%", csrd_exposure="High"
    ),
    DataCenter(
        id="singapore", name="Singapore", location="APAC", risk=RiskLevel.high,
        co2="408 g", trend=TrendDirection.up, carbon_intensity=408, capacity_mw=120,
        pue=1.38, renewable_pct=35, wue=2.1, cue=0.62, annual_water="1.8M m³",
        annual_co2="98K tCO₂e", forecast_2035="+12%", csrd_exposure="Medium"
    ),
    DataCenter(
        id="frankfurt", name="Frankfurt", location="EU West", risk=RiskLevel.medium,
        co2="284 g", trend=TrendDirection.down, carbon_intensity=284, capacity_mw=180,
        pue=1.24, renewable_pct=72, wue=1.2, cue=0.35, annual_water="1.2M m³",
        annual_co2="76K tCO₂e", forecast_2035="-15%", csrd_exposure="High"
    ),
    DataCenter(
        id="warsaw", name="Warsaw", location="EU Central", risk=RiskLevel.low,
        co2="234 g", trend=TrendDirection.down, carbon_intensity=234, capacity_mw=95,
        pue=1.19, renewable_pct=68, wue=1.1, cue=0.28, annual_water="0.8M m³",
        annual_co2="42K tCO₂e", forecast_2035="-31%", csrd_exposure="High"
    ),
    DataCenter(
        id="stockholm", name="Stockholm", location="Nordic", risk=RiskLevel.low,
        co2="22 g", trend=TrendDirection.down, carbon_intensity=22, capacity_mw=200,
        pue=1.08, renewable_pct=98, wue=0.4, cue=0.02, annual_water="0.3M m³",
        annual_co2="8K tCO₂e", forecast_2035="-5%", csrd_exposure="Low"
    )
]

FORECAST_DATA = ForecastData(
    facility="N. Virginia cluster",
    scenario="SSP5-8.5",
    years=[2025, 2027, 2030, 2033, 2035],
    bau_emissions=[95000, 110000, 135000, 165000, 195000],
    optimized_emissions=[95000, 98000, 105000, 110000, 115000],
    threshold=120000,
    potential_reduction=38,
    cost_avoidance=24,
    sbti_status="on_track"
)

PRIORITY_ACTIONS = [
    PriorityAction(
        priority=PriorityLevel.high,
        title="Migrate workloads from N. Virginia to Stockholm",
        description="Shift non-latency-sensitive compute to Nordic region with 22 gCO₂/kWh grid intensity.",
        reduction="18,400 tCO₂e/year",
        cost="$2.1M migration",
        confidence=92
    ),
    PriorityAction(
        priority=PriorityLevel.high,
        title="Deploy liquid cooling in Singapore cluster",
        description="Replace air cooling with immersion systems to reduce PUE from 1.42 to 1.18.",
        reduction="8,200 tCO₂e/year",
        cost="$4.8M capex",
        confidence=88
    ),
    PriorityAction(
        priority=PriorityLevel.medium,
        title="Negotiate 24/7 renewable PPAs in Frankfurt",
        description="Lock in wind + solar contracts with battery storage to achieve 95% clean energy.",
        reduction="12,600 tCO₂e/year",
        cost="$1.2M/year premium",
        confidence=85
    ),
    PriorityAction(
        priority=PriorityLevel.medium,
        title="Optimize cooling schedules with AI",
        description="Deploy predictive algorithms to reduce cooling energy by 15% across all sites.",
        reduction="6,800 tCO₂e/year",
        cost="$380K software",
        confidence=78
    ),
    PriorityAction(
        priority=PriorityLevel.strategic,
        title="Phase out coal-heavy regions by 2028",
        description="Exit or transform facilities in grids with >40% coal dependency.",
        reduction="32,000 tCO₂e/year",
        cost="$18M restructuring",
        confidence=72
    ),
    PriorityAction(
        priority=PriorityLevel.strategic,
        title="Invest in on-site solar + storage",
        description="Deploy 50MW solar across 12 facilities with 4-hour battery backup.",
        reduction="14,200 tCO₂e/year",
        cost="$42M capex",
        confidence=81
    )
]

SITE_INTELLIGENCE = {
    "stockholm": SiteIntelligence(
        name="Stockholm, Sweden",
        score=88,
        rating="/ 100 — Excellent candidate",
        summary="Outstanding renewable energy, cool climate, strong governance",
        recommendation="strongly_recommended",
        factors=[
            SiteFactor(name="Renewable energy availability", score=96, note="Grid is 98% renewable (hydro + wind); among cleanest in the world"),
            SiteFactor(name="Climate & cooling efficiency", score=94, note="Cold climate enables free cooling 10+ months/year; minimal AC needed"),
            SiteFactor(name="Water availability", score=82, note="Abundant freshwater; low stress even under climate scenarios"),
            SiteFactor(name="Regulatory environment", score=92, note="Stable, transparent, strong ESG culture; CSRD-ready infrastructure"),
            SiteFactor(name="Grid reliability & resilience", score=88, note="Highly reliable Nordic grid; excellent interconnection"),
            SiteFactor(name="Land & infrastructure cost", score=76, note="Moderate costs offset by operational savings and incentives")
        ]
    ),
    "australia": SiteIntelligence(
        name="New South Wales, Australia",
        score=74,
        rating="/ 100 — Good candidate",
        summary="Strong renewable growth, good governance, but water stress risk",
        recommendation="good",
        factors=[
            SiteFactor(name="Renewable energy availability", score=82, note="Grid rapidly decarbonising — 68% renewable target by 2030; solar surplus"),
            SiteFactor(name="Climate & cooling efficiency", score=62, note="Hot summers require significant cooling infrastructure; free cooling limited"),
            SiteFactor(name="Water availability", score=58, note="Water stress risk under climate scenarios; WUE targets harder to achieve"),
            SiteFactor(name="Regulatory environment", score=88, note="Strong governance, transparent regulations, active ESG reporting culture"),
            SiteFactor(name="Grid reliability & resilience", score=86, note="High reliability; good interconnection across eastern grid"),
            SiteFactor(name="Land & infrastructure cost", score=74, note="Moderate costs; good proximity to Asia-Pacific demand centres")
        ]
    ),
    "texas": SiteIntelligence(
        name="Texas, USA",
        score=61,
        rating="/ 100 — Proceed with caution",
        summary="Low cost but grid instability, water scarcity, and high carbon intensity",
        recommendation="caution",
        factors=[
            SiteFactor(name="Renewable energy availability", score=62, note="Large wind/solar capacity but grid mix still includes significant gas (~45%)"),
            SiteFactor(name="Climate & cooling efficiency", score=40, note="Extreme heat; cooling costs are among the highest in North America"),
            SiteFactor(name="Water availability", score=38, note="High water stress; aquifer depletion accelerating. WUE targets very hard to meet"),
            SiteFactor(name="Regulatory environment", score=72, note="Favourable business environment but ERCOT grid isolated; limited interconnection"),
            SiteFactor(name="Grid reliability & resilience", score=52, note="ERCOT outage risk demonstrated in 2021; winter storm vulnerability"),
            SiteFactor(name="Land & infrastructure cost", score=90, note="Very low land cost and strong incentives — primary attraction")
        ]
    )
}

# Authentication Endpoints
@app.post("/api/auth/register", response_model=TokenResponse, tags=["Authentication"])
@limiter.limit("5/hour")
async def register(
    request: Request,
    user_data: UserCreate,
    response: Response,
    db: Session = Depends(get_db)
):
    """Register a new user account"""
    from models import User as DBUser

    # The authentication service keeps a fast in-memory lookup, while the
    # database remains the source of truth across application restarts.
    # Check both before creating a user so a duplicate email returns a clean
    # client error instead of an unhandled database integrity error.
    if db.query(DBUser).filter(DBUser.email == user_data.email).first():
        raise HTTPException(status_code=400, detail="A user with this email already exists")

    try:
        user = AuthService.create_user(user_data)
        from models import Organization as DBOrganization

        organization = DBOrganization(
            id=user["organization_id"],
            name=user_data.company or f"{user_data.full_name}'s organization",
            slug=AuthService.create_organization_slug(user_data.company or user_data.full_name),
            plan_tier="free",
            subscription_status="trial",
        )
        db.add(organization)
        db.add(DBUser(
            id=user["id"],
            email=user["email"],
            password_hash=user["password_hash"],
            full_name=user["full_name"],
            organization_id=user["organization_id"],
            role="owner",
            is_active=True,
        ))
        db.commit()
        
        # Create tokens
        access_token = AuthService.create_access_token(
            data={"sub": user["id"], "email": user["email"], "role": user["role"], "organization_id": user.get("organization_id")}
        )
        refresh_token = AuthService.create_refresh_token(user["id"])
        
        # Set refresh token as HTTP-only cookie
        response.set_cookie(
            key="refresh_token",
            value=refresh_token,
            httponly=True,
            secure=True,
            samesite="lax",
            max_age=7 * 24 * 60 * 60  # 7 days
        )
        
        return TokenResponse(
            access_token=access_token,
            refresh_token=refresh_token,
            expires_in=1800  # 30 minutes
        )
    except ValueError as e:
        db.rollback()
        raise HTTPException(status_code=400, detail=str(e))
    except Exception:
        db.rollback()
        AuthService.delete_user(user_data.email)
        raise

@app.post("/api/auth/login", response_model=Union[TokenResponse, OTPRequiredResponse], tags=["Authentication"])
@limiter.limit("10/minute")
async def login(request: Request, credentials: UserLogin, response: Response):
    """Login with email and password"""
    user = AuthService.authenticate_user(credentials.email, credentials.password)
    
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    # Check if OTP is enabled
    if user.get("otp_enabled") and user.get("otp_confirmed"):
        # Generate and return OTP (in production, send via email/SMS)
        otp_code = AuthService.generate_otp(credentials.email)
        otp_response = {
            "requires_otp": True,
            "email": credentials.email,
            "message": "OTP sent to your registered device"
        }
        if not is_production():
            otp_response["otp_code"] = otp_code
        return otp_response
    
    # Create tokens
    access_token = AuthService.create_access_token(
        data={"sub": user["id"], "email": user["email"], "role": user["role"], "organization_id": user.get("organization_id")}
    )
    refresh_token = AuthService.create_refresh_token(user["id"])
    
    # Set refresh token as HTTP-only cookie
    response.set_cookie(
        key="refresh_token",
        value=refresh_token,
        httponly=True,
        secure=True,
        samesite="lax",
        max_age=7 * 24 * 60 * 60
    )
    
    return TokenResponse(
        access_token=access_token,
        refresh_token=refresh_token,
        expires_in=1800
    )

@app.post("/api/auth/verify-otp", response_model=TokenResponse, tags=["Authentication"])
@limiter.limit("5/minute")
async def verify_otp(request: Request, otp_data: OTPVerify, response: Response):
    """Verify OTP code and complete login"""
    if not AuthService.verify_otp(otp_data.email, otp_data.otp_code):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired OTP code"
        )
    
    user = AuthService.get_user_by_email(otp_data.email)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    # Create tokens
    access_token = AuthService.create_access_token(
        data={"sub": user["id"], "email": user["email"], "role": user["role"], "organization_id": user.get("organization_id")}
    )
    refresh_token = AuthService.create_refresh_token(user["id"])
    
    # Set refresh token as HTTP-only cookie
    response.set_cookie(
        key="refresh_token",
        value=refresh_token,
        httponly=True,
        secure=True,
        samesite="lax",
        max_age=7 * 24 * 60 * 60
    )
    
    return TokenResponse(
        access_token=access_token,
        refresh_token=refresh_token,
        expires_in=1800
    )

@app.post("/api/auth/refresh", response_model=TokenResponse, tags=["Authentication"])
async def refresh_token(response: Response, refresh_token: Optional[str] = Cookie(None)):
    """Refresh access token using refresh token"""
    if not refresh_token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Refresh token not found"
        )
    
    user_id = AuthService.verify_refresh_token(refresh_token)
    if not user_id:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired refresh token"
        )
    
    user = AuthService.get_user_by_id(user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    # Create new tokens
    access_token = AuthService.create_access_token(
        data={"sub": user["id"], "email": user["email"], "role": user["role"], "organization_id": user.get("organization_id")}
    )
    new_refresh_token = AuthService.create_refresh_token(user["id"])
    
    # Revoke old refresh token
    AuthService.revoke_refresh_token(refresh_token)
    
    # Set new refresh token
    response.set_cookie(
        key="refresh_token",
        value=new_refresh_token,
        httponly=True,
        secure=True,
        samesite="lax",
        max_age=7 * 24 * 60 * 60
    )
    
    return TokenResponse(
        access_token=access_token,
        refresh_token=new_refresh_token,
        expires_in=1800
    )

@app.post("/api/auth/logout", tags=["Authentication"])
async def logout(response: Response, refresh_token: Optional[str] = Cookie(None)):
    """Logout and revoke refresh token"""
    if refresh_token:
        AuthService.revoke_refresh_token(refresh_token)
    
    # Clear refresh token cookie
    response.delete_cookie(key="refresh_token")
    
    return {"message": "Successfully logged out"}

@app.get("/api/auth/me", tags=["Authentication"])
async def get_current_user_info(current_user: Dict = Depends(get_current_user)):
    """Get current user information"""
    return {
        "id": current_user["id"],
        "organization_id": current_user.get("organization_id"),
        "email": current_user["email"],
        "full_name": current_user["full_name"],
        "company": current_user.get("company"),
        "role": current_user["role"],
        "otp_enabled": current_user.get("otp_enabled", False)
    }

@app.post("/api/auth/enable-otp", tags=["Authentication"])
async def enable_otp(current_user: Dict = Depends(get_current_user)):
    """Enable OTP for user account"""
    if is_production():
        raise HTTPException(status_code=501, detail="OTP enrollment is not yet available in production")
    provisioning_uri = AuthService.enable_otp(current_user["email"])
    return {
        "message": "OTP setup started",
        "provisioning_uri": provisioning_uri,
        "note": "Scan this URI with your authenticator app. OTP challenges begin after confirmation."
    }

@app.post("/api/auth/disable-otp", tags=["Authentication"])
async def disable_otp(current_user: Dict = Depends(get_current_user)):
    """Disable OTP for user account"""
    if is_production():
        raise HTTPException(status_code=501, detail="OTP management is not yet available in production")
    AuthService.disable_otp(current_user["email"])
    return {"message": "OTP disabled successfully"}

# API Endpoints
@app.get("/", tags=["Root"])
async def root():
    """Root endpoint with API information and links to documentation"""
    return {
        "service": "Flaer Carbon Intelligence API",
        "version": "1.0.0",
        "status": "running",
        "authentication": "JWT with optional OTP",
        "documentation": {
            "swagger_ui": "/docs",
            "redoc": "/redoc",
            "openapi_json": "/openapi.json"
        },
        "frontend_url": os.getenv("FRONTEND_URL", "http://localhost:5173"),
        "endpoints_count": 18
    }

@app.get("/health", tags=["Health"])
@app.get("/api/health", tags=["Health"])
async def health_check():
    """Health check endpoint"""
    return {"status": "ok", "service": "flaer-api"}

@app.get("/api/dashboard/overview", response_model=DashboardOverview, tags=["Dashboard"])
async def get_dashboard_overview(current_user: Dict = Depends(get_current_user)):
    """Get portfolio overview with key metrics (requires authentication)"""
    return DASHBOARD_OVERVIEW

@app.get("/api/dashboard/datacenters", response_model=List[DataCenter], tags=["Data Centers"])
async def get_datacenters(current_user: Dict = Depends(get_current_user)):
    """Get list of all data centers with detailed metrics (requires authentication)"""
    return DATA_CENTERS

@app.get("/api/dashboard/datacenters/{dc_id}", response_model=DataCenter, tags=["Data Centers"])
async def get_datacenter(dc_id: str, current_user: Dict = Depends(get_current_user)):
    """Get detailed information for a specific data center (requires authentication)"""
    dc = next((d for d in DATA_CENTERS if d.id == dc_id), None)
    if not dc:
        raise HTTPException(status_code=404, detail=f"Data center '{dc_id}' not found")
    return dc

@app.get("/api/dashboard/forecast", response_model=ForecastData, tags=["Forecast"])
async def get_forecast(current_user: Dict = Depends(get_current_user)):
    """Get emissions forecast data for 2030/2035 projections (requires authentication)"""
    return FORECAST_DATA

@app.get("/api/dashboard/actions", response_model=List[PriorityAction], tags=["Actions"])
async def get_actions(current_user: Dict = Depends(get_current_user)):
    """Get list of priority actions ranked by impact (requires authentication)"""
    return PRIORITY_ACTIONS

@app.get("/api/dashboard/site-intelligence", tags=["Site Intelligence"])
async def get_site_intelligence(current_user: Dict = Depends(get_current_user)):
    """Get all site intelligence analyses (requires authentication)"""
    return SITE_INTELLIGENCE

@app.get("/api/dashboard/site-intelligence/{site_id}", response_model=SiteIntelligence, tags=["Site Intelligence"])
async def get_site(site_id: str, current_user: Dict = Depends(get_current_user)):
    """Get detailed site intelligence for a specific location (requires authentication)"""
    site = SITE_INTELLIGENCE.get(site_id)
    if not site:
        raise HTTPException(status_code=404, detail=f"Site '{site_id}' not found")
    return site

@app.post("/api/dashboard/calculator", response_model=CalculatorResult, tags=["Calculator"])
async def calculate_emissions(input_data: CalculatorInput, current_user: Dict = Depends(get_current_user)):
    """Calculate carbon emissions based on input parameters (requires authentication)"""
    annual_emissions = (
        input_data.servers * 0.5 * 8760 * input_data.pue * 
        input_data.carbon_intensity * (input_data.utilization / 100)
    ) / 1000000
    
    monthly_cost = input_data.servers * 0.5 * 730 * 0.12 * input_data.pue
    trees_equivalent = annual_emissions * 16
    cars_equivalent = annual_emissions / 4.6
    
    return CalculatorResult(
        annual_emissions=round(annual_emissions, 2),
        monthly_cost=round(monthly_cost / 1000, 0),
        scope2_intensity=int(round(input_data.carbon_intensity * input_data.pue, 0)),
        trees_equivalent=int(round(trees_equivalent, 0)),
        cars_equivalent=int(round(cars_equivalent, 0))
    )

# Carbon Data Endpoints
@app.get("/api/carbon/live", tags=["Carbon Data"])
async def get_live_carbon_data():
    """Get real-time carbon intensity data for all regions"""
    try:
        data = await carbon_service.get_all_regions()
        return {
            "status": "success",
            "timestamp": data[list(data.keys())[0]]["timestamp"] if data else None,
            "regions": data,
            "note": "Data refreshes every 15 minutes. Using fallback data with simulated variation until API keys are configured."
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching carbon data: {str(e)}")

@app.get("/api/carbon/live/{region}", tags=["Carbon Data"])
async def get_region_carbon_data(region: str):
    """Get real-time carbon intensity data for a specific region"""
    try:
        data = await carbon_service.get_carbon_intensity(region)
        if not data:
            raise HTTPException(status_code=404, detail=f"Region '{region}' not found")
        return {
            "status": "success",
            "region": region,
            "data": data
        }
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching carbon data: {str(e)}")

@app.get("/api/carbon/regions", tags=["Carbon Data"])
async def get_available_regions():
    """Get list of available regions for carbon data"""
    return {
        "regions": list(carbon_service.region_zones.keys()),
        "count": len(carbon_service.region_zones)
    }

# ============================================================================
# FLAER AI ASSISTANT ENDPOINTS
# ============================================================================

class WeeklyDigestRequest(BaseModel):
    organization_id: str = Field(..., description="Organization ID")
    week_start: Optional[str] = Field(None, description="Week start date (ISO format)")

class SiteRequirements(BaseModel):
    it_load_mw: float = Field(..., ge=1, le=500, description="Required IT load in MW")
    target_region: str = Field(..., description="Target geographic region")
    renewable_requirement: float = Field(..., ge=0, le=100, description="Minimum renewable % required")
    budget: str = Field(..., description="Budget level: low, medium, high")

class AnomalyCheck(BaseModel):
    data_center_id: str = Field(..., description="Data center ID to check")
    previous_week_data: Optional[Dict] = Field(None, description="Previous week metrics for comparison")

@app.get("/api/ai/context/{organization_id}", tags=["Flaer AI"])
async def detect_user_context(
    organization_id: str,
    db: Session = Depends(get_db),
    current_user: Dict = Depends(get_current_user)
):
    """
    Detect user context: operator (has data centers) or planner (planning new facility)
    """
    try:
        ai = create_ai_assistant(db)
        if organization_id != current_user.get("organization_id"):
            raise HTTPException(status_code=403, detail="Organization access denied")

        context = ai.detect_user_context(organization_id)
        
        return {
            "organization_id": organization_id,
            "context": context,
            "description": "User operates existing data centers" if context == "operator" else "User is planning a new data center"
        }
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error detecting context: {str(e)}")

@app.post("/api/ai/weekly-digest", tags=["Flaer AI"])
async def generate_weekly_digest(
    request: WeeklyDigestRequest,
    db: Session = Depends(get_db),
    current_user: Dict = Depends(get_current_user)
):
    """
    Generate weekly consumption digest for data center operators
    Includes: energy, carbon, PUE, WUE, top actions, and trend analysis
    """
    try:
        ai = create_ai_assistant(db)
        if request.organization_id != current_user.get("organization_id"):
            raise HTTPException(status_code=403, detail="Organization access denied")
        
        # Parse week start date or use current week
        if request.week_start:
            week_start = datetime.fromisoformat(request.week_start.replace('Z', '+00:00'))
        else:
            week_start = datetime.now() - timedelta(days=datetime.now().weekday())
        
        digest = ai.generate_weekly_digest(request.organization_id, week_start)
        if "error" in digest:
            raise HTTPException(status_code=404, detail=digest["error"])
        
        # Format as markdown
        markdown = ai.format_weekly_digest(digest)
        
        return {
            "status": "success",
            "digest": digest,
            "markdown": markdown,
            "generated_at": datetime.now().isoformat()
        }
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error generating digest: {str(e)}")

@app.post("/api/ai/check-anomalies", tags=["Flaer AI"])
async def check_anomalies(
    request: AnomalyCheck,
    db: Session = Depends(get_db),
    current_user: Dict = Depends(get_current_user)
):
    """
    Check for anomalies in data center metrics
    Flags: PUE > 1.75, WUE > 1.8, week-on-week spike > 5%
    """
    try:
        from models import DataCenter
        
        # Get data center
        data_center = db.query(DataCenter).filter(
            DataCenter.id == request.data_center_id,
            DataCenter.organization_id == current_user.get("organization_id")
        ).first()
        
        if not data_center:
            raise HTTPException(status_code=404, detail="Data center not found")
        
        ai = create_ai_assistant(db)
        anomalies = ai.check_anomalies(data_center, request.previous_week_data)
        
        return {
            "status": "success",
            "data_center_id": request.data_center_id,
            "data_center_name": data_center.name,
            "anomalies_found": len(anomalies),
            "anomalies": anomalies
        }
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error checking anomalies: {str(e)}")

@app.post("/api/ai/recommend-locations", tags=["Flaer AI"])
async def recommend_locations(
    requirements: SiteRequirements,
    num_recommendations: int = 5,
    db: Session = Depends(get_db),
    current_user: Dict = Depends(get_current_user)
):
    """
    Recommend top locations for new data center site selection
    Scores based on: grid carbon, renewable availability, water stress, climate risk, regulatory fit
    """
    try:
        ai = create_ai_assistant(db)
        
        requirements_dict = {
            'it_load_mw': requirements.it_load_mw,
            'target_region': requirements.target_region,
            'renewable_requirement': requirements.renewable_requirement,
            'budget': requirements.budget
        }
        
        recommendations = ai.recommend_locations(requirements_dict, num_recommendations)
        
        # Extract best location
        best_location = recommendations[0] if recommendations else None
        
        return {
            "status": "success",
            "requirements": requirements_dict,
            "best_location": best_location,
            "all_recommendations": recommendations,
            "scoring_methodology": "Equal weight (20%) across 5 dimensions: grid carbon, renewable availability, water stress, climate risk, regulatory fit"
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error generating recommendations: {str(e)}")

@app.get("/api/ai/score-location/{location}", tags=["Flaer AI"])
async def score_location(
    location: str,
    it_load_mw: float = 100,
    target_region: str = "global",
    renewable_requirement: float = 50,
    budget: str = "medium",
    db: Session = Depends(get_db),
    current_user: Dict = Depends(get_current_user)
):
    """
    Score a specific location for data center site selection
    Returns composite score and breakdown by dimension
    """
    try:
        ai = create_ai_assistant(db)
        
        requirements = {
            'it_load_mw': it_load_mw,
            'target_region': target_region,
            'renewable_requirement': renewable_requirement,
            'budget': budget
        }
        
        score_data = ai.score_location(location, requirements)
        
        return {
            "status": "success",
            "location": location,
            "score_data": score_data
        }
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error scoring location: {str(e)}")

@app.get("/api/ai/available-locations", tags=["Flaer AI"])
async def get_available_locations(db: Session = Depends(get_db)):
    """Get list of all available locations for site scoring"""
    ai = create_ai_assistant(db)
    locations = list(ai.GRID_CARBON_DATA.keys())
    
    return {
        "locations": locations,
        "count": len(locations),
        "regions": {
            "North America": ["virginia", "oregon", "iowa", "montreal"],
            "Europe": ["frankfurt", "dublin", "stockholm", "milan"],
            "Asia Pacific": ["tokyo", "hong-kong", "singapore", "mumbai"],
            "Other": ["sao-paulo", "bahrain", "cape-town"]
        }
    }


class ChatMessage(BaseModel):
    role: str
    content: str

class ChatRequest(BaseModel):
    messages: List[ChatMessage]
    portfolio_context: Optional[Dict] = None


@app.post("/api/ai/chat", tags=["Flaer AI"])
@limiter.limit("30/minute")
async def ai_chat(request: Request, chat: ChatRequest, current_user: Dict = Depends(get_current_user), db: Session = Depends(get_db)):
    """Claude-powered chat endpoint with data center sustainability context"""
    import os
    api_key = os.getenv("GROQ_API_KEY", "")
    if not api_key:
        raise HTTPException(status_code=503, detail="AI API key not configured")

    try:
        from groq import Groq
    except ImportError:
        raise HTTPException(status_code=503, detail="Groq SDK not installed")

    # Build portfolio context from the user's real data
    dc_context = ""
    try:
        import sqlalchemy
        org_id = current_user.get("organization_id")
        if org_id:
            dcs = db.execute(
                sqlalchemy.text("SELECT name, location, pue, wue, renewable_pct, carbon_intensity, capacity_mw FROM data_centers WHERE organization_id = :org AND is_active = 1"),
                {"org": org_id}
            ).fetchall()
            if dcs:
                dc_context = "\n\nUSER PORTFOLIO:\n" + "\n".join(
                    f"- {r[0]} ({r[1]}): PUE={r[2]}, WUE={r[3]} L/kWh, renewable={r[4]}%, carbon={r[5]} gCO₂/kWh, capacity={r[6]} MW"
                    for r in dcs
                )
    except Exception:
        pass

    system_prompt = f"""You are flaer AI — a concise, expert sustainability intelligence assistant for data center operators and planners.

PLATFORM CONTEXT:
Flaer is a SaaS sustainability intelligence platform. You help users track emissions, optimise PUE/WUE, plan new facilities, navigate CSRD compliance, and evaluate PPAs.

YOUR EXPERTISE:
- GHG Protocol Scope 1, 2 & 3 accounting for data centres
- PUE, WUE, CUE efficiency benchmarking (thresholds: PUE >1.75, WUE >1.8 L/kWh)
- CSRD / EU Taxonomy compliance for digital infrastructure
- Renewable energy procurement: PPAs, RECs, Guarantees of Origin
- Site selection: MCDA scoring across carbon, water, climate, regulatory dimensions
- Climate scenario modelling: SSP5-8.5, IEA NZE, balanced transition
- Cooling technologies: free-air, adiabatic, liquid cooling, district cooling
- Carbon markets: EU ETS, voluntary offsets, CORSIA
- Data sources: IEA 2024 WEO, IPCC AR6, GHG Protocol, EU ETS, Ember grid data
{dc_context}

RESPONSE STYLE:
- Be concise and data-driven. Lead with the answer, not preamble.
- Use **bold** for key numbers and terms.
- Use bullet lists for comparisons or multiple items.
- Include specific numbers (gCO₂/kWh, %, €/MWh) wherever relevant.
- Never say "I'm an AI" or add disclaimers. Just answer as an expert.
- Keep responses under 300 words unless the question demands more detail.
- If the user asks about their portfolio and you have data above, use it."""

    client = Groq(api_key=api_key)
    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        max_tokens=800,
        messages=[{"role": "system", "content": system_prompt}] +  # type: ignore[arg-type]
                 [{"role": m.role, "content": m.content} for m in chat.messages]  # type: ignore[arg-type]
    )

    return {"reply": response.choices[0].message.content}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=5001, log_level="info")


# ============================================================================
# DATA CENTER MANAGEMENT ENDPOINTS
# ============================================================================

@app.post("/api/data-centers", response_model=DataCenterResponse, tags=["Data Centers"])
@limiter.limit("20/minute")
async def create_data_center(
    request: Request,
    data: DataCenterCreate,
    current_user: Dict = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Create a new data center for tracking.
    
    Required metrics:
    - name: Data center name
    - location: Physical location
    - capacity_mw: Total capacity in MW
    - pue: Power Usage Effectiveness (1.0-3.0)
    - carbon_intensity: Grid carbon intensity (gCO2/kWh)
    - renewable_pct: Renewable energy percentage (0-100)
    
    Optional metrics:
    - wue: Water Usage Effectiveness (L/kWh)
    - cue: Carbon Usage Effectiveness
    - latitude/longitude: Geographic coordinates
    """
    organization_id = current_user["organization_id"]
    
    # Check organization limits
    from models import Organization as DBOrganization
    org = db.query(DBOrganization).filter(DBOrganization.id == organization_id).first()
    
    if not org:
        raise HTTPException(status_code=404, detail="Organization not found")
    
    # Count existing data centers
    existing_count = len(data_center_service.get_data_centers(db, organization_id))
    
    if existing_count >= org.max_data_centers:
        raise HTTPException(
            status_code=403,
            detail=f"Data center limit reached. Your plan allows {org.max_data_centers} facilities. Upgrade to add more."
        )
    
    try:
        dc = data_center_service.create_data_center(db, organization_id, data)
        return dc
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@app.get("/api/data-centers", response_model=List[DataCenterResponse], tags=["Data Centers"])
@limiter.limit("60/minute")
async def list_data_centers(
    request: Request,
    include_inactive: bool = False,
    current_user: Dict = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get all data centers for the current organization"""
    organization_id = current_user["organization_id"]
    data_centers = data_center_service.get_data_centers(db, organization_id, include_inactive)
    return data_centers


@app.get("/api/data-centers/summary", tags=["Data Centers"])
@limiter.limit("60/minute")
async def get_portfolio_summary(
    request: Request,
    current_user: Dict = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get portfolio-level summary statistics"""
    organization_id = current_user["organization_id"]
    summary = data_center_service.get_portfolio_summary(db, organization_id)
    return summary


@app.get("/api/data-centers/{dc_id}", response_model=DataCenterResponse, tags=["Data Centers"])
@limiter.limit("60/minute")
async def get_data_center(
    request: Request,
    dc_id: str,
    current_user: Dict = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get a specific data center by ID"""
    organization_id = current_user["organization_id"]
    dc = data_center_service.get_data_center(db, organization_id, dc_id)
    
    if not dc:
        raise HTTPException(status_code=404, detail="Data center not found")
    
    return dc


@app.put("/api/data-centers/{dc_id}", response_model=DataCenterResponse, tags=["Data Centers"])
@limiter.limit("30/minute")
async def update_data_center(
    request: Request,
    dc_id: str,
    data: DataCenterUpdate,
    current_user: Dict = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Update data center metrics.
    
    Use this endpoint to:
    - Update real-time PUE, WUE, CUE values
    - Adjust renewable energy percentage
    - Update carbon intensity as grid mix changes
    - Modify capacity after expansions
    """
    organization_id = current_user["organization_id"]
    dc = data_center_service.update_data_center(db, organization_id, dc_id, data)
    
    if not dc:
        raise HTTPException(status_code=404, detail="Data center not found")
    
    return dc


@app.delete("/api/data-centers/{dc_id}", tags=["Data Centers"])
@limiter.limit("20/minute")
async def delete_data_center(
    request: Request,
    dc_id: str,
    current_user: Dict = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Deactivate a data center (soft delete)"""
    organization_id = current_user["organization_id"]
    success = data_center_service.delete_data_center(db, organization_id, dc_id)
    
    if not success:
        raise HTTPException(status_code=404, detail="Data center not found")
    
    return {"message": "Data center deactivated successfully"}
