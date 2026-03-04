# AIrth Project Structure

## 📁 Directory Organization

```
AIrth/
├── src/                          # Source code
│   ├── app.py                    # Main web application
│   ├── airth_platform.py         # Core platform functionality
│   ├── climate_impact_analyzer.py # Climate analysis module
│   └── enhanced_reporting.py     # Enhanced reporting features
│
├── outputs/                      # Generated outputs
│   ├── airth_dashboard.png       # Dashboard screenshots
│   ├── airth_global_map.html     # Interactive maps
│   ├── demo_esg_report.html      # Demo ESG reports
│   ├── demo_esg_report.json      # Demo data
│   └── emissions_forecast_*.png  # Forecast visualizations
│
├── examples/                     # Usage examples
│   └── example_usage.py          # Code examples
│
├── docs/                         # Documentation
│   └── PROJECT_STRUCTURE.md      # This file
│
├── requirements.txt              # Python dependencies
├── README.md                     # Main documentation
└── LICENSE                       # License information
```

## 🚀 Quick Start

### 1. Install Dependencies
```bash
cd AIrth
pip install -r requirements.txt
```

### 2. Run the Application
```bash
python src/app.py
```

### 3. Access the Platform
Open your browser and navigate to: http://127.0.0.1:8050

## 📦 Module Descriptions

### `src/app.py`
Main web application built with Dash. Features:
- Interactive global data center map
- Emissions analysis and forecasting
- Sustainability recommendations
- Cost analysis and ROI calculations
- Climate impact assessment

### `src/airth_platform.py`
Core platform functionality:
- Data center management
- Emissions calculations
- AI-powered predictions
- Sustainability scoring

### `src/climate_impact_analyzer.py`
Climate analysis module:
- Regional climate data
- Water stress analysis
- Heat island effect calculations
- Location-specific recommendations

### `src/enhanced_reporting.py`
Enhanced reporting features:
- ESG report generation
- Detailed recommendations
- Implementation timelines
- ROI calculations

## 🎨 Design Features

- **Modern UI**: Professional dark theme with blue-purple-pink gradient
- **Responsive Layout**: Bootstrap-based responsive design
- **Interactive Charts**: Plotly-powered visualizations
- **Real-time Updates**: Dynamic data updates
- **Professional Styling**: Glass-morphism effects and smooth animations

## 📊 Data Flow

1. **Data Input** → Data centers added to platform
2. **Processing** → AI models analyze and predict
3. **Visualization** → Interactive charts and maps
4. **Recommendations** → Actionable sustainability insights
5. **Reporting** → ESG reports and forecasts

## 🔧 Configuration

All configuration is done through the main application file (`src/app.py`).
Data centers can be added by modifying the `data_centers` list.

## 📝 License

See LICENSE file for details.