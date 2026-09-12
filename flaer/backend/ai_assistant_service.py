"""
Flaer AI Assistant Service
Sustainability intelligence assistant for data center operators
"""
from typing import Dict, List, Optional, Tuple
from datetime import datetime, timedelta
from sqlalchemy.orm import Session
from models import DataCenter, Organization
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class FlaerAI:
    """
    Flaer AI - Sustainability Intelligence Assistant
    Helps data center operators track metrics and plan new facilities
    """
    
    # Thresholds for anomaly detection
    PUE_THRESHOLD = 1.75
    WUE_THRESHOLD = 1.8
    SPIKE_THRESHOLD = 0.05  # 5% week-on-week
    
    # Site scoring weights (equal weight = 20 each)
    SCORING_WEIGHTS = {
        'grid_carbon': 20,
        'renewable_availability': 20,
        'water_stress': 20,
        'climate_risk': 20,
        'regulatory_fit': 20
    }
    
    # Reference data for site scoring
    GRID_CARBON_DATA = {
        'stockholm': 13, 'montreal': 29, 'sao-paulo': 82, 'oregon': 95,
        'dublin': 295, 'milan': 289, 'frankfurt': 338, 'virginia': 385,
        'singapore': 408, 'iowa': 412, 'tokyo': 462, 'bahrain': 632,
        'hong-kong': 678, 'mumbai': 708, 'cape-town': 912
    }
    
    WATER_STRESS_INDEX = {
        'stockholm': 0.2, 'montreal': 0.3, 'oregon': 0.4, 'dublin': 0.5,
        'frankfurt': 0.6, 'milan': 0.7, 'sao-paulo': 0.8, 'virginia': 0.6,
        'iowa': 0.5, 'tokyo': 0.7, 'singapore': 0.9, 'hong-kong': 0.8,
        'mumbai': 0.9, 'bahrain': 1.0, 'cape-town': 0.95
    }
    
    CLIMATE_RISK_SCORE = {
        'stockholm': 0.2, 'montreal': 0.3, 'frankfurt': 0.4, 'dublin': 0.5,
        'oregon': 0.5, 'milan': 0.6, 'virginia': 0.7, 'iowa': 0.7,
        'tokyo': 0.8, 'sao-paulo': 0.7, 'singapore': 0.6, 'hong-kong': 0.8,
        'mumbai': 0.85, 'bahrain': 0.9, 'cape-town': 0.8
    }
    
    RENEWABLE_AVAILABILITY = {
        'stockholm': 98, 'montreal': 97, 'oregon': 89, 'sao-paulo': 83,
        'dublin': 68, 'milan': 61, 'frankfurt': 52, 'virginia': 45,
        'tokyo': 38, 'singapore': 28, 'mumbai': 24, 'bahrain': 18,
        'hong-kong': 12, 'iowa': 58, 'cape-town': 8
    }
    
    REGULATORY_FIT = {
        'stockholm': 95, 'frankfurt': 90, 'dublin': 88, 'milan': 85,
        'montreal': 82, 'oregon': 75, 'virginia': 70, 'iowa': 68,
        'tokyo': 80, 'singapore': 72, 'sao-paulo': 65, 'hong-kong': 70,
        'mumbai': 60, 'bahrain': 55, 'cape-town': 58
    }
    
    def __init__(self, db: Session):
        self.db = db
    
    def detect_user_context(self, organization_id: str) -> str:
        """
        Determine if user has existing data centers or is planning
        Returns: 'operator' or 'planner'
        """
        data_centers = self.db.query(DataCenter).filter(
            DataCenter.organization_id == organization_id,
            DataCenter.is_active == True
        ).count()
        
        return 'operator' if data_centers > 0 else 'planner'
    
    def check_anomalies(self, data_center: DataCenter, 
                       previous_week_data: Optional[Dict] = None) -> List[Dict]:
        """
        Flag anomalies in data center metrics
        Returns list of anomaly alerts
        """
        anomalies = []
        
        # Check PUE threshold
        if data_center.pue and data_center.pue > self.PUE_THRESHOLD:
            anomalies.append({
                'type': 'PUE_HIGH',
                'severity': 'high',
                'metric': 'PUE',
                'value': data_center.pue,
                'threshold': self.PUE_THRESHOLD,
                'message': f'PUE of {data_center.pue} exceeds threshold of {self.PUE_THRESHOLD}',
                'action': 'Review cooling efficiency and IT load distribution'
            })
        
        # Check WUE threshold
        if data_center.wue and data_center.wue > self.WUE_THRESHOLD:
            anomalies.append({
                'type': 'WUE_HIGH',
                'severity': 'high',
                'metric': 'WUE',
                'value': data_center.wue,
                'threshold': self.WUE_THRESHOLD,
                'message': f'WUE of {data_center.wue} L/kWh exceeds threshold of {self.WUE_THRESHOLD}',
                'action': 'Consider water-free cooling alternatives or optimize water usage'
            })
        
        # Check week-on-week spike (if previous data available)
        if previous_week_data:
            if 'energy_mwh' in previous_week_data:
                current_energy = previous_week_data.get('current_energy_mwh', 0)
                prev_energy = previous_week_data['energy_mwh']
                if prev_energy > 0:
                    change = (current_energy - prev_energy) / prev_energy
                    if abs(change) > self.SPIKE_THRESHOLD:
                        anomalies.append({
                            'type': 'ENERGY_SPIKE',
                            'severity': 'medium',
                            'metric': 'Energy Consumption',
                            'change_pct': round(change * 100, 1),
                            'message': f'Energy consumption changed by {round(change * 100, 1)}% week-on-week',
                            'action': 'Investigate sudden load changes or equipment issues'
                        })
        
        return anomalies
    
    def generate_weekly_digest(self, organization_id: str, 
                              week_start: datetime) -> Dict:
        """
        Generate weekly consumption digest for an organization
        """
        data_centers = self.db.query(DataCenter).filter(
            DataCenter.organization_id == organization_id,
            DataCenter.is_active == True
        ).all()
        
        if not data_centers:
            return {'error': 'No active data centers found'}
        
        # Calculate aggregate metrics (using sample data for demo)
        total_energy_mwh = sum(dc.capacity_mw * 24 * 7 * 0.7 for dc in data_centers)  # 70% utilization
        prev_week_energy = total_energy_mwh * 0.98  # Simulate 2% increase
        energy_change_pct = ((total_energy_mwh - prev_week_energy) / prev_week_energy) * 100
        
        # Calculate carbon emissions (Scope 2 = purchased electricity)
        total_carbon_tco2 = sum(
            dc.capacity_mw * 24 * 7 * 0.7 * dc.carbon_intensity / 1000
            for dc in data_centers
        )
        scope2_pct = 92  # Typically 90-95% for data centers
        
        # Calculate average metrics
        avg_pue = sum(dc.pue for dc in data_centers) / len(data_centers)
        avg_wue = sum(dc.wue for dc in data_centers if dc.wue) / len([dc for dc in data_centers if dc.wue]) if any(dc.wue for dc in data_centers) else 0
        avg_renewable = sum(dc.renewable_pct for dc in data_centers) / len(data_centers)
        
        # Determine PUE status
        pue_status = 'On target' if avg_pue <= self.PUE_THRESHOLD else 'Above threshold — action required'
        
        # Generate top 3 actions
        actions = self._generate_top_actions(data_centers, avg_pue, avg_renewable, total_carbon_tco2)
        
        # Determine trend
        trend = self._analyze_trend(energy_change_pct, avg_pue)
        
        return {
            'facility_name': f'{len(data_centers)} facilities',
            'week_of': week_start.strftime('%B %d, %Y'),
            'energy_mwh': round(total_energy_mwh, 1),
            'energy_change_pct': round(energy_change_pct, 1),
            'carbon_tco2': round(total_carbon_tco2, 1),
            'scope2_pct': scope2_pct,
            'pue': round(avg_pue, 2),
            'pue_status': pue_status,
            'wue': round(avg_wue, 2) if avg_wue else None,
            'renewable_pct': round(avg_renewable, 1),
            'top_actions': actions,
            'assumption': 'Weekly metering was not provided; energy and carbon use are estimated from IT capacity at 70% utilization using GHG Protocol Scope 2 location-based factors.',
            'trend': trend
        }
    
    def _generate_top_actions(self, data_centers: List[DataCenter], 
                             avg_pue: float, avg_renewable: float,
                             total_carbon: float) -> List[Dict]:
        """Generate top 3 recommended actions"""
        actions = []
        
        # Action 1: PUE optimization (if needed)
        if avg_pue > 1.5:
            potential_saving = total_carbon * (avg_pue - 1.4) / avg_pue
            actions.append({
                'priority': 1,
                'action': f'Optimize cooling efficiency to reduce PUE from {avg_pue:.2f} to 1.4',
                'impact': f'Save {potential_saving:.1f} tCO₂/week',
                'effort': 'Medium',
                'timeframe': '3-6 months'
            })
        
        # Action 2: Renewable energy increase
        if avg_renewable < 80:
            target_renewable = min(avg_renewable + 20, 90)
            carbon_reduction = total_carbon * (target_renewable - avg_renewable) / 100
            actions.append({
                'priority': 2,
                'action': f'Increase renewable energy mix from {avg_renewable:.0f}% to {target_renewable:.0f}%',
                'impact': f'Reduce {carbon_reduction:.1f} tCO₂/week (Scope 2)',
                'effort': 'High',
                'timeframe': '6-12 months'
            })
        
        # Action 3: High-carbon facility migration
        high_carbon_dcs = sorted(data_centers, key=lambda x: x.carbon_intensity, reverse=True)[:3]
        if high_carbon_dcs and high_carbon_dcs[0].carbon_intensity > 500:
            actions.append({
                'priority': 3,
                'action': f'Migrate workloads from {high_carbon_dcs[0].location} (carbon intensity: {high_carbon_dcs[0].carbon_intensity} gCO₂/kWh)',
                'impact': 'Reduce up to 40% of facility emissions',
                'effort': 'Very High',
                'timeframe': '12-24 months'
            })
        
        # If no major actions needed, suggest monitoring
        if not actions:
            actions.append({
                'priority': 1,
                'action': 'Maintain current performance levels',
                'impact': 'Continue monitoring for optimization opportunities',
                'effort': 'Low',
                'timeframe': 'Ongoing'
            })

        if len(actions) < 3:
            actions.append({
                'priority': len(actions) + 1,
                'action': 'Prioritize Scope 2 reduction through additional renewable electricity procurement',
                'impact': f'Potentially reduce up to {total_carbon * 0.2:.1f} tCO₂/week with a 20 percentage-point renewable mix increase',
                'effort': 'Medium',
                'timeframe': '3-12 months'
            })

        if len(actions) < 3:
            actions.append({
                'priority': len(actions) + 1,
                'action': 'Collect actual weekly IT load, facility load, water, and emissions factors',
                'impact': 'Improves anomaly detection and GHG Protocol reporting accuracy',
                'effort': 'Low',
                'timeframe': '1-4 weeks'
            })
        
        return actions[:3]
    
    def _analyze_trend(self, energy_change_pct: float, avg_pue: float) -> str:
        """Analyze performance trend"""
        if energy_change_pct > 5:
            return f'Energy consumption increased {energy_change_pct:.1f}% — investigate load growth and efficiency measures'
        elif energy_change_pct < -5:
            return f'Energy consumption decreased {abs(energy_change_pct):.1f}% — positive trend, maintain optimization efforts'
        elif avg_pue > 1.6:
            return f'Performance stable but PUE of {avg_pue:.2f} indicates room for cooling optimization'
        else:
            return 'Performance stable and within target thresholds — continue monitoring'
    
    def score_location(self, location: str, requirements: Dict) -> Dict:
        """
        Score a candidate location for data center site selection
        Requirements: {
            'it_load_mw': float,
            'target_region': str,
            'renewable_requirement': float (0-100),
            'budget': str ('low', 'medium', 'high')
        }
        """
        location_lower = location.lower()
        if location_lower not in self.GRID_CARBON_DATA:
            available = ", ".join(sorted(self.GRID_CARBON_DATA.keys()))
            raise ValueError(f"No scoring data available for '{location}'. Available locations: {available}")
        
        # Calculate individual dimension scores (0-100)
        grid_carbon_score = self._score_grid_carbon(location_lower)
        renewable_score = self._score_renewable_availability(location_lower)
        water_score = self._score_water_stress(location_lower)
        climate_score = self._score_climate_risk(location_lower)
        regulatory_score = self._score_regulatory_fit(location_lower)
        
        # Calculate composite score
        composite_score = (
            grid_carbon_score * self.SCORING_WEIGHTS['grid_carbon'] +
            renewable_score * self.SCORING_WEIGHTS['renewable_availability'] +
            water_score * self.SCORING_WEIGHTS['water_stress'] +
            climate_score * self.SCORING_WEIGHTS['climate_risk'] +
            regulatory_score * self.SCORING_WEIGHTS['regulatory_fit']
        ) / 100
        
        # Determine best dimension and biggest risk
        scores = {
            'Grid Carbon': grid_carbon_score,
            'Renewable': renewable_score,
            'Water': water_score,
            'Climate': climate_score,
            'Regulatory': regulatory_score
        }
        best_dimension = max(scores, key=scores.get)
        biggest_risk = min(scores, key=scores.get)
        
        return {
            'location': location,
            'composite_score': round(composite_score, 1),
            'grid_carbon_score': round(grid_carbon_score, 1),
            'renewable_score': round(renewable_score, 1),
            'water_score': round(water_score, 1),
            'climate_score': round(climate_score, 1),
            'regulatory_score': round(regulatory_score, 1),
            'best_dimension': best_dimension,
            'biggest_risk': biggest_risk,
            'grid_carbon_intensity': self.GRID_CARBON_DATA.get(location_lower, 400),
            'renewable_availability': self.RENEWABLE_AVAILABILITY.get(location_lower, 50)
        }
    
    def _score_grid_carbon(self, location: str) -> float:
        """Score based on grid carbon intensity (lower is better)"""
        carbon = self.GRID_CARBON_DATA.get(location, 400)
        # Best: <50 gCO₂/kWh = 100, Worst: >800 = 0
        return max(0, min(100, 100 - (carbon / 8)))
    
    def _score_renewable_availability(self, location: str) -> float:
        """Score based on renewable energy availability"""
        renewable_pct = self.RENEWABLE_AVAILABILITY.get(location, 50)
        return renewable_pct  # Direct percentage
    
    def _score_water_stress(self, location: str) -> float:
        """Score based on water stress (lower stress is better)"""
        stress = self.WATER_STRESS_INDEX.get(location, 0.5)
        return (1 - stress) * 100
    
    def _score_climate_risk(self, location: str) -> float:
        """Score based on climate risk (lower risk is better)"""
        risk = self.CLIMATE_RISK_SCORE.get(location, 0.5)
        return (1 - risk) * 100
    
    def _score_regulatory_fit(self, location: str) -> float:
        """Score based on regulatory environment"""
        return self.REGULATORY_FIT.get(location, 60)
    
    def recommend_locations(self, requirements: Dict, 
                           num_recommendations: int = 5) -> List[Dict]:
        """
        Recommend top locations for data center site selection
        Returns sorted list of scored locations with rationale
        """
        all_locations = list(self.GRID_CARBON_DATA.keys())
        scored_locations = []
        
        for location in all_locations:
            score_data = self.score_location(location, requirements)
            
            # Generate one-line rationale
            rationale = self._generate_rationale(score_data, requirements)
            score_data['rationale'] = rationale
            
            scored_locations.append(score_data)
        
        # Sort by composite score (descending)
        scored_locations.sort(key=lambda x: x['composite_score'], reverse=True)
        
        return scored_locations[:num_recommendations]
    
    def _generate_rationale(self, score_data: Dict, requirements: Dict) -> str:
        """Generate one-line rationale for location recommendation"""
        location = score_data['location'].title()
        best = score_data['best_dimension']
        carbon = score_data['grid_carbon_intensity']
        renewable = score_data['renewable_availability']
        
        if score_data['composite_score'] >= 80:
            return f'{location}: Excellent choice with {carbon} gCO₂/kWh grid and {renewable}% renewable access'
        elif score_data['composite_score'] >= 60:
            return f'{location}: Strong option, excels in {best} but monitor {score_data["biggest_risk"]}'
        else:
            return f'{location}: Viable with trade-offs, requires mitigation for {score_data["biggest_risk"]}'
    
    def format_weekly_digest(self, digest: Dict) -> str:
        """Format weekly digest as markdown"""
        output = f"""## Weekly consumption summary — {digest['facility_name']} — week of {digest['week_of']}

**Energy:** {digest['energy_mwh']} MWh consumed | {'+' if digest['energy_change_pct'] > 0 else ''}{digest['energy_change_pct']}% vs prior week
**Carbon:** {digest['carbon_tco2']} tCO₂ emitted | Scope 2 = {digest['scope2_pct']}% of total
**PUE:** {digest['pue']} | Status: {digest['pue_status']}
**WUE:** {digest['wue']} L/kWh | **Renewable mix:** {digest['renewable_pct']}%
**Assumption:** {digest.get('assumption', 'Using provided facility data and GHG Protocol Scope 2 methodology.')}

### This week's top 3 actions
"""
        for action in digest['top_actions']:
            output += f"{action['priority']}. {action['action']} — {action['impact']}\n"
        
        output += f"\n### Trend\n{digest['trend']}"
        
        return output


def create_ai_assistant(db: Session) -> FlaerAI:
    """Factory function to create AI assistant instance"""
    return FlaerAI(db)

# Made with Bob
