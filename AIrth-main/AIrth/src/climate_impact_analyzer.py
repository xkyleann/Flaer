import numpy as np
from typing import Dict, Tuple, List
from dataclasses import dataclass
from enum import Enum


class ClimateZone(Enum):
    """Climate zone classifications"""
    ARCTIC = "Arctic"
    SUBARCTIC = "Subarctic"
    TEMPERATE = "Temperate"
    SUBTROPICAL = "Subtropical"
    TROPICAL = "Tropical"
    ARID = "Arid"
    MEDITERRANEAN = "Mediterranean"


class WaterStressLevel(Enum):
    """Water stress classifications"""
    LOW = "Low"
    LOW_MEDIUM = "Low-Medium"
    MEDIUM_HIGH = "Medium-High"
    HIGH = "High"
    EXTREMELY_HIGH = "Extremely High"


@dataclass
class ClimateData:
    """Climate data for a location"""
    zone: ClimateZone
    avg_temp_celsius: float
    temp_range: Tuple[float, float]  # (min, max)
    humidity_avg: float
    free_cooling_days: int  # Days per year suitable for free cooling
    extreme_weather_risk: str
    seasonal_variation: str


@dataclass
class RegionalImpact:
    """Regional environmental impact data"""
    water_stress_level: WaterStressLevel
    water_stress_score: float  # 0-5 scale
    grid_carbon_intensity: float  # kg CO2/kWh
    renewable_potential: Dict[str, float]  # Solar, wind, hydro percentages
    air_quality_index: int  # 0-500 scale
    population_density: int  # people per km²
    ecological_sensitivity: str  # Low, Medium, High


class ClimateImpactAnalyzer:
    """Analyze climate and environmental impacts based on data center location"""
    
    def __init__(self):
        self.climate_zones = self._initialize_climate_zones()
        self.water_stress_data = self._initialize_water_stress()
        self.grid_intensity_data = self._initialize_grid_intensity()
        
    def _initialize_climate_zones(self) -> Dict:
        """Initialize climate zone data by latitude ranges"""
        return {
            'arctic': {'lat_range': (66.5, 90), 'zone': ClimateZone.ARCTIC},
            'subarctic': {'lat_range': (50, 66.5), 'zone': ClimateZone.SUBARCTIC},
            'temperate': {'lat_range': (30, 50), 'zone': ClimateZone.TEMPERATE},
            'subtropical': {'lat_range': (23.5, 30), 'zone': ClimateZone.SUBTROPICAL},
            'tropical': {'lat_range': (0, 23.5), 'zone': ClimateZone.TROPICAL}
        }
    
    def _initialize_water_stress(self) -> Dict:
        """Initialize water stress data by region (simplified)"""
        # Based on WRI Aqueduct data - simplified for demonstration
        return {
            'north_america': {'stress': 2.5, 'level': WaterStressLevel.MEDIUM_HIGH},
            'europe': {'stress': 2.0, 'level': WaterStressLevel.LOW_MEDIUM},
            'asia': {'stress': 3.5, 'level': WaterStressLevel.HIGH},
            'middle_east': {'stress': 4.5, 'level': WaterStressLevel.EXTREMELY_HIGH},
            'africa': {'stress': 3.8, 'level': WaterStressLevel.HIGH},
            'south_america': {'stress': 1.5, 'level': WaterStressLevel.LOW},
            'oceania': {'stress': 2.8, 'level': WaterStressLevel.MEDIUM_HIGH}
        }
    
    def _initialize_grid_intensity(self) -> Dict:
        """Initialize grid carbon intensity by country/region"""
        # kg CO2 per kWh - based on real data
        return {
            'finland': 0.15, 'sweden': 0.18, 'norway': 0.12, 'france': 0.08,
            'germany': 0.38, 'uk': 0.28, 'netherlands': 0.35, 'spain': 0.38,
            'usa': 0.45, 'canada': 0.32, 'china': 0.65, 'india': 0.72,
            'japan': 0.48, 'south_korea': 0.52, 'australia': 0.82,
            'singapore': 0.42, 'uae': 0.55, 'brazil': 0.48, 'russia': 0.68,
            'south_africa': 0.88
        }
    
    def determine_climate_zone(self, latitude: float, longitude: float) -> ClimateZone:
        """Determine climate zone based on coordinates"""
        abs_lat = abs(latitude)
        
        if abs_lat >= 66.5:
            return ClimateZone.ARCTIC
        elif abs_lat >= 50:
            return ClimateZone.SUBARCTIC
        elif abs_lat >= 30:
            # Check for arid/mediterranean
            if -10 <= longitude <= 60 and 20 <= abs_lat <= 40:  # Mediterranean 
                return ClimateZone.MEDITERRANEAN
            elif abs_lat >= 35:  # Arid regions (I simplified it, maybe in the future I can add more details)
                return ClimateZone.ARID
            return ClimateZone.TEMPERATE
        elif abs_lat >= 23.5:
            return ClimateZone.SUBTROPICAL
        else:
            return ClimateZone.TROPICAL
    
    def get_climate_data(self, latitude: float, longitude: float) -> ClimateData:
        """Get comprehensive climate data for location"""
        zone = self.determine_climate_zone(latitude, longitude)
        
        # temperature based on latitude
        abs_lat = abs(latitude)
        base_temp = 30 - (abs_lat * 0.6) 
        
        climate_profiles = {
            ClimateZone.ARCTIC: {
                'avg_temp': -10, 'range': (-30, 10), 'humidity': 70,
                'free_cooling_days': 365, 'extreme_risk': 'Extreme cold, ice storms',
                'seasonal': 'Extreme seasonal variation'
            },
            ClimateZone.SUBARCTIC: {
                'avg_temp': 5, 'range': (-20, 25), 'humidity': 65,
                'free_cooling_days': 300, 'extreme_risk': 'Cold waves, heavy snow',
                'seasonal': 'High seasonal variation'
            },
            ClimateZone.TEMPERATE: {
                'avg_temp': 15, 'range': (-5, 30), 'humidity': 60,
                'free_cooling_days': 200, 'extreme_risk': 'Moderate storms, occasional extremes',
                'seasonal': 'Moderate seasonal variation'
            },
            ClimateZone.MEDITERRANEAN: {
                'avg_temp': 18, 'range': (5, 35), 'humidity': 55,
                'free_cooling_days': 180, 'extreme_risk': 'Heat waves, droughts',
                'seasonal': 'Moderate seasonal variation'
            },
            ClimateZone.SUBTROPICAL: {
                'avg_temp': 22, 'range': (10, 35), 'humidity': 70,
                'free_cooling_days': 120, 'extreme_risk': 'Hurricanes, heat waves',
                'seasonal': 'Low seasonal variation'
            },
            ClimateZone.TROPICAL: {
                'avg_temp': 27, 'range': (20, 35), 'humidity': 80,
                'free_cooling_days': 30, 'extreme_risk': 'Typhoons, extreme humidity',
                'seasonal': 'Minimal seasonal variation'
            },
            ClimateZone.ARID: {
                'avg_temp': 25, 'range': (5, 45), 'humidity': 30,
                'free_cooling_days': 150, 'extreme_risk': 'Extreme heat, dust storms',
                'seasonal': 'High temperature variation'
            }
        }
        
        profile = climate_profiles.get(zone, climate_profiles[ClimateZone.TEMPERATE])
        
        return ClimateData(
            zone=zone,
            avg_temp_celsius=profile['avg_temp'],
            temp_range=profile['range'],
            humidity_avg=profile['humidity'],
            free_cooling_days=profile['free_cooling_days'],
            extreme_weather_risk=profile['extreme_risk'],
            seasonal_variation=profile['seasonal']
        )
    
    def get_regional_impact(self, latitude: float, longitude: float) -> RegionalImpact:
        """Get regional environmental impact data"""

        region = self._determine_region(latitude, longitude)
        water_data = self.water_stress_data.get(region, {'stress': 2.5, 'level': WaterStressLevel.MEDIUM_HIGH})
        grid_intensity = self._estimate_grid_intensity(latitude, longitude)
        renewable_potential = self._estimate_renewable_potential(latitude, longitude)
        air_quality = self._estimate_air_quality(latitude, longitude)
        pop_density = self._estimate_population_density(latitude, longitude)
        ecological = self._determine_ecological_sensitivity(latitude, longitude)
        
        return RegionalImpact(
            water_stress_level=water_data['level'],
            water_stress_score=water_data['stress'],
            grid_carbon_intensity=grid_intensity,
            renewable_potential=renewable_potential,
            air_quality_index=air_quality,
            population_density=pop_density,
            ecological_sensitivity=ecological
        )
    
    def _determine_region(self, lat: float, lon: float) -> str:
        """Determine geographic region"""
        if lat > 35 and -130 < lon < -60:
            return 'north_america'
        elif lat > 35 and -10 < lon < 40:
            return 'europe'
        elif lat > 10 and 60 < lon < 150:
            return 'asia'
        elif 10 < lat < 40 and 25 < lon < 60:
            return 'middle_east'
        elif -35 < lat < 35 and -20 < lon < 55:
            return 'africa'
        elif -60 < lat < 15 and -85 < lon < -35:
            return 'south_america'
        else:
            return 'oceania'
    
    def _estimate_grid_intensity(self, lat: float, lon: float) -> float:
        """Estimate grid carbon intensity"""

        region = self._determine_region(lat, lon)
        base_intensity = {
            'north_america': 0.45, 'europe': 0.30, 'asia': 0.65,
            'middle_east': 0.55, 'africa': 0.70, 'south_america': 0.48,
            'oceania': 0.75
        }
        return base_intensity.get(region, 0.50)
    
    def _estimate_renewable_potential(self, lat: float, lon: float) -> Dict[str, float]:
        """Estimate renewable energy potential"""
        abs_lat = abs(lat)
        solar = max(20, 100 - abs_lat * 1.5)
        wind = 60 if 30 < abs_lat < 60 else 40
        hydro = 30
        
        # Normalize to 100%
        total = solar + wind + hydro
        return {
            'solar': round(solar / total * 100, 1),
            'wind': round(wind / total * 100, 1),
            'hydro': round(hydro / total * 100, 1)
        }
    
    def _estimate_air_quality(self, lat: float, lon: float) -> int:
        """Estimate air quality index (0-500, lower is better)"""
        region = self._determine_region(lat, lon)
        base_aqi = {
            'north_america': 80, 'europe': 60, 'asia': 150,
            'middle_east': 120, 'africa': 100, 'south_america': 70,
            'oceania': 50
        }
        return base_aqi.get(region, 100)
    
    def _estimate_population_density(self, lat: float, lon: float) -> int:
        """Estimate population density"""
        region = self._determine_region(lat, lon)
        density = {
            'north_america': 35, 'europe': 75, 'asia': 150,
            'middle_east': 45, 'africa': 45, 'south_america': 25,
            'oceania': 5
        }
        return density.get(region, 50)
    
    def _determine_ecological_sensitivity(self, lat: float, lon: float) -> str:
        """Determine ecological sensitivity of region"""
        abs_lat = abs(lat)
        
        if abs_lat < 10:  # Tropical rainforests
            return "High"
        elif abs_lat > 60:  # Arctic/Antarctic
            return "High"
        elif 20 < abs_lat < 35:  # Arid regions
            return "Medium-High"
        else:
            return "Medium"
    
    def calculate_heat_island_effect(self, power_mw: float, area_sqm: float) -> Dict:
        """Calculate urban heat island effect"""
        heat_output_w = power_mw * 1_000_000
        heat_flux = heat_output_w / area_sqm
        
        # Estimated temperature increase (simplified model)
        # Typical data center: 200-400 W/m² heat flux
        temp_increase = heat_flux / 100  # Rough estimate: 1°C per 100 W/m²
        affected_radius_km = np.sqrt(area_sqm / np.pi) / 1000 * 3 
        
        return {
            'heat_flux_w_per_m2': round(heat_flux, 1),
            'estimated_temp_increase_c': round(temp_increase, 2),
            'affected_radius_km': round(affected_radius_km, 2),
            'severity': 'High' if temp_increase > 2 else 'Moderate' if temp_increase > 1 else 'Low'
        }
    
    def calculate_water_impact(self, water_usage_liters_day: float, 
                               water_stress_score: float) -> Dict:
        """Calculate water resource impact"""
        # Annual water usage
        annual_liters = water_usage_liters_day * 365
        annual_cubic_meters = annual_liters / 1000
        
        # Olympic swimming pools equivalent (2,500 m³ each)
        olympic_pools = annual_cubic_meters / 2500
        
        # Impact severity based on water stress
        if water_stress_score > 4:
            severity = "Critical"
            impact_desc = "Severe strain on extremely water-stressed region"
        elif water_stress_score > 3:
            severity = "High"
            impact_desc = "Significant impact on water-stressed region"
        elif water_stress_score > 2:
            severity = "Moderate"
            impact_desc = "Moderate impact on regional water resources"
        else:
            severity = "Low"
            impact_desc = "Minimal impact on water-abundant region"
        
        return {
            'annual_cubic_meters': round(annual_cubic_meters, 0),
            'olympic_pools_equivalent': round(olympic_pools, 1),
            'severity': severity,
            'impact_description': impact_desc,
            'mitigation_priority': 'Urgent' if water_stress_score > 3.5 else 'High' if water_stress_score > 2.5 else 'Medium'
        }
    
    def generate_location_recommendations(self, climate_data: ClimateData, 
                                         regional_impact: RegionalImpact) -> List[Dict]:
        """Generate location-specific recommendations"""
        recommendations = []
        
        # Climate-based recommendations
        if climate_data.free_cooling_days > 250:
            recommendations.append({
                'category': 'Cooling Strategy',
                'priority': 'HIGH',
                'recommendation': 'Maximize free cooling utilization',
                'rationale': f'{climate_data.free_cooling_days} days/year suitable for free cooling',
                'potential_savings': '30-40% cooling energy reduction'
            })
        
        if climate_data.zone in [ClimateZone.TROPICAL, ClimateZone.SUBTROPICAL]:
            recommendations.append({
                'category': 'Renewable Energy',
                'priority': 'HIGH',
                'recommendation': 'Prioritize solar energy installation',
                'rationale': f'High solar potential in {climate_data.zone.value} climate',
                'potential_savings': '40-60% renewable energy achievable'
            })
        
        # Water stress recommendations
        if regional_impact.water_stress_level in [WaterStressLevel.HIGH, WaterStressLevel.EXTREMELY_HIGH]:
            recommendations.append({
                'category': 'Water Conservation',
                'priority': 'CRITICAL',
                'recommendation': 'Implement aggressive water recycling and air cooling',
                'rationale': f'{regional_impact.water_stress_level.value} water stress in region',
                'potential_savings': '50-70% water usage reduction'
            })
        
        # Grid intensity recommendations
        if regional_impact.grid_carbon_intensity > 0.6:
            recommendations.append({
                'category': 'Carbon Reduction',
                'priority': 'HIGH',
                'recommendation': 'Urgent renewable energy procurement needed',
                'rationale': f'High grid carbon intensity ({regional_impact.grid_carbon_intensity} kg CO₂/kWh)',
                'potential_savings': '60-80% emissions reduction with renewables'
            })
        
        # Renewable potential recommendations
        if regional_impact.renewable_potential['wind'] > 40:
            recommendations.append({
                'category': 'Renewable Energy',
                'priority': 'MEDIUM',
                'recommendation': 'Explore wind power purchase agreements',
                'rationale': f"High wind potential ({regional_impact.renewable_potential['wind']}%)",
                'potential_savings': '30-50% renewable energy from wind'
            })
        
        return recommendations


# usage and testing
if __name__ == "__main__":
    print("=" * 70)
    print("Climate & Environmental Impact Analyzer - Demo")
    print("=" * 70)
    
    analyzer = ClimateImpactAnalyzer()
    
    test_locations = [
        ("Google Hamina Finland", (60.5695, 27.1978), 120, 750000),
        ("China Telecom Inner Mongolia", (40.8414, 111.7519), 150, 1000000),
        ("Meta Singapore", (1.3521, 103.8198), 110, 700000),
        ("AWS Virginia", (38.9072, -77.0369), 200, 900000)
    ]
    
    for name, (lat, lon), power, area in test_locations:
        print(f"\n{'='*70}")
        print(f"📍 {name}")
        print(f"   Location: {lat:.4f}°, {lon:.4f}°")
        print(f"   Capacity: {power} MW, Area: {area:,} m²")
        print(f"{'='*70}")
        
        climate = analyzer.get_climate_data(lat, lon)
        print(f"\n🌡️  Climate Zone: {climate.zone.value}")
        print(f"   Average Temperature: {climate.avg_temp_celsius}°C")
        print(f"   Free Cooling Days: {climate.free_cooling_days}/year")
        print(f"   Extreme Weather Risk: {climate.extreme_weather_risk}")
        
        regional = analyzer.get_regional_impact(lat, lon)
        print(f"\n💧 Water Stress: {regional.water_stress_level.value} ({regional.water_stress_score}/5)")
        print(f"⚡ Grid Carbon Intensity: {regional.grid_carbon_intensity} kg CO₂/kWh")
        print(f"🌱 Renewable Potential: Solar {regional.renewable_potential['solar']}%, Wind {regional.renewable_potential['wind']}%")
        
        heat_island = analyzer.calculate_heat_island_effect(power, area)
        print(f"\n🔥 Heat Island Effect:")
        print(f"   Temperature Increase: {heat_island['estimated_temp_increase_c']}°C")
        print(f"   Affected Radius: {heat_island['affected_radius_km']} km")
        print(f"   Severity: {heat_island['severity']}")
        
        water_usage = power * 103333  # liters/day
        water_impact = analyzer.calculate_water_impact(water_usage, regional.water_stress_score)
        print(f"\n💦 Water Impact:")
        print(f"   Annual Usage: {water_impact['annual_cubic_meters']:,.0f} m³")
        print(f"   Equivalent: {water_impact['olympic_pools_equivalent']} Olympic pools")
        print(f"   Severity: {water_impact['severity']}")
        
        recommendations = analyzer.generate_location_recommendations(climate, regional)
        print(f"\n💡 Location-Specific Recommendations:")
        for i, rec in enumerate(recommendations, 1):
            print(f"   {i}. [{rec['priority']}] {rec['recommendation']}")
            print(f"      → {rec['rationale']}")
    
    print(f"\n{'='*70}")
    print("✓ Climate Impact Analysis Complete!")
    print(f"{'='*70}\n")
