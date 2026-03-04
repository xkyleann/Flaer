# AIrth - Sustainable Energy Platform

![AIrth Logo](https://img.shields.io/badge/AIrth-Sustainable%20Energy-green)
![Python](https://img.shields.io/badge/Python-3.8%2B-blue)
![License](https://img.shields.io/badge/License-MIT-yellow)

## 🌍 Overview

**AIrth** is an AI-powered digital platform that maps global data centers, predicts their long-term environmental impact, and recommends sustainable actions. The system uses machine learning to forecast future energy demand, grid emissions, and climate risks, converting complex environmental data into strategic insights.

### Key Features

- 🗺️ **Global Data Center Mapping** - Interactive visualization of data centers worldwide
- 🤖 **AI-Powered Predictions** - Machine learning models for emissions forecasting
- 💡 **Sustainability Recommendations** - Actionable insights for reducing environmental impact
- 📊 **Comprehensive Analytics** - Real-time monitoring of energy, water, and carbon metrics
- 🎯 **SDG Alignment** - Supports UN SDG 7 (Clean Energy) and SDG 13 (Climate Action)

## 📋 Problem Statement

Data centers are among the fastest-growing sources of carbon emissions and electricity use:

- **Current Impact**: Data centers consumed ~460 TWh in 2022 (IEA, 2024)
- **Future Projection**: Could more than double by 2030
- **Carbon Footprint**: Up to 300 million tons of CO₂ annually
- **Water Usage**: Large facilities use 12-19 million liters per day

### Who Is Affected?

- **Governments & Policymakers** - Need data for sustainable infrastructure planning
- **Tech Companies** - Must optimize energy and reduce emissions
- **Researchers & NGOs** - Require accurate climate impact data

## 🚀 Quick Start

### Prerequisites

- Python 3.8 or higher
- pip package manager
- Web browser

### Installation & Running

1. **Install dependencies**

```bash
pip install -r requirements.txt
```

2. **Start the web application**

```bash
python app.py
```

3. **Open in browser**

Navigate to: **http://127.0.0.1:8050**

That's it! The interactive web interface will load with 5 pre-configured global data centers.

📖 **For detailed instructions, see [QUICKSTART.md](QUICKSTART.md)**

### Alternative: Command-Line Demo

For a non-interactive demo that generates static visualizations:

```bash
python airth_platform.py
```

## 💻 Usage

### Quick Start Demo

The platform includes a comprehensive demo that showcases all features:

```python
python airth_platform.py
```

This will:
- Add 5 sample data centers from around the world
- Train the AI prediction model
- Generate an interactive global map
- Create a summary dashboard
- Produce emissions forecasts
- Generate sustainability reports

### Using the Platform Programmatically

```python
from airth_platform import AIrthPlatform

# Initialize platform
platform = AIrthPlatform()

# Add a data center
dc = platform.add_data_center(
    name="My Data Center",
    location=(40.7, -74.0),  # (latitude, longitude)
    power_mw=100,
    area_sqm=500000,
    grid_carbon_intensity=0.5,  # kg CO2 per kWh
    renewable_percentage=30
)

# Train prediction model
platform.train_prediction_model()

# Generate visualizations
platform.generate_global_map()
platform.generate_summary_dashboard()

# Get emissions forecast
predictions = platform.generate_emissions_forecast("My Data Center", years=10)

# Generate sustainability report
report = platform.generate_sustainability_report("My Data Center")
```

## 📊 Output Files

The platform generates several output files:

1. **airth_global_map.html** - Interactive map showing all data centers with metrics
2. **airth_dashboard.png** - Summary dashboard with key statistics
3. **emissions_forecast_*.png** - Emissions predictions for each data center

## 🔬 Technical Architecture

### Core Components

1. **DataCenterModel** - Individual data center environmental metrics
   - Power consumption tracking
   - Water usage estimation
   - Carbon emissions calculation
   - Renewable energy integration

2. **EmissionPredictor** - AI-powered forecasting
   - Random Forest regression model
   - SSP5-8.5 climate scenario integration
   - 10-year emissions predictions
   - Temperature impact modeling

3. **SustainabilityRecommender** - Action recommendations
   - Renewable energy integration strategies
   - Cooling system optimization
   - Energy efficiency improvements
   - Location strategy analysis

4. **AIrthPlatform** - Main orchestration layer
   - Data center management
   - Visualization generation
   - Report creation
   - Global analytics

### Data Sources & Methodology

- **Energy Consumption**: Based on IEA data center energy models
- **Water Usage**: Derived from China Telecom Inner Mongolia benchmark (150 MW = 12-19M L/day)
- **Carbon Intensity**: Regional grid emission factors
- **Climate Projections**: SSP5-8.5 scenario (0.2°C increase per year)
- **Growth Modeling**: 15% annual energy demand growth with 5% cooling penalty per temperature increase

## 📈 Impact Metrics

### Expected Outcomes

- **15-25% reduction** in energy waste through optimized operations
- **Lower carbon emissions** via renewable integration
- **Improved transparency** in data center environmental reporting
- **Strategic planning** for sustainable digital infrastructure

### Real-World Example

**China Telecom Inner Mongolia Information Park** (World's largest data center):
- Area: 1 million m²
- Power: 150 MW
- Water: 12-19 million liters/day
- **AIrth Impact**: Could identify 20-30% efficiency improvements

## 🎯 Sustainability Recommendations

The platform provides four categories of recommendations:

1. **Renewable Energy Integration**
   - Target: 50%+ renewable energy
   - Impact: Significant emission reductions
   - Implementation: Solar panels, wind PPAs

2. **Cooling Optimization**
   - Target: 25% water reduction
   - Impact: Millions of liters saved daily
   - Implementation: AI cooling, liquid cooling, free cooling

3. **Energy Efficiency**
   - Target: 15% power reduction
   - Impact: Lower operational costs and emissions
   - Implementation: Workload optimization, server consolidation

4. **Location Strategy**
   - Target: 40-60% carbon reduction
   - Impact: Leverage cleaner grids
   - Implementation: Strategic site selection

## 🌐 Global Impact & SDGs

AIrth directly supports:

- **SDG 7: Affordable and Clean Energy** - Promotes renewable integration
- **SDG 13: Climate Action** - Reduces carbon emissions from digital infrastructure
- **SDG 9: Industry, Innovation and Infrastructure** - Enables sustainable tech development

## 📚 References

- International Energy Agency (IEA). (2024). Data Center Energy Consumption Report
- IPCC Climate Projections - SSP5-8.5 Scenario
- Data Center Map. (2025). Global Data Center Database
- Planet Tracker. (2025). Asian AI Water Resources Report

## 🔮 Future Development

### Phase 1: Research & Concept ✅
- Problem statement and concept development
- Platform mockup and initial design

### Phase 2: Prototype & Testing (Current)
- AI models for emissions forecasting
- GIS mapping integration
- User testing and feedback

### Phase 3: Refinement & Global Impact
- Global implementation plan
- Partnership development
- Public launch and scaling

## 🤝 Contributing

AIrth is designed to be open and collaborative. Contributions are welcome in:

- Data source integration
- Model improvements
- Visualization enhancements
- Documentation updates

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 👥 Team

Developed as part of the Sustainable Energy initiative to accelerate the transition to cleaner digital infrastructure.

## 📞 Contact

For questions, partnerships, or collaboration opportunities, please reach out through the project repository.

---

**AIrth** - Making digital infrastructure sustainable, one data center at a time. 🌱
