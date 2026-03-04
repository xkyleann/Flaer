"""
AIrth - Sustainable Energy Platform
AI-powered digital platform that maps global data centers, predicts their 
long-term environmental impact, and recommends sustainable actions.
"""

import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestRegressor
from sklearn.preprocessing import StandardScaler
import matplotlib.pyplot as plt
import seaborn as sns
import folium
from datetime import datetime, timedelta
import json
from typing import Dict, List, Tuple, Optional
import warnings
warnings.filterwarnings('ignore')


class DataCenterModel:
    """Model for individual data center environmental metrics with advanced calculations"""
    
    def __init__(self, name: str, location: Tuple[float, float],
                 power_mw: float, area_sqm: float):
        self.name = name
        self.location = location  # (latitude, longitude)
        self.power_mw = power_mw
        self.area_sqm = area_sqm
        self.water_usage_liters_day = self._estimate_water_usage()
        self.carbon_emissions_tons_year = 0
        self.renewable_percentage = 0
        
        self.it_equipment_power_mw = power_mw * 0.6  # Assume 60% for IT equipment
        self.pue = 1.67  # Default industry average
        self.server_utilization = 0.65  # Default 65%
        self.electricity_price_per_kwh = 0.12  # USD per kWh
        self.carbon_price_per_ton = 50  # USD per ton CO2
        self.water_price_per_liter = 0.002  # USD per liter
        
    def _estimate_water_usage(self) -> float:
        """Estimate daily water usage based on power consumption"""
        # Based on China Telecom example: 150 MW uses 12-19M liters/day
        # Average: 15.5M liters for 150 MW = 103,333 liters per MW
        return self.power_mw * 103333
    
    def calculate_carbon_emissions(self, grid_carbon_intensity: float) -> float:
        """
        Calculate annual carbon emissions
        grid_carbon_intensity: kg CO2 per kWh
        """
        annual_energy_kwh = self.power_mw * 1000 * 24 * 365
        self.carbon_emissions_tons_year = (annual_energy_kwh * grid_carbon_intensity) / 1000
        return self.carbon_emissions_tons_year
    
    def set_renewable_percentage(self, percentage: float):
        """Set the percentage of renewable energy used"""
        self.renewable_percentage = min(100, max(0, percentage))
    
    def calculate_pue(self) -> float:
        """
        Calculate Power Usage Effectiveness
        PUE = Total Facility Energy / IT Equipment Energy
        Best: 1.0-1.2, Average: 1.5-2.0, Poor: >2.0
        """
        # Estimate based on renewable percentage and efficiency
        base_pue = 1.67
        if self.renewable_percentage > 80:
            self.pue = 1.2 + (100 - self.renewable_percentage) * 0.01
        elif self.renewable_percentage > 50:
            self.pue = 1.4 + (80 - self.renewable_percentage) * 0.01
        else:
            self.pue = 1.6 + (50 - self.renewable_percentage) * 0.01
        return self.pue
    
    def calculate_wue(self) -> float:
        """
        Calculate Water Usage Effectiveness
        WUE = Annual Water Usage (L) / IT Equipment Energy (kWh)
        Target: <1.8 L/kWh
        """
        annual_water = self.water_usage_liters_day * 365
        it_energy_kwh = self.it_equipment_power_mw * 1000 * 24 * 365
        wue = annual_water / it_energy_kwh if it_energy_kwh > 0 else 0
        return wue
    
    def calculate_cue(self) -> float:
        """
        Calculate Carbon Usage Effectiveness
        CUE = Total CO2 Emissions (kg) / IT Equipment Energy (kWh)
        Lower is better
        """
        it_energy_kwh = self.it_equipment_power_mw * 1000 * 24 * 365
        cue = (self.carbon_emissions_tons_year * 1000) / it_energy_kwh if it_energy_kwh > 0 else 0
        return cue
    
    def calculate_costs(self) -> Dict:
        """Calculate annual operational costs"""
        annual_energy_kwh = self.power_mw * 1000 * 24 * 365
        annual_water_liters = self.water_usage_liters_day * 365
        
        energy_cost = annual_energy_kwh * self.electricity_price_per_kwh
        water_cost = annual_water_liters * self.water_price_per_liter
        carbon_cost = self.carbon_emissions_tons_year * self.carbon_price_per_ton
        
        # Potential savings with 50% renewable
        renewable_gap = max(0, 50 - self.renewable_percentage)
        potential_carbon_savings = (self.carbon_emissions_tons_year * renewable_gap / 100) * self.carbon_price_per_ton
        
        return {
            'energy_cost_usd': energy_cost,
            'water_cost_usd': water_cost,
            'carbon_cost_usd': carbon_cost,
            'total_cost_usd': energy_cost + water_cost + carbon_cost,
            'potential_savings_usd': potential_carbon_savings
        }
    
    def calculate_roi_renewable(self, investment_usd: float) -> Dict:
        """Calculate ROI for renewable energy investment"""
        current_costs = self.calculate_costs()
        
        # Assume 50% renewable reduces carbon costs by 50%
        annual_savings = current_costs['carbon_cost_usd'] * 0.5
        
        # Add energy cost savings (renewable often cheaper long-term)
        annual_savings += current_costs['energy_cost_usd'] * 0.15
        
        roi_years = investment_usd / annual_savings if annual_savings > 0 else float('inf')
        
        return {
            'investment_usd': investment_usd,
            'annual_savings_usd': annual_savings,
            'roi_years': roi_years,
            'payback_period': f"{roi_years:.1f} years" if roi_years < 100 else ">100 years"
        }
    
    def calculate_scope_emissions(self) -> Dict:
        """Calculate Scope 1, 2, 3 emissions"""
        # Scope 1: Direct emissions (backup generators, on-site fuel)
        scope1 = self.carbon_emissions_tons_year * 0.05  # ~5% from backup generators
        
        # Scope 2: Indirect from purchased electricity
        scope2 = self.carbon_emissions_tons_year * 0.90  # ~90% from grid electricity
        
        # Scope 3: Supply chain, employee travel, etc.
        scope3 = self.carbon_emissions_tons_year * 0.05  # ~5% from other sources
        
        return {
            'scope1_tons': scope1,
            'scope2_tons': scope2,
            'scope3_tons': scope3,
            'total_tons': scope1 + scope2 + scope3
        }
    
    def get_metrics(self) -> Dict:
        """Return all metrics as dictionary including advanced calculations"""
        costs = self.calculate_costs()
        scope_emissions = self.calculate_scope_emissions()
        
        return {
            'name': self.name,
            'location': self.location,
            'power_mw': self.power_mw,
            'area_sqm': self.area_sqm,
            'water_usage_liters_day': self.water_usage_liters_day,
            'carbon_emissions_tons_year': self.carbon_emissions_tons_year,
            'renewable_percentage': self.renewable_percentage,
            'effective_emissions': self.carbon_emissions_tons_year * (1 - self.renewable_percentage/100),
            
            'pue': self.calculate_pue(),
            'wue': self.calculate_wue(),
            'cue': self.calculate_cue(),
            'server_utilization': self.server_utilization,
            
            'energy_cost_usd': costs['energy_cost_usd'],
            'water_cost_usd': costs['water_cost_usd'],
            'carbon_cost_usd': costs['carbon_cost_usd'],
            'total_cost_usd': costs['total_cost_usd'],
            'potential_savings_usd': costs['potential_savings_usd'],
            
            'scope1_emissions': scope_emissions['scope1_tons'],
            'scope2_emissions': scope_emissions['scope2_tons'],
            'scope3_emissions': scope_emissions['scope3_tons'],
        }


class EmissionPredictor:
    """AI model for predicting future emissions and energy demand"""
    
    def __init__(self):
        self.model = RandomForestRegressor(n_estimators=100, random_state=42)
        self.scaler = StandardScaler()
        self.is_trained = False
        
    def prepare_training_data(self, data_centers: List[DataCenterModel], 
                            years: int = 5) -> Tuple[np.ndarray, np.ndarray]:
        """Prepare synthetic training data for the model"""
        X = []
        y = []
        
        for dc in data_centers:
            for year in range(years):

                temp_increase = year * 0.2  # SSP5-8.5 scenario
                features = [
                    dc.power_mw,
                    dc.area_sqm / 1000000,  # Convert to millions
                    dc.renewable_percentage,
                    year,
                    temp_increase
                ]
                
                growth_factor = 1 + (year * 0.15)  # 15% annual growth
                cooling_penalty = 1 + (temp_increase * 0.05)  # 5% per 0.2°C
                future_emissions = dc.carbon_emissions_tons_year * growth_factor * cooling_penalty
                
                X.append(features)
                y.append(future_emissions)
        
        return np.array(X), np.array(y)
    
    def train(self, data_centers: List[DataCenterModel]):
        """Train the prediction model"""
        X, y = self.prepare_training_data(data_centers)
        X_scaled = self.scaler.fit_transform(X)
        self.model.fit(X_scaled, y)
        self.is_trained = True
        print(f"✓ Model trained on {len(X)} data points")
        
    def predict_future_emissions(self, dc: DataCenterModel, 
                                years_ahead: int = 10) -> List[float]:
        """Predict emissions for future years"""
        if not self.is_trained:
            raise ValueError("Model must be trained first")
        
        predictions = []
        for year in range(years_ahead + 1):
            temp_increase = year * 0.2
            features = np.array([[
                dc.power_mw,
                dc.area_sqm / 1000000,
                dc.renewable_percentage,
                year,
                temp_increase
            ]])
            features_scaled = self.scaler.transform(features)
            prediction = self.model.predict(features_scaled)[0]
            predictions.append(prediction)
        
        return predictions


class SustainabilityRecommender:
    """Generate recommendations for sustainable data center operations"""
    
    @staticmethod
    def analyze_and_recommend(dc: DataCenterModel, 
                             grid_carbon_intensity: float) -> Dict:
        """Analyze data center and provide recommendations"""
        recommendations = []
        potential_savings = {}
        
        # 1. Renewable Energy Integration
        if dc.renewable_percentage < 50:
            renewable_gap = 50 - dc.renewable_percentage
            emission_reduction = dc.carbon_emissions_tons_year * (renewable_gap / 100)
            recommendations.append({
                'priority': 'HIGH',
                'category': 'Renewable Energy',
                'action': f'Increase renewable energy from {dc.renewable_percentage:.1f}% to 50%',
                'impact': f'Reduce emissions by {emission_reduction:.0f} tons CO₂/year',
                'implementation': 'Install on-site solar panels or sign PPA with renewable provider'
            })
            potential_savings['renewable_integration'] = emission_reduction
        
        # 2. Cooling Optimization
        water_per_mw = dc.water_usage_liters_day / dc.power_mw
        if water_per_mw > 80000:  # High water usage
            water_reduction = dc.water_usage_liters_day * 0.25
            recommendations.append({
                'priority': 'MEDIUM',
                'category': 'Cooling Optimization',
                'action': 'Implement advanced cooling systems (liquid cooling, free cooling)',
                'impact': f'Reduce water usage by {water_reduction/1000000:.1f}M liters/day (25%)',
                'implementation': 'Deploy AI-powered cooling optimization and upgrade to efficient systems'
            })
            potential_savings['cooling_optimization'] = water_reduction
        
        if dc.power_mw > 100:  
            energy_reduction = dc.power_mw * 0.15  # 15% potential reduction
            emission_reduction = energy_reduction * 1000 * 24 * 365 * grid_carbon_intensity / 1000
            recommendations.append({
                'priority': 'HIGH',
                'category': 'Energy Efficiency',
                'action': 'Optimize server utilization and implement workload management',
                'impact': f'Reduce power consumption by {energy_reduction:.1f} MW, saving {emission_reduction:.0f} tons CO₂/year',
                'implementation': 'Deploy AI workload optimization and decommission underutilized servers'
            })
            potential_savings['energy_efficiency'] = emission_reduction
        
        if grid_carbon_intensity > 0.5:  # High carbon grid
            recommendations.append({
                'priority': 'MEDIUM',
                'category': 'Location Strategy',
                'action': 'Consider relocation to regions with cleaner energy grids',
                'impact': 'Potential 40-60% reduction in carbon footprint',
                'implementation': 'Evaluate regions with high renewable energy availability and cooler climates'
            })
        
        # Calculate total potential impact
        total_emission_reduction = sum([v for k, v in potential_savings.items() 
                                       if 'emission' in k or 'renewable' in k or 'energy' in k])
        
        return {
            'recommendations': recommendations,
            'potential_savings': potential_savings,
            'total_emission_reduction_tons': total_emission_reduction,
            'sustainability_score': min(100, dc.renewable_percentage + 
                                      (100 - dc.renewable_percentage) * 0.3)
        }


class AIrthPlatform:
    """Main platform for AIrth - Sustainable Energy"""
    
    def __init__(self):
        self.data_centers: List[DataCenterModel] = []
        self.predictor = EmissionPredictor()
        self.recommender = SustainabilityRecommender()
        
    def add_data_center(self, name: str, location: Tuple[float, float],
                       power_mw: float, area_sqm: float,
                       grid_carbon_intensity: float = 0.5,
                       renewable_percentage: float = 0) -> DataCenterModel:
        """Add a new data center to the platform"""
        dc = DataCenterModel(name, location, power_mw, area_sqm)
        dc.calculate_carbon_emissions(grid_carbon_intensity)
        dc.set_renewable_percentage(renewable_percentage)
        self.data_centers.append(dc)
        return dc
    
    def train_prediction_model(self):
        """Train the AI prediction model"""
        if len(self.data_centers) < 3:
            print("⚠ Warning: Need at least 3 data centers for training")
            return
        self.predictor.train(self.data_centers)
    
    def generate_global_map(self, output_file: str = 'airth_global_map.html'):
        """Generate interactive global map of data centers"""
        if not self.data_centers:
            print("No data centers to map")
            return
        
        m = folium.Map(location=[20, 0], zoom_start=2, tiles='OpenStreetMap')
        
        # Add data centers
        for dc in self.data_centers:
            metrics = dc.get_metrics()
            
            if metrics['effective_emissions'] < 50000:
                color = 'green'
            elif metrics['effective_emissions'] < 150000:
                color = 'orange'
            else:
                color = 'red'
            
            popup_html = f"""
            <div style="font-family: Arial; width: 250px;">
                <h4>{dc.name}</h4>
                <b>Power:</b> {dc.power_mw:.1f} MW<br>
                <b>Area:</b> {dc.area_sqm/1000000:.2f} million m²<br>
                <b>Water Usage:</b> {dc.water_usage_liters_day/1000000:.1f}M L/day<br>
                <b>Emissions:</b> {dc.carbon_emissions_tons_year:.0f} tons CO₂/year<br>
                <b>Renewable:</b> {dc.renewable_percentage:.1f}%<br>
                <b>Effective Emissions:</b> {metrics['effective_emissions']:.0f} tons CO₂/year
            </div>
            """
            
            folium.CircleMarker(
                location=dc.location,
                radius=min(30, dc.power_mw / 10),
                popup=folium.Popup(popup_html, max_width=300),
                color=color,
                fill=True,
                fillColor=color,
                fillOpacity=0.6,
                weight=2
            ).add_to(m)
        
        m.save(output_file)
        print(f"✓ Global map saved to {output_file}")
        return m
    
    def generate_emissions_forecast(self, dc_name: str, years: int = 10):
        """Generate emissions forecast for a specific data center"""
        dc = next((d for d in self.data_centers if d.name == dc_name), None)
        if not dc:
            print(f"Data center '{dc_name}' not found")
            return
        
        if not self.predictor.is_trained:
            print("Training prediction model...")
            self.train_prediction_model()
        
        predictions = self.predictor.predict_future_emissions(dc, years)
        
        # visualization
        plt.figure(figsize=(12, 6))
        years_range = list(range(years + 1))
        
        plt.plot(years_range, predictions, marker='o', linewidth=2, 
                label='Predicted Emissions', color='#e74c3c')
        
        baseline = [dc.carbon_emissions_tons_year] * (years + 1)
        plt.plot(years_range, baseline, '--', label='Current Emissions', 
                color='#95a5a6', alpha=0.7)
        
        plt.xlabel('Years from Now', fontsize=12)
        plt.ylabel('CO₂ Emissions (tons/year)', fontsize=12)
        plt.title(f'Emissions Forecast: {dc.name}', fontsize=14, fontweight='bold')
        plt.legend()
        plt.grid(True, alpha=0.3)
        plt.tight_layout()
        
        filename = f'emissions_forecast_{dc_name.replace(" ", "_")}.png'
        plt.savefig(filename, dpi=300, bbox_inches='tight')
        print(f"✓ Forecast chart saved to {filename}")
        plt.close()
        
        return predictions
    
    def generate_sustainability_report(self, dc_name: str) -> Dict:
        """Generate comprehensive sustainability report"""
        dc = next((d for d in self.data_centers if d.name == dc_name), None)
        if not dc:
            print(f"Data center '{dc_name}' not found")
            return {}
        
        # recommendations
        analysis = self.recommender.analyze_and_recommend(dc, 0.5)
        
        # Print report
        print("\n" + "="*70)
        print(f"SUSTAINABILITY REPORT: {dc.name}")
        print("="*70)
        
        metrics = dc.get_metrics()
        print("\n📊 CURRENT METRICS:")
        print(f"  Power Consumption: {metrics['power_mw']:.1f} MW")
        print(f"  Water Usage: {metrics['water_usage_liters_day']/1000000:.2f} million liters/day")
        print(f"  Annual Emissions: {metrics['carbon_emissions_tons_year']:.0f} tons CO₂")
        print(f"  Renewable Energy: {metrics['renewable_percentage']:.1f}%")
        print(f"  Effective Emissions: {metrics['effective_emissions']:.0f} tons CO₂")
        print(f"  Sustainability Score: {analysis['sustainability_score']:.1f}/100")
        
        print("\n💡 RECOMMENDATIONS:")
        for i, rec in enumerate(analysis['recommendations'], 1):
            print(f"\n  {i}. [{rec['priority']}] {rec['category']}")
            print(f"     Action: {rec['action']}")
            print(f"     Impact: {rec['impact']}")
            print(f"     Implementation: {rec['implementation']}")
        
        if analysis['total_emission_reduction_tons'] > 0:
            print(f"\n🎯 TOTAL POTENTIAL IMPACT:")
            print(f"  Emission Reduction: {analysis['total_emission_reduction_tons']:.0f} tons CO₂/year")
            reduction_pct = (analysis['total_emission_reduction_tons'] / 
                           metrics['carbon_emissions_tons_year'] * 100)
            print(f"  Percentage Reduction: {reduction_pct:.1f}%")
        
        print("\n" + "="*70 + "\n")
        
        return analysis
    
    def generate_summary_dashboard(self):
        """Generate summary dashboard with key metrics"""
        if not self.data_centers:
            print("No data centers to analyze")
            return
        
        total_power = sum(dc.power_mw for dc in self.data_centers)
        total_emissions = sum(dc.carbon_emissions_tons_year for dc in self.data_centers)
        total_water = sum(dc.water_usage_liters_day for dc in self.data_centers)
        avg_renewable = np.mean([dc.renewable_percentage for dc in self.data_centers])
        
        fig, axes = plt.subplots(2, 2, figsize=(15, 10))
        fig.suptitle('AIrth Platform - Global Data Center Dashboard', 
                    fontsize=16, fontweight='bold')

        ax1 = axes[0, 0]
        names = [dc.name for dc in self.data_centers]
        powers = [dc.power_mw for dc in self.data_centers]
        colors = plt.colormaps['viridis'](np.linspace(0, 1, len(names)))
        ax1.barh(names, powers, color=colors)
        ax1.set_xlabel('Power (MW)')
        ax1.set_title('Power Consumption by Data Center')
        ax1.grid(axis='x', alpha=0.3)
        
        ax2 = axes[0, 1]
        emissions = [dc.carbon_emissions_tons_year for dc in self.data_centers]
        renewable = [dc.renewable_percentage for dc in self.data_centers]
        scatter = ax2.scatter(renewable, emissions, s=200, c=emissions, 
                            cmap='RdYlGn_r', alpha=0.6, edgecolors='black')
        ax2.set_xlabel('Renewable Energy (%)')
        ax2.set_ylabel('Annual Emissions (tons CO₂)')
        ax2.set_title('Emissions vs Renewable Energy Usage')
        ax2.grid(True, alpha=0.3)
        plt.colorbar(scatter, ax=ax2, label='Emissions')
        
        ax3 = axes[1, 0]
        water_usage = [dc.water_usage_liters_day/1000000 for dc in self.data_centers]
        ax3.pie(water_usage, labels=names, autopct='%1.1f%%', startangle=90)
        ax3.set_title('Water Usage Distribution (Million L/day)')
        
        ax4 = axes[1, 1]
        ax4.axis('off')
        summary_text = f"""
        GLOBAL SUMMARY
        
        Total Data Centers: {len(self.data_centers)}
        
        Total Power: {total_power:.1f} MW
        
        Total Emissions: {total_emissions:.0f} tons CO₂/year
        
        Total Water Usage: {total_water/1000000:.1f} million L/day
        
        Average Renewable: {avg_renewable:.1f}%
        
        Estimated Global Impact:
        • Equivalent to {total_emissions/1000:.1f}k cars/year
        • Could power {total_power*1000/1.2:.0f}k homes
        """
        ax4.text(0.1, 0.5, summary_text, fontsize=12, verticalalignment='center',
                fontfamily='monospace', bbox=dict(boxstyle='round', 
                facecolor='wheat', alpha=0.5))
        
        plt.tight_layout()
        plt.savefig('airth_dashboard.png', dpi=300, bbox_inches='tight')
        print("✓ Dashboard saved to airth_dashboard.png")
        plt.close()


def demo_airth_platform():
    """Demonstration of AIrth platform capabilities"""
    print("\n" + "="*70)
    print("AIrth - Sustainable Energy Platform Demo")
    print("AI-powered platform for data center environmental impact analysis")
    print("="*70 + "\n")
    
    platform = AIrthPlatform()
    
    print("📍 Adding global data centers...")
    
    # China Telecom - Inner Mongolia (World's largest)
    platform.add_data_center(
        name="China Telecom Inner Mongolia",
        location=(40.8, 111.7),
        power_mw=150,
        area_sqm=1000000,
        grid_carbon_intensity=0.65,  # China's coal-heavy grid
        renewable_percentage=15
    )
    
    # Google Data Center - Finland
    platform.add_data_center(
        name="Google Hamina Finland",
        location=(60.5, 27.2),
        power_mw=120,
        area_sqm=750000,
        grid_carbon_intensity=0.15,  # Finland's clean grid
        renewable_percentage=85
    )
    
    # AWS US-East
    platform.add_data_center(
        name="AWS US-East Virginia",
        location=(38.9, -77.5),
        power_mw=200,
        area_sqm=900000,
        grid_carbon_intensity=0.45,
        renewable_percentage=45
    )
    
    # Microsoft Azure - Netherlands
    platform.add_data_center(
        name="Azure Netherlands",
        location=(52.3, 4.9),
        power_mw=95,
        area_sqm=600000,
        grid_carbon_intensity=0.35,
        renewable_percentage=60
    )
    
    # Facebook - Singapore
    platform.add_data_center(
        name="Meta Singapore",
        location=(1.3, 103.8),
        power_mw=110,
        area_sqm=700000,
        grid_carbon_intensity=0.42,
        renewable_percentage=30
    )


    
    print(f"✓ Added {len(platform.data_centers)} data centers\n")
    
    # Train prediction model
    print("🤖 Training AI prediction model...")
    platform.train_prediction_model()
    print()
    
    print("🗺️  Generating global map...")
    platform.generate_global_map()
    print()
    
    # dashboard
    print("📊 Generating summary dashboard...")
    platform.generate_summary_dashboard()
    print()
    
    # emissions forecast for largest data center
    print("📈 Generating emissions forecast...")
    platform.generate_emissions_forecast("China Telecom Inner Mongolia", years=10)
    print()
    
    # sustainability reports
    print("📋 Generating sustainability reports...\n")
    for dc in platform.data_centers[:2]:  # First 2 for demo
        platform.generate_sustainability_report(dc.name)
    
    print("\n" + "="*70)
    print("✅ Demo Complete!")
    print("="*70)
    print("\nGenerated files:")
    print("  • airth_global_map.html - Interactive global map")
    print("  • airth_dashboard.png - Summary dashboard")
    print("  • emissions_forecast_*.png - Emissions predictions")
    print("\nAIrth helps reduce data center environmental impact through:")
    print("  ✓ Real-time monitoring and mapping")
    print("  ✓ AI-powered emissions forecasting")
    print("  ✓ Actionable sustainability recommendations")
    print("  ✓ Support for SDG 7 (Clean Energy) and SDG 13 (Climate Action)")
    print("="*70 + "\n")


if __name__ == "__main__":
    demo_airth_platform()
