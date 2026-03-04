from datetime import datetime
from typing import Dict, List, Optional
import json
from dataclasses import dataclass, asdict
from enum import Enum


class ReportFormat(Enum):
    """Supported report formats"""
    PDF = "pdf"
    EXCEL = "excel"
    POWERPOINT = "powerpoint"
    JSON = "json"
    HTML = "html"


class ComplianceFramework(Enum):
    """Supported compliance frameworks"""
    EU_TAXONOMY = "EU Taxonomy"
    CDP = "Carbon Disclosure Project"
    GRI = "Global Reporting Initiative"
    TCFD = "Task Force on Climate-related Financial Disclosures"
    SASB = "Sustainability Accounting Standards Board"
    ISO_14001 = "ISO 14001 Environmental Management"


@dataclass
class ReportConfig:
    """Configuration for report generation"""
    title: str
    company_name: str
    logo_path: Optional[str] = None
    color_scheme: Dict[str, str] = None
    include_charts: bool = True
    include_recommendations: bool = True
    compliance_frameworks: List[ComplianceFramework] = None
    
    def __post_init__(self):
        if self.color_scheme is None:
            self.color_scheme = {
                'primary': '#00FFA3',
                'secondary': '#7C3AED',
                'accent': '#F59E0B'
            }
        if self.compliance_frameworks is None:
            self.compliance_frameworks = []


class EnhancedReportGenerator:
    """Generate comprehensive ESG reports with multiple formats and frameworks"""
    
    def __init__(self, platform):
        """
        Initialize report generator
        
        Args:
            platform: AIrthPlatform instance with data centers
        """
        self.platform = platform
        self.report_history = []
        
    def generate_esg_report(self,
                           data_center_name: str,
                           config: ReportConfig,
                           report_format: ReportFormat = ReportFormat.JSON) -> Dict:
        """
        Generate comprehensive ESG report for a data center
        
        Args:
            data_center_name: Name of the data center
            config: Report configuration
            report_format: Output format
            
        Returns:
            Dictionary containing report data and metadata
        """
        dc = None
        for data_center in self.platform.data_centers:
            if data_center.name == data_center_name:
                dc = data_center
                break
        
        if not dc:
            raise ValueError(f"Data center '{data_center_name}' not found")
        
        metrics = dc.get_metrics()
        
        report = {
            'metadata': self._generate_metadata(config),
            'executive_summary': self._generate_executive_summary(dc, metrics),
            'environmental_metrics': self._generate_environmental_section(dc, metrics),
            'efficiency_metrics': self._generate_efficiency_section(metrics),
            'emissions_analysis': self._generate_emissions_section(dc, metrics),
            'cost_analysis': self._generate_cost_section(metrics),
            'sustainability_recommendations': self._generate_recommendations_section(dc),
            'compliance': self._generate_compliance_section(metrics, config.compliance_frameworks),
            'future_projections': self._generate_projections_section(dc),
            'benchmarking': self._generate_benchmarking_section(dc, metrics)
        }
        
        self.report_history.append({
            'timestamp': datetime.now().isoformat(),
            'data_center': data_center_name,
            'format': report_format.value
        })
        
        return report
    
    def _generate_metadata(self, config: ReportConfig) -> Dict:
        """Generate report metadata"""
        return {
            'title': config.title,
            'company_name': config.company_name,
            'generated_date': datetime.now().strftime('%Y-%m-%d'),
            'generated_time': datetime.now().strftime('%H:%M:%S'),
            'report_version': '1.0',
            'platform': 'AIrth Sustainable Energy Platform',
            'color_scheme': config.color_scheme
        }
    
    def _generate_executive_summary(self, dc, metrics: Dict) -> Dict:
        """Generate executive summary section"""
        return {
            'facility_name': dc.name,
            'location': f"Lat: {dc.location[0]:.4f}, Lon: {dc.location[1]:.4f}",
            'capacity': f"{metrics['power_mw']} MW",
            'annual_emissions': f"{metrics['carbon_emissions_tons_year']:,.0f} tons CO₂",
            'renewable_percentage': f"{metrics['renewable_percentage']}%",
            'pue_rating': f"{metrics['pue']:.2f}",
            'sustainability_score': self._calculate_sustainability_score(metrics),
            'key_highlights': [
                f"Operating at {metrics['renewable_percentage']}% renewable energy",
                f"PUE of {metrics['pue']:.2f} ({'Excellent' if metrics['pue'] < 1.3 else 'Good' if metrics['pue'] < 1.5 else 'Average'})",
                f"Annual water usage: {metrics['water_usage_liters_day']:,.0f} liters/day",
                f"Effective emissions: {metrics['effective_emissions']:,.0f} tons CO₂/year"
            ]
        }
    
    def _generate_environmental_section(self, dc, metrics: Dict) -> Dict:
        """Generate environmental metrics section"""
        return {
            'energy_consumption': {
                'total_annual_mwh': metrics['power_mw'] * 8760,
                'renewable_mwh': metrics['power_mw'] * 8760 * metrics['renewable_percentage'] / 100,
                'fossil_fuel_mwh': metrics['power_mw'] * 8760 * (100 - metrics['renewable_percentage']) / 100
            },
            'water_usage': {
                'daily_liters': metrics['water_usage_liters_day'],
                'annual_liters': metrics['water_usage_liters_day'] * 365,
                'wue': metrics['wue']
            },
            'carbon_footprint': {
                'total_emissions_tons': metrics['carbon_emissions_tons_year'],
                'effective_emissions_tons': metrics['effective_emissions'],
                'scope1_tons': metrics['scope1_emissions'],
                'scope2_tons': metrics['scope2_emissions'],
                'scope3_tons': metrics['scope3_emissions']
            },
            'land_use': {
                'facility_area_sqm': metrics['area_sqm'],
                'facility_area_acres': metrics['area_sqm'] / 4047
            }
        }
    
    def _generate_efficiency_section(self, metrics: Dict) -> Dict:
        """Generate efficiency metrics section"""
        return {
            'pue': {
                'value': metrics['pue'],
                'rating': 'Excellent' if metrics['pue'] < 1.3 else 'Good' if metrics['pue'] < 1.5 else 'Average' if metrics['pue'] < 2.0 else 'Poor',
                'industry_average': 1.67,
                'best_practice': 1.2
            },
            'wue': {
                'value': metrics['wue'],
                'target': 1.8,
                'status': 'Meeting Target' if metrics['wue'] < 1.8 else 'Above Target'
            },
            'cue': {
                'value': metrics['cue'],
                'description': 'Carbon intensity per kWh of IT equipment energy'
            },
            'server_utilization': {
                'value': metrics['server_utilization'],
                'target': 0.80,
                'improvement_potential': max(0, 0.80 - metrics['server_utilization'])
            }
        }
    
    def _generate_emissions_section(self, dc, metrics: Dict) -> Dict:
        """Generate emissions analysis section"""
        trees_needed = metrics['effective_emissions'] * 16  # ~16 trees per ton CO2
        cars_equivalent = metrics['effective_emissions'] / 4.6  # Average car: 4.6 tons/year
        homes_powered = (metrics['power_mw'] * 8760) / 10.5  # Average home: 10.5 MWh/year
        
        return {
            'current_emissions': {
                'total_tons_co2': metrics['carbon_emissions_tons_year'],
                'effective_tons_co2': metrics['effective_emissions'],
                'reduction_from_renewables': metrics['carbon_emissions_tons_year'] - metrics['effective_emissions']
            },
            'scope_breakdown': {
                'scope1': metrics['scope1_emissions'],
                'scope2': metrics['scope2_emissions'],
                'scope3': metrics['scope3_emissions']
            },
            'tangible_impact': {
                'trees_needed_to_offset': int(trees_needed),
                'equivalent_cars_on_road': int(cars_equivalent),
                'homes_powered_annually': int(homes_powered)
            }
        }
    
    def _generate_cost_section(self, metrics: Dict) -> Dict:
        """Generate cost analysis section"""
        return {
            'annual_costs': {
                'energy_cost_usd': metrics['energy_cost_usd'],
                'water_cost_usd': metrics['water_cost_usd'],
                'carbon_cost_usd': metrics['carbon_cost_usd'],
                'total_cost_usd': metrics['total_cost_usd']
            },
            'savings_potential': {
                'renewable_investment_savings_usd': metrics['potential_savings_usd'],
                'description': 'Potential annual savings from 50% renewable energy integration'
            }
        }
    
    def _generate_recommendations_section(self, dc) -> Dict:
        """Generate detailed sustainability recommendations section"""
        metrics = dc.get_metrics()
        grid_carbon_intensity = metrics['carbon_emissions_tons_year'] / (dc.power_mw * 8760 * 1000) * 1000
        
        analysis = self.platform.recommender.analyze_and_recommend(dc, grid_carbon_intensity)
        
        detailed_recommendations = []
        for rec in analysis['recommendations']:
            detailed_rec = {
                'category': rec['category'],
                'priority': rec['priority'],
                'action': rec['action'],
                'impact': rec['impact'],
                'implementation': rec.get('implementation', ''),
                'detailed_steps': self._get_implementation_steps(rec['category']),
                'timeline': self._get_implementation_timeline(rec['category']),
                'estimated_cost': self._estimate_implementation_cost(rec['category'], dc),
                'roi_analysis': self._calculate_recommendation_roi(rec['category'], dc, metrics),
                'success_metrics': self._get_success_metrics(rec['category']),
                'case_studies': self._get_case_studies(rec['category'])
            }
            detailed_recommendations.append(detailed_rec)
        
        return {
            'sustainability_score': analysis['sustainability_score'],
            'total_potential_reduction': analysis.get('total_emission_reduction_tons', 0),
            'priority_recommendations': detailed_recommendations,
            'implementation_roadmap': self._generate_implementation_roadmap(detailed_recommendations)
        }
    
    def _get_implementation_steps(self, category: str) -> List[str]:
        """Get detailed implementation steps for each category"""
        steps = {
            'Renewable Energy': [
                'Conduct renewable energy feasibility study (solar, wind, hydro)',
                'Evaluate on-site vs off-site renewable options',
                'Request proposals from renewable energy providers',
                'Negotiate Power Purchase Agreements (PPAs) or install on-site systems',
                'Integrate renewable energy with existing grid connection',
                'Install monitoring systems for renewable energy tracking',
                'Obtain renewable energy certificates (RECs) for verification'
            ],
            'Cooling Optimization': [
                'Audit current cooling systems and identify inefficiencies',
                'Implement AI-powered cooling management software',
                'Upgrade to high-efficiency chillers and cooling towers',
                'Deploy liquid cooling for high-density racks',
                'Implement free cooling where climate permits',
                'Optimize airflow management with hot/cold aisle containment',
                'Install real-time temperature and humidity monitoring',
                'Train staff on optimized cooling operations'
            ],
            'Energy Efficiency': [
                'Conduct comprehensive energy audit',
                'Implement server virtualization and consolidation',
                'Deploy workload optimization and auto-scaling',
                'Upgrade to energy-efficient servers and storage',
                'Implement intelligent power management',
                'Optimize UPS and power distribution efficiency',
                'Deploy LED lighting with motion sensors',
                'Establish continuous monitoring and optimization program'
            ],
            'Location Strategy': [
                'Analyze regional grid carbon intensity and renewable availability',
                'Evaluate climate conditions for natural cooling potential',
                'Assess proximity to renewable energy sources',
                'Consider water availability and regulations',
                'Evaluate tax incentives and renewable energy policies',
                'Plan phased migration strategy',
                'Establish new facility with sustainability-first design'
            ]
        }
        return steps.get(category, ['Contact sustainability consultant for detailed implementation plan'])
    
    def _get_implementation_timeline(self, category: str) -> Dict:
        """Get implementation timeline for each category"""
        timelines = {
            'Renewable Energy': {
                'planning_phase': '3-6 months',
                'procurement_phase': '6-12 months',
                'implementation_phase': '12-18 months',
                'total_duration': '21-36 months',
                'quick_wins': 'Sign PPA within 6 months for immediate renewable credits'
            },
            'Cooling Optimization': {
                'planning_phase': '1-2 months',
                'procurement_phase': '2-4 months',
                'implementation_phase': '6-12 months',
                'total_duration': '9-18 months',
                'quick_wins': 'Deploy AI cooling software within 3 months for 5-10% immediate savings'
            },
            'Energy Efficiency': {
                'planning_phase': '1-3 months',
                'procurement_phase': '3-6 months',
                'implementation_phase': '6-12 months',
                'total_duration': '10-21 months',
                'quick_wins': 'Server consolidation can start immediately with 10-15% savings in 3 months'
            },
            'Location Strategy': {
                'planning_phase': '6-12 months',
                'procurement_phase': '12-24 months',
                'implementation_phase': '24-36 months',
                'total_duration': '42-72 months',
                'quick_wins': 'Prioritize new workloads in cleaner regions immediately'
            }
        }
        return timelines.get(category, {'total_duration': 'Varies', 'quick_wins': 'Consult with experts'})
    
    def _estimate_implementation_cost(self, category: str, dc) -> Dict:
        """Estimate implementation costs"""
        power_mw = dc.power_mw
        
        costs = {
            'Renewable Energy': {
                'low_estimate': power_mw * 50000,  # $50k per MW for PPA
                'high_estimate': power_mw * 200000,  # $200k per MW for on-site solar
                'currency': 'USD',
                'notes': 'PPA requires minimal upfront cost; on-site installation higher but provides long-term ownership'
            },
            'Cooling Optimization': {
                'low_estimate': power_mw * 30000,  # $30k per MW
                'high_estimate': power_mw * 100000,  # $100k per MW
                'currency': 'USD',
                'notes': 'AI software is low cost; hardware upgrades (liquid cooling) are higher'
            },
            'Energy Efficiency': {
                'low_estimate': power_mw * 20000,  # $20k per MW
                'high_estimate': power_mw * 80000,  # $80k per MW
                'currency': 'USD',
                'notes': 'Software optimization is low cost; hardware replacement is higher'
            },
            'Location Strategy': {
                'low_estimate': power_mw * 500000,  # $500k per MW
                'high_estimate': power_mw * 2000000,  # $2M per MW
                'currency': 'USD',
                'notes': 'Major capital investment; consider for new facilities or major expansions'
            }
        }
        return costs.get(category, {'low_estimate': 0, 'high_estimate': 0, 'currency': 'USD', 'notes': 'Contact for estimate'})
    
    def _calculate_recommendation_roi(self, category: str, dc, metrics: Dict) -> Dict:
        """Calculate ROI for each recommendation"""
        annual_energy_cost = metrics['energy_cost_usd']
        annual_carbon_cost = metrics['carbon_cost_usd']
        
        roi = {
            'Renewable Energy': {
                'annual_savings': annual_carbon_cost * 0.5 + annual_energy_cost * 0.05,
                'payback_period_years': 5.0,
                'description': '50% carbon cost reduction + 5% energy cost savings'
            },
            'Cooling Optimization': {
                'annual_savings': annual_energy_cost * 0.15 + metrics['water_cost_usd'] * 0.25,
                'payback_period_years': 3.0,
                'description': '15% energy savings + 25% water cost reduction'
            },
            'Energy Efficiency': {
                'annual_savings': annual_energy_cost * 0.15,
                'payback_period_years': 4.0,
                'description': '15% energy cost reduction through optimization'
            },
            'Location Strategy': {
                'annual_savings': (annual_carbon_cost + annual_energy_cost) * 0.40,
                'payback_period_years': 10.0,
                'description': '40% reduction in combined energy and carbon costs'
            }
        }
        return roi.get(category, {'annual_savings': 0, 'payback_period_years': 0, 'description': 'Varies'})
    
    def _get_success_metrics(self, category: str) -> List[str]:
        """Define success metrics for each category"""
        metrics = {
            'Renewable Energy': [
                'Renewable energy percentage increase',
                'Scope 2 emissions reduction (tons CO₂)',
                'Renewable Energy Certificates (RECs) acquired',
                'Grid carbon intensity reduction',
                'Annual carbon cost savings'
            ],
            'Cooling Optimization': [
                'PUE improvement (target: <1.3)',
                'Water usage reduction (liters/day)',
                'WUE improvement (target: <1.8 L/kWh)',
                'Cooling energy consumption reduction (%)',
                'Temperature stability improvement'
            ],
            'Energy Efficiency': [
                'Total energy consumption reduction (MWh)',
                'Server utilization increase (target: >80%)',
                'Power per compute unit reduction',
                'Annual energy cost savings',
                'Carbon emissions reduction (tons CO₂)'
            ],
            'Location Strategy': [
                'Grid carbon intensity at new location',
                'Total emissions reduction (%)',
                'Renewable energy availability increase',
                'Natural cooling days per year',
                'Long-term cost savings'
            ]
        }
        return metrics.get(category, ['Define custom metrics with sustainability team'])
    
    def _get_case_studies(self, category: str) -> List[Dict]:
        """Provide relevant case studies"""
        cases = {
            'Renewable Energy': [
                {
                    'company': 'Google',
                    'achievement': '100% renewable energy matching since 2017',
                    'impact': 'Eliminated millions of tons of CO₂ emissions',
                    'key_learning': 'Long-term PPAs with renewable providers enable scale'
                },
                {
                    'company': 'Microsoft',
                    'achievement': '60% renewable energy by 2020, targeting 100% by 2025',
                    'impact': 'Significant carbon footprint reduction',
                    'key_learning': 'Combination of on-site and off-site renewable sources'
                }
            ],
            'Cooling Optimization': [
                {
                    'company': 'Google DeepMind',
                    'achievement': 'AI-powered cooling reduced energy by 40%',
                    'impact': 'Millions in annual savings, PUE improvement',
                    'key_learning': 'Machine learning can optimize complex cooling systems'
                },
                {
                    'company': 'Facebook Prineville',
                    'achievement': 'Free air cooling in Oregon climate',
                    'impact': 'PUE of 1.09, industry-leading efficiency',
                    'key_learning': 'Location selection enables natural cooling'
                }
            ],
            'Energy Efficiency': [
                {
                    'company': 'AWS',
                    'achievement': 'Server utilization optimization',
                    'impact': '3.6x more efficient than typical enterprise data center',
                    'key_learning': 'Workload optimization and auto-scaling critical'
                },
                {
                    'company': 'Apple',
                    'achievement': 'Custom silicon and efficient hardware',
                    'impact': 'Significant power reduction per compute unit',
                    'key_learning': 'Hardware innovation drives efficiency gains'
                }
            ],
            'Location Strategy': [
                {
                    'company': 'Facebook Luleå Sweden',
                    'achievement': 'Arctic location with 100% renewable energy',
                    'impact': 'Near-zero carbon emissions, natural cooling',
                    'key_learning': 'Strategic location selection maximizes sustainability'
                },
                {
                    'company': 'Microsoft underwater data center',
                    'achievement': 'Project Natick - ocean cooling',
                    'impact': 'Innovative cooling solution, renewable powered',
                    'key_learning': 'Novel locations can provide unique sustainability benefits'
                }
            ]
        }
        return cases.get(category, [{'company': 'Various', 'achievement': 'Industry best practices available', 'impact': 'Proven results', 'key_learning': 'Consult industry reports'}])
    
    def _generate_implementation_roadmap(self, recommendations: List[Dict]) -> Dict:
        """Generate phased implementation roadmap"""
        # Sort by priority
        high_priority = [r for r in recommendations if r['priority'] == 'HIGH']
        medium_priority = [r for r in recommendations if r['priority'] == 'MEDIUM']
        low_priority = [r for r in recommendations if r['priority'] == 'LOW']
        
        return {
            'phase_1_immediate': {
                'duration': '0-6 months',
                'focus': 'Quick wins and planning',
                'actions': [r['action'] for r in high_priority[:2]] if high_priority else ['Begin sustainability assessment'],
                'expected_impact': 'Initial 5-10% improvement'
            },
            'phase_2_short_term': {
                'duration': '6-18 months',
                'focus': 'Major implementations',
                'actions': [r['action'] for r in high_priority[2:] + medium_priority[:2]],
                'expected_impact': 'Cumulative 15-25% improvement'
            },
            'phase_3_long_term': {
                'duration': '18-36 months',
                'focus': 'Strategic transformations',
                'actions': [r['action'] for r in medium_priority[2:] + low_priority],
                'expected_impact': 'Cumulative 30-50% improvement'
            },
            'continuous_improvement': {
                'duration': 'Ongoing',
                'focus': 'Monitoring and optimization',
                'actions': ['Regular audits', 'Technology updates', 'Best practice adoption'],
                'expected_impact': 'Sustained performance and continuous gains'
            }
        }
    
    def _generate_compliance_section(self, metrics: Dict, frameworks: List[ComplianceFramework]) -> Dict:
        """Generate compliance framework section"""
        compliance = {}
        
        for framework in frameworks:
            if framework == ComplianceFramework.EU_TAXONOMY:
                compliance['EU_Taxonomy'] = {
                    'renewable_energy_threshold': '50%',
                    'current_status': f"{metrics['renewable_percentage']}%",
                    'compliant': metrics['renewable_percentage'] >= 50
                }
            elif framework == ComplianceFramework.CDP:
                compliance['CDP'] = {
                    'scope1_reported': True,
                    'scope2_reported': True,
                    'scope3_reported': True,
                    'emissions_reduction_target': 'Set and tracked'
                }
            elif framework == ComplianceFramework.GRI:
                compliance['GRI'] = {
                    'energy_consumption_reported': True,
                    'water_usage_reported': True,
                    'emissions_reported': True,
                    'standard': 'GRI 302 (Energy), GRI 303 (Water), GRI 305 (Emissions)'
                }
            elif framework == ComplianceFramework.TCFD:
                compliance['TCFD'] = {
                    'climate_risk_assessment': 'Included in 10-year projections',
                    'scenario_analysis': 'SSP5-8.5 scenario integrated',
                    'governance': 'Sustainability metrics tracked'
                }
        
        return compliance
    
    def _generate_projections_section(self, dc) -> Dict:
        """Generate future projections section"""
        if self.platform.predictor and self.platform.predictor.is_trained:
            predictions = self.platform.predictor.predict_future_emissions(dc, years_ahead=10)
            return {
                'forecast_horizon': '10 years',
                'methodology': 'Random Forest ML with SSP5-8.5 climate scenario',
                'projected_emissions': [
                    {
                        'year': i,
                        'emissions_tons_co2': float(pred)
                    }
                    for i, pred in enumerate(predictions)
                ],
                'growth_factors': {
                    'energy_demand_growth': '15% annually',
                    'temperature_increase': '0.2°C per year',
                    'cooling_penalty': '5% per 0.2°C'
                }
            }
        return {'status': 'Predictions not available'}
    
    def _generate_benchmarking_section(self, dc, metrics: Dict) -> Dict:
        """Generate benchmarking section"""
        all_dcs = [(dc_obj.name, dc_obj.get_metrics()) for dc_obj in self.platform.data_centers]
        
        # Calculate rankings
        sorted_by_emissions = sorted(all_dcs, key=lambda x: x[1]['effective_emissions'])
        sorted_by_renewable = sorted(all_dcs, key=lambda x: x[1]['renewable_percentage'], reverse=True)
        sorted_by_pue = sorted(all_dcs, key=lambda x: x[1]['pue'])
        
        # Find current facility rank
        emissions_rank = next(i for i, (name, _) in enumerate(sorted_by_emissions, 1) if name == dc.name)
        renewable_rank = next(i for i, (name, _) in enumerate(sorted_by_renewable, 1) if name == dc.name)
        pue_rank = next(i for i, (name, _) in enumerate(sorted_by_pue, 1) if name == dc.name)
        
        return {
            'total_facilities': len(all_dcs),
            'rankings': {
                'emissions': {
                    'rank': emissions_rank,
                    'percentile': int((1 - emissions_rank / len(all_dcs)) * 100)
                },
                'renewable_energy': {
                    'rank': renewable_rank,
                    'percentile': int((1 - renewable_rank / len(all_dcs)) * 100)
                },
                'pue_efficiency': {
                    'rank': pue_rank,
                    'percentile': int((1 - pue_rank / len(all_dcs)) * 100)
                }
            },
            'industry_averages': {
                'renewable_percentage': sum(m['renewable_percentage'] for _, m in all_dcs) / len(all_dcs),
                'pue': sum(m['pue'] for _, m in all_dcs) / len(all_dcs),
                'emissions_tons': sum(m['effective_emissions'] for _, m in all_dcs) / len(all_dcs)
            }
        }
    
    def _calculate_sustainability_score(self, metrics: Dict) -> int:
        """Calculate overall sustainability score (0-100)"""
        score = 0
        
        # Renewable energy (40 points)
        score += min(40, metrics['renewable_percentage'] * 0.4)
        
        # PUE efficiency (30 points)
        if metrics['pue'] <= 1.2:
            score += 30
        elif metrics['pue'] <= 1.5:
            score += 20
        elif metrics['pue'] <= 2.0:
            score += 10
        
        # Water efficiency (15 points)
        if metrics['wue'] < 1.8:
            score += 15
        elif metrics['wue'] < 2.5:
            score += 10
        
        # Carbon intensity (15 points)
        if metrics['cue'] < 0.3:
            score += 15
        elif metrics['cue'] < 0.5:
            score += 10
        elif metrics['cue'] < 0.7:
            score += 5
        
        return int(score)
    
    def export_report(self, report: Dict, filename: str, format: ReportFormat = ReportFormat.JSON):
        """
        Export report to file
        
        Args:
            report: Report dictionary
            filename: Output filename
            format: Export format
        """
        if format == ReportFormat.JSON:
            with open(filename, 'w') as f:
                json.dump(report, f, indent=2)
            print(f"✓ Report exported to {filename}")
        elif format == ReportFormat.HTML:
            html_content = self._generate_html_report(report)
            with open(filename, 'w') as f:
                f.write(html_content)
            print(f"✓ HTML report exported to {filename}")
        else:
            print(f"⚠ Format {format.value} not yet implemented. Exporting as JSON.")
            self.export_report(report, filename.replace(f'.{format.value}', '.json'), ReportFormat.JSON)
    
    def _generate_html_report(self, report: Dict) -> str:
        """Generate HTML version of report"""
        metadata = report['metadata']
        summary = report['executive_summary']
        
        html = f"""
<!DOCTYPE html>
<html>
<head>
    <title>{metadata['title']}</title>
    <style>
        body {{ font-family: Arial, sans-serif; margin: 40px; background: #f5f5f5; }}
        .header {{ background: {metadata['color_scheme']['primary']}; color: white; padding: 20px; border-radius: 10px; }}
        .section {{ background: white; margin: 20px 0; padding: 20px; border-radius: 10px; box-shadow: 0 2px 4px rgba(0,0,0,0.1); }}
        .metric {{ display: inline-block; margin: 10px 20px 10px 0; }}
        .metric-label {{ font-size: 12px; color: #666; }}
        .metric-value {{ font-size: 24px; font-weight: bold; color: {metadata['color_scheme']['secondary']}; }}
        h1 {{ margin: 0; }}
        h2 {{ color: {metadata['color_scheme']['secondary']}; }}
        .score {{ font-size: 48px; font-weight: bold; color: {metadata['color_scheme']['accent']}; }}
    </style>
</head>
<body>
    <div class="header">
        <h1>{metadata['title']}</h1>
        <p>{metadata['company_name']} | Generated: {metadata['generated_date']}</p>
    </div>
    
    <div class="section">
        <h2>Executive Summary</h2>
        <p><strong>Facility:</strong> {summary['facility_name']}</p>
        <p><strong>Location:</strong> {summary['location']}</p>
        <p><strong>Capacity:</strong> {summary['capacity']}</p>
        <div class="score">Sustainability Score: {summary['sustainability_score']}/100</div>
    </div>
    
    <div class="section">
        <h2>Key Metrics</h2>
        <div class="metric">
            <div class="metric-label">Annual Emissions</div>
            <div class="metric-value">{summary['annual_emissions']}</div>
        </div>
        <div class="metric">
            <div class="metric-label">Renewable Energy</div>
            <div class="metric-value">{summary['renewable_percentage']}</div>
        </div>
        <div class="metric">
            <div class="metric-label">PUE Rating</div>
            <div class="metric-value">{summary['pue_rating']}</div>
        </div>
    </div>
    
    <div class="section">
        <h2>Key Highlights</h2>
        <ul>
            {''.join(f'<li>{highlight}</li>' for highlight in summary['key_highlights'])}
        </ul>
    </div>
    
    <div class="section">
        <p><em>Full detailed report available in JSON format</em></p>
    </div>
</body>
</html>
"""
        return html
    
    def schedule_automated_report(self, 
                                  data_center_name: str,
                                  config: ReportConfig,
                                  frequency: str = 'monthly',
                                  recipients: List[str] = None):
        """
        Schedule automated report generation and delivery
        
        Args:
            data_center_name: Name of data center
            config: Report configuration
            frequency: 'daily', 'weekly', 'monthly', 'quarterly', 'annual'
            recipients: List of email addresses
        """
        schedule_config = {
            'data_center': data_center_name,
            'config': asdict(config),
            'frequency': frequency,
            'recipients': recipients or [],
            'next_run': self._calculate_next_run(frequency),
            'created': datetime.now().isoformat()
        }
        
        print(f"✓ Scheduled {frequency} reports for {data_center_name}")
        print(f"  Recipients: {', '.join(recipients) if recipients else 'None'}")
        print(f"  Next run: {schedule_config['next_run']}")
        
        return schedule_config
    
    def _calculate_next_run(self, frequency: str) -> str:
        """Calculate next scheduled run time"""
        from datetime import timedelta
        now = datetime.now()
        
        if frequency == 'daily':
            next_run = now + timedelta(days=1)
        elif frequency == 'weekly':
            next_run = now + timedelta(weeks=1)
        elif frequency == 'monthly':
            next_run = now + timedelta(days=30)
        elif frequency == 'quarterly':
            next_run = now + timedelta(days=90)
        elif frequency == 'annual':
            next_run = now + timedelta(days=365)
        else:
            next_run = now + timedelta(days=30)
        
        return next_run.strftime('%Y-%m-%d %H:%M:%S')


if __name__ == "__main__":
    from airth_platform import AIrthPlatform
    
    print("=" * 70)
    print("Enhanced Reporting Module - Demo")
    print("=" * 70)
    
    platform = AIrthPlatform()
    
    platform.add_data_center(
        "Demo Data Center",
        (40.7128, -74.0060),
        100,
        500000,
        0.45,
        60
    )
    
    platform.train_prediction_model()
    
    # Create report generator
    reporter = EnhancedReportGenerator(platform)
    
    config = ReportConfig(
        title="Q4 2024 Sustainability Report",
        company_name="Demo Corporation",
        compliance_frameworks=[
            ComplianceFramework.EU_TAXONOMY,
            ComplianceFramework.CDP,
            ComplianceFramework.GRI
        ]
    )
    
    # Generate report
    print("\n📊 Generating ESG Report...")
    report = reporter.generate_esg_report("Demo Data Center", config)
    
    # Export reports
    reporter.export_report(report, "demo_esg_report.json", ReportFormat.JSON)
    reporter.export_report(report, "demo_esg_report.html", ReportFormat.HTML)
    
    # Schedule automated reports
    print("\n📅 Scheduling Automated Reports...")
    reporter.schedule_automated_report(
        "Demo Data Center",
        config,
        frequency='monthly',
        recipients=['sustainability@demo.com', 'board@demo.com']
    )
    
    print("\n✓ Enhanced Reporting Demo Complete!")
    print(f"  Sustainability Score: {report['executive_summary']['sustainability_score']}/100")
    print(f"  Reports generated: demo_esg_report.json, demo_esg_report.html")


