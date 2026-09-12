"""
Data Center Management Service
Handles CRUD operations for data centers with real-time metrics integration
"""
from typing import List, Dict, Optional
from datetime import datetime, timezone
from sqlalchemy.orm import Session
from models import DataCenter as DBDataCenter, Organization
from pydantic import BaseModel, Field, validator
import uuid


class DataCenterCreate(BaseModel):
    """Schema for creating a new data center"""
    name: str = Field(..., min_length=1, max_length=255, description="Data center name")
    location: str = Field(..., min_length=1, max_length=255, description="Physical location (city, country)")
    latitude: Optional[float] = Field(None, ge=-90, le=90, description="Latitude coordinate")
    longitude: Optional[float] = Field(None, ge=-180, le=180, description="Longitude coordinate")
    capacity_mw: int = Field(..., ge=1, le=10000, description="Total capacity in MW")
    pue: float = Field(..., ge=1.0, le=3.0, description="Power Usage Effectiveness")
    wue: Optional[float] = Field(None, ge=0.1, le=10.0, description="Water Usage Effectiveness (L/kWh)")
    cue: Optional[float] = Field(None, ge=0.0, le=2.0, description="Carbon Usage Effectiveness")
    carbon_intensity: float = Field(..., ge=0, le=1000, description="Grid carbon intensity (gCO2/kWh)")
    renewable_pct: int = Field(0, ge=0, le=100, description="Renewable energy percentage")
    
    # Optional monitoring integration
    monitoring_api_url: Optional[str] = Field(None, description="API endpoint for real-time metrics")
    monitoring_api_key: Optional[str] = Field(None, description="API key for monitoring system")
    
    @validator('pue')
    def validate_pue(cls, v):
        if v < 1.0:
            raise ValueError('PUE cannot be less than 1.0')
        if v > 2.5:
            raise ValueError('PUE above 2.5 indicates severe inefficiency - please verify')
        return v


class DataCenterUpdate(BaseModel):
    """Schema for updating data center metrics"""
    name: Optional[str] = Field(None, min_length=1, max_length=255)
    location: Optional[str] = Field(None, min_length=1, max_length=255)
    latitude: Optional[float] = Field(None, ge=-90, le=90)
    longitude: Optional[float] = Field(None, ge=-180, le=180)
    capacity_mw: Optional[int] = Field(None, ge=1, le=10000)
    pue: Optional[float] = Field(None, ge=1.0, le=3.0)
    wue: Optional[float] = Field(None, ge=0.1, le=10.0)
    cue: Optional[float] = Field(None, ge=0.0, le=2.0)
    carbon_intensity: Optional[float] = Field(None, ge=0, le=1000)
    renewable_pct: Optional[int] = Field(None, ge=0, le=100)
    is_active: Optional[bool] = None


class DataCenterResponse(BaseModel):
    """Schema for data center response"""
    id: str
    organization_id: str
    name: str
    location: str
    latitude: Optional[float]
    longitude: Optional[float]
    capacity_mw: int
    pue: float
    wue: Optional[float]
    cue: Optional[float]
    carbon_intensity: float
    renewable_pct: int
    risk_level: str
    annual_water: Optional[str]
    annual_co2: Optional[str]
    forecast_2035: Optional[str]
    csrd_exposure: Optional[str]
    is_active: bool
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True


class DataCenterService:
    """Service for managing data centers"""
    
    @staticmethod
    def calculate_risk_level(pue: float, carbon_intensity: float, renewable_pct: int) -> str:
        """Calculate risk level based on metrics"""
        risk_score = 0
        
        # PUE scoring (0-40 points)
        if pue >= 1.75:
            risk_score += 40
        elif pue >= 1.5:
            risk_score += 25
        elif pue >= 1.3:
            risk_score += 10
        
        # Carbon intensity scoring (0-40 points)
        if carbon_intensity >= 400:
            risk_score += 40
        elif carbon_intensity >= 300:
            risk_score += 25
        elif carbon_intensity >= 200:
            risk_score += 10
        
        # Renewable percentage scoring (0-20 points)
        if renewable_pct < 30:
            risk_score += 20
        elif renewable_pct < 50:
            risk_score += 10
        
        # Determine risk level
        if risk_score >= 60:
            return "high"
        elif risk_score >= 30:
            return "medium"
        else:
            return "low"
    
    @staticmethod
    def calculate_annual_metrics(capacity_mw: int, pue: float, carbon_intensity: float, 
                                 wue: Optional[float] = None) -> Dict[str, str]:
        """Calculate annual water and CO2 metrics"""
        # Annual energy consumption (MWh)
        # Assume 8760 hours/year and 70% average utilization
        annual_energy_mwh = capacity_mw * 8760 * 0.7
        
        # Annual CO2 (tCO2e)
        annual_co2 = (annual_energy_mwh * carbon_intensity * pue) / 1000
        
        # Annual water (m³) - if WUE is provided
        annual_water = None
        if wue:
            # Convert MWh to kWh and multiply by WUE (L/kWh), then convert to m³
            annual_water_m3 = (annual_energy_mwh * 1000 * wue * pue) / 1000
            annual_water = f"{annual_water_m3/1_000_000:.1f}M m³"
        
        return {
            "annual_co2": f"{annual_co2/1000:.0f}K tCO₂e",
            "annual_water": annual_water
        }
    
    @staticmethod
    def calculate_forecast_2035(carbon_intensity: float, renewable_pct: int) -> str:
        """Estimate 2035 emissions trajectory"""
        # Simple heuristic based on current state
        if renewable_pct >= 80 and carbon_intensity < 100:
            return "-25%"
        elif renewable_pct >= 60 and carbon_intensity < 250:
            return "-15%"
        elif renewable_pct >= 40:
            return "-5%"
        elif carbon_intensity > 400:
            return "+15%"
        else:
            return "+5%"
    
    @staticmethod
    def calculate_csrd_exposure(location: str, carbon_intensity: float) -> str:
        """Determine CSRD exposure level"""
        # EU locations have high CSRD exposure
        eu_keywords = ["EU", "Europe", "Germany", "France", "Sweden", "Poland", "Spain", 
                      "Italy", "Netherlands", "Belgium", "Austria", "Denmark", "Finland"]
        
        is_eu = any(keyword.lower() in location.lower() for keyword in eu_keywords)
        
        if is_eu:
            return "High"
        elif carbon_intensity > 400:
            return "Medium"
        else:
            return "Low"
    
    @staticmethod
    def create_data_center(db: Session, organization_id: str, data: DataCenterCreate) -> DBDataCenter:
        """Create a new data center"""
        # Calculate derived metrics
        risk_level = DataCenterService.calculate_risk_level(
            data.pue, data.carbon_intensity, data.renewable_pct
        )
        
        annual_metrics = DataCenterService.calculate_annual_metrics(
            data.capacity_mw, data.pue, data.carbon_intensity, data.wue
        )
        
        forecast_2035 = DataCenterService.calculate_forecast_2035(
            data.carbon_intensity, data.renewable_pct
        )
        
        csrd_exposure = DataCenterService.calculate_csrd_exposure(
            data.location, data.carbon_intensity
        )
        
        # Create data center
        dc = DBDataCenter(
            id=str(uuid.uuid4()),
            organization_id=organization_id,
            name=data.name,
            location=data.location,
            capacity_mw=data.capacity_mw,
            pue=data.pue,
            wue=data.wue,
            cue=data.cue,
            carbon_intensity=data.carbon_intensity,
            renewable_pct=data.renewable_pct,
            risk_level=risk_level,
            annual_water=annual_metrics["annual_water"],
            annual_co2=annual_metrics["annual_co2"],
            forecast_2035=forecast_2035,
            csrd_exposure=csrd_exposure,
            is_active=True
        )
        
        db.add(dc)
        db.commit()
        db.refresh(dc)
        
        return dc
    
    @staticmethod
    def get_data_centers(db: Session, organization_id: str, 
                        include_inactive: bool = False) -> List[DBDataCenter]:
        """Get all data centers for an organization"""
        query = db.query(DBDataCenter).filter(
            DBDataCenter.organization_id == organization_id
        )
        
        if not include_inactive:
            query = query.filter(DBDataCenter.is_active == True)
        
        return query.order_by(DBDataCenter.created_at.desc()).all()
    
    @staticmethod
    def get_data_center(db: Session, organization_id: str, dc_id: str) -> Optional[DBDataCenter]:
        """Get a specific data center"""
        return db.query(DBDataCenter).filter(
            DBDataCenter.id == dc_id,
            DBDataCenter.organization_id == organization_id
        ).first()
    
    @staticmethod
    def update_data_center(db: Session, organization_id: str, dc_id: str, 
                          data: DataCenterUpdate) -> Optional[DBDataCenter]:
        """Update a data center"""
        dc = DataCenterService.get_data_center(db, organization_id, dc_id)
        if not dc:
            return None
        
        # Update fields
        update_data = data.dict(exclude_unset=True)
        
        # Recalculate derived metrics if relevant fields changed
        if any(k in update_data for k in ['pue', 'carbon_intensity', 'renewable_pct']):
            pue = update_data.get('pue', dc.pue)
            carbon_intensity = update_data.get('carbon_intensity', dc.carbon_intensity)
            renewable_pct = update_data.get('renewable_pct', dc.renewable_pct)
            
            update_data['risk_level'] = DataCenterService.calculate_risk_level(
                pue, carbon_intensity, renewable_pct
            )
            
            update_data['forecast_2035'] = DataCenterService.calculate_forecast_2035(
                carbon_intensity, renewable_pct
            )
        
        if any(k in update_data for k in ['capacity_mw', 'pue', 'carbon_intensity', 'wue']):
            capacity_mw = update_data.get('capacity_mw', dc.capacity_mw)
            pue = update_data.get('pue', dc.pue)
            carbon_intensity = update_data.get('carbon_intensity', dc.carbon_intensity)
            wue = update_data.get('wue', dc.wue)
            
            annual_metrics = DataCenterService.calculate_annual_metrics(
                capacity_mw, pue, carbon_intensity, wue
            )
            update_data['annual_co2'] = annual_metrics['annual_co2']
            update_data['annual_water'] = annual_metrics['annual_water']
        
        if 'location' in update_data or 'carbon_intensity' in update_data:
            location = update_data.get('location', dc.location)
            carbon_intensity = update_data.get('carbon_intensity', dc.carbon_intensity)
            update_data['csrd_exposure'] = DataCenterService.calculate_csrd_exposure(
                location, carbon_intensity
            )
        
        # Apply updates
        for key, value in update_data.items():
            setattr(dc, key, value)
        
        dc.updated_at = datetime.now(timezone.utc)
        db.commit()
        db.refresh(dc)
        
        return dc
    
    @staticmethod
    def delete_data_center(db: Session, organization_id: str, dc_id: str) -> bool:
        """Soft delete a data center"""
        dc = DataCenterService.get_data_center(db, organization_id, dc_id)
        if not dc:
            return False
        
        dc.is_active = False
        dc.updated_at = datetime.now(timezone.utc)
        db.commit()
        
        return True
    
    @staticmethod
    def get_portfolio_summary(db: Session, organization_id: str) -> Dict:
        """Get portfolio-level summary statistics"""
        data_centers = DataCenterService.get_data_centers(db, organization_id)
        
        if not data_centers:
            return {
                "total_facilities": 0,
                "total_capacity_mw": 0,
                "avg_pue": 0,
                "avg_carbon_intensity": 0,
                "avg_renewable_pct": 0,
                "risk_breakdown": {"high": 0, "medium": 0, "low": 0}
            }
        
        total_capacity = sum(dc.capacity_mw for dc in data_centers)
        
        # Weighted averages by capacity
        avg_pue = sum(dc.pue * dc.capacity_mw for dc in data_centers) / total_capacity
        avg_carbon = sum(dc.carbon_intensity * dc.capacity_mw for dc in data_centers) / total_capacity
        avg_renewable = sum(dc.renewable_pct * dc.capacity_mw for dc in data_centers) / total_capacity
        
        risk_breakdown = {
            "high": sum(1 for dc in data_centers if dc.risk_level == "high"),
            "medium": sum(1 for dc in data_centers if dc.risk_level == "medium"),
            "low": sum(1 for dc in data_centers if dc.risk_level == "low")
        }
        
        return {
            "total_facilities": len(data_centers),
            "total_capacity_mw": total_capacity,
            "avg_pue": round(avg_pue, 2),
            "avg_carbon_intensity": round(avg_carbon, 0),
            "avg_renewable_pct": round(avg_renewable, 0),
            "risk_breakdown": risk_breakdown
        }


# Export service instance
data_center_service = DataCenterService()

# Made with Bob
