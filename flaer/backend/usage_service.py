"""
Usage tracking and limits enforcement service
"""
from typing import Dict, Optional
from datetime import datetime, timedelta, timezone
from billing_service import PRICING_TIERS


class UsageService:
    """Track and enforce usage limits"""
    
    @staticmethod
    def check_data_center_limit(organization: Dict) -> bool:
        """Check if organization can add more data centers"""
        tier_limits = PRICING_TIERS.get(organization["plan_tier"], PRICING_TIERS["free"])
        current_count = organization.get("data_centers_count", 0)
        max_allowed = tier_limits["max_data_centers"]
        
        return current_count < max_allowed
    
    @staticmethod
    def check_user_limit(organization: Dict) -> bool:
        """Check if organization can add more users"""
        tier_limits = PRICING_TIERS.get(organization["plan_tier"], PRICING_TIERS["free"])
        current_count = organization.get("users_count", 0)
        max_allowed = tier_limits["max_users"]
        
        return current_count < max_allowed
    
    @staticmethod
    def check_api_limit(organization: Dict, api_usage_count: int) -> bool:
        """Check if organization is within API call limits"""
        tier_limits = PRICING_TIERS.get(organization["plan_tier"], PRICING_TIERS["free"])
        max_allowed = tier_limits["api_calls_per_month"]
        
        return api_usage_count < max_allowed
    
    @staticmethod
    def get_usage_stats(organization_id: str, db) -> Dict:
        """Get usage statistics for an organization"""
        from models import DataCenter, User, APIUsage
        
        # Count data centers
        data_centers_count = db.query(DataCenter).filter(
            DataCenter.organization_id == organization_id,
            DataCenter.is_active == True
        ).count()
        
        # Count users
        users_count = db.query(User).filter(
            User.organization_id == organization_id,
            User.is_active == True
        ).count()
        
        # Count API calls this month
        start_of_month = datetime.now(timezone.utc).replace(
            day=1, hour=0, minute=0, second=0, microsecond=0
        )
        api_calls_count = db.query(APIUsage).filter(
            APIUsage.organization_id == organization_id,
            APIUsage.timestamp >= start_of_month
        ).count()
        
        return {
            "data_centers": data_centers_count,
            "users": users_count,
            "api_calls_this_month": api_calls_count
        }
    
    @staticmethod
    def track_api_call(
        organization_id: str,
        endpoint: str,
        method: str,
        status_code: int,
        response_time_ms: int,
        user_id: Optional[str] = None,
        ip_address: Optional[str] = None,
        db = None
    ):
        """Track an API call for usage monitoring"""
        from models import APIUsage
        
        if db is None:
            return
        
        usage = APIUsage(
            organization_id=organization_id,
            endpoint=endpoint,
            method=method,
            status_code=status_code,
            response_time_ms=response_time_ms,
            user_id=user_id,
            ip_address=ip_address
        )
        
        db.add(usage)
        db.commit()
    
    @staticmethod
    def get_limits_info(organization: Dict) -> Dict:
        """Get limits information for an organization"""
        tier_limits = PRICING_TIERS.get(organization["plan_tier"], PRICING_TIERS["free"])
        
        return {
            "plan_tier": organization["plan_tier"],
            "limits": {
                "data_centers": {
                    "max": tier_limits["max_data_centers"],
                    "current": organization.get("data_centers_count", 0)
                },
                "users": {
                    "max": tier_limits["max_users"],
                    "current": organization.get("users_count", 0)
                },
                "api_calls": {
                    "max": tier_limits["api_calls_per_month"],
                    "current": organization.get("api_calls_count", 0)
                }
            },
            "features": tier_limits["features"]
        }
    
    @staticmethod
    def has_feature(organization: Dict, feature: str) -> bool:
        """Check if organization has access to a feature"""
        tier_limits = PRICING_TIERS.get(organization["plan_tier"], PRICING_TIERS["free"])
        features = tier_limits["features"]
        
        # "all_features" grants access to everything
        if "all_features" in features:
            return True
        
        return feature in features


# Singleton instance
usage_service = UsageService()

# Made with Bob
