# Flaer Carbon Intelligence Dashboard

A comprehensive carbon intelligence dashboard for data center portfolio management, built with Svelte frontend and Flask backend.

## 🎯 Overview

The dashboard provides real-time carbon intelligence across 47 data center facilities with:
- Portfolio health monitoring (72/100 score)
- Global footprint mapping
- Emissions forecasting (2030/2035)
- Priority action recommendations
- Interactive carbon calculator
- Site intelligence for new facilities

## 🏗️ Architecture

### Frontend (Svelte)
- **Location**: `frontend-svelte/`
- **Port**: 5173 (Vite dev server)
- **Framework**: Svelte + Vite
- **Components**:
  - `Dashboard.svelte` - Main container with navigation
  - `DashboardSidebar.svelte` - Navigation with health score
  - `DashboardOverview.svelte` - Portfolio metrics & map
  - `DashboardForecast.svelte` - Emissions projections
  - `DashboardAnalytics.svelte` - Performance metrics
  - `DashboardActions.svelte` - Priority interventions
  - `DashboardCalculator.svelte` - Carbon calculator
  - `DashboardSiteIQ.svelte` - Location analysis

### Backend (Flask)
- **Location**: `backend/`
- **Port**: 5001
- **Framework**: Flask + Flask-CORS
- **API Endpoints**:
  - `GET /api/health` - Health check
  - `GET /api/dashboard/overview` - Portfolio summary
  - `GET /api/dashboard/datacenters` - All data centers
  - `GET /api/dashboard/datacenters/<id>` - Specific data center
  - `GET /api/dashboard/forecast` - Emissions forecast data
  - `GET /api/dashboard/actions` - Priority actions
  - `GET /api/dashboard/site-intelligence` - All site analyses
  - `GET /api/dashboard/site-intelligence/<id>` - Specific site
  - `POST /api/dashboard/calculator` - Carbon calculations

## 🚀 Getting Started

### Prerequisites
- Node.js 18+ (for frontend)
- Python 3.8+ (for backend)

### Backend Setup

```bash
cd backend

# Create virtual environment (optional)
python3 -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Start backend server
python3 app.py
```

Backend will run on http://127.0.0.1:5001

### Frontend Setup

```bash
cd frontend-svelte

# Install dependencies
npm install

# Start development server
npm run dev
```

Frontend will run on http://localhost:5173

## 📊 Dashboard Sections

### 1. Overview
- **Portfolio Health**: 72/100 score with trend indicator
- **Key Metrics**: Total emissions, carbon intensity, renewable energy %
- **Global Map**: Interactive visualization of 5 major data centers
- **Priority Interventions**: Table of facilities ranked by urgency
- **Resource Pressure**: Water-intensive sites and threshold alerts
- **Regulatory Alerts**: CSRD compliance requirements

### 2. Forecast
- **Emissions Projections**: 2030/2035 trajectories
- **Scenarios**: SSP5-8.5 climate scenario modeling
- **BAU vs Optimized**: Visual comparison of pathways
- **Impact Metrics**: Potential reduction (-38%), cost avoidance ($24M)
- **SBTi Alignment**: 1.5°C pathway tracking

### 3. Analytics
- **Data Center Selection**: Dropdown for 5 facilities
- **Performance Gauges**: Carbon intensity, PUE, renewable energy
- **Energy Mix**: Coal, gas, nuclear, renewables breakdown
- **Scope Breakdown**: Scope 1, 2, 3 emissions distribution
- **Real-time Data**: Live metrics with target comparisons

### 4. Actions
- **6 Priority Interventions**: Ranked by impact and feasibility
- **Categories**: High priority, Medium priority, Strategic
- **Metrics per Action**:
  - Annual CO₂ reduction
  - Investment required
  - Confidence score (72-92%)
- **Action Buttons**: Details and Approve workflows

### 5. Calculator
- **Input Parameters**:
  - Number of servers (100-10,000)
  - PUE (1.0-2.0)
  - Grid carbon intensity (50-800 gCO₂/kWh)
  - Average utilization (20-100%)
- **Results**:
  - Annual emissions (tCO₂e)
  - Monthly energy cost
  - Scope 2 intensity
  - Equivalents (trees, cars)

### 6. Site Intelligence
- **Interactive Map**: Click regions to analyze
- **3 Candidate Locations**:
  - Stockholm, Sweden (Score: 88/100) - Excellent
  - New South Wales, Australia (Score: 74/100) - Good
  - Texas, USA (Score: 61/100) - Caution
- **6 Evaluation Factors**:
  - Renewable energy availability
  - Climate & cooling efficiency
  - Water availability
  - Regulatory environment
  - Grid reliability & resilience
  - Land & infrastructure cost
- **Recommendations**: Color-coded by suitability

## 🔌 API Usage Examples

### Get Portfolio Overview
```bash
curl http://127.0.0.1:5001/api/dashboard/overview
```

### Get Data Center Details
```bash
curl http://127.0.0.1:5001/api/dashboard/datacenters/stockholm
```

### Calculate Carbon Emissions
```bash
curl -X POST http://127.0.0.1:5001/api/dashboard/calculator \
  -H "Content-Type: application/json" \
  -d '{
    "servers": 2000,
    "pue": 1.2,
    "carbon_intensity": 300,
    "utilization": 70
  }'
```

### Get Site Intelligence
```bash
curl http://127.0.0.1:5001/api/dashboard/site-intelligence/stockholm
```

## 📈 Data Centers

The system tracks 5 major data centers:

1. **N. Virginia** (US East)
   - Carbon Intensity: 412 gCO₂/kWh
   - Risk: High
   - Capacity: 150 MW
   - Renewable: 48%

2. **Singapore** (APAC)
   - Carbon Intensity: 408 gCO₂/kWh
   - Risk: High
   - Capacity: 120 MW
   - Renewable: 35%

3. **Frankfurt** (EU West)
   - Carbon Intensity: 284 gCO₂/kWh
   - Risk: Medium
   - Capacity: 180 MW
   - Renewable: 72%

4. **Warsaw** (EU Central)
   - Carbon Intensity: 234 gCO₂/kWh
   - Risk: Low
   - Capacity: 95 MW
   - Renewable: 68%

5. **Stockholm** (Nordic)
   - Carbon Intensity: 22 gCO₂/kWh
   - Risk: Low
   - Capacity: 200 MW
   - Renewable: 98%

## 🎨 Design System

### Color Palette
- **Background**: Dark theme (#07110f, #0b1714)
- **Panels**: Semi-transparent white overlays
- **Green** (#2cad84): Low risk, positive metrics
- **Blue** (#7faeff): Medium priority, neutral
- **Amber** (#b67e3d): Medium risk, caution
- **Red** (#d35d5c): High risk, critical
- **Gold** (#b79563): Strategic, long-term

### Typography
- **Font**: Inter (Google Fonts)
- **Weights**: 400, 500, 600, 700, 800, 900
- **Headings**: 900 weight, tight letter-spacing
- **Body**: 400-700 weight, readable line-height

## 🔧 Development

### Frontend Development
```bash
cd frontend-svelte
npm run dev    # Start dev server
npm run build  # Build for production
npm run preview # Preview production build
```

### Backend Development
```bash
cd backend
python3 app.py  # Start with auto-reload
```

### Adding New API Endpoints
1. Add data structure to `backend/app.py`
2. Create route handler with `@app.get()` or `@app.post()`
3. Return JSON with `jsonify()`
4. Update this README with endpoint documentation

### Adding New Dashboard Sections
1. Create new component in `frontend-svelte/src/lib/`
2. Import in `Dashboard.svelte`
3. Add to navigation in `DashboardSidebar.svelte`
4. Add route case in `Dashboard.svelte`

## 📝 Notes

- Frontend uses static data for demo purposes
- Backend provides RESTful API for future integration
- All emissions data is illustrative for demonstration
- CORS is enabled for local development
- Production deployment requires environment configuration

## 🚦 Status

- ✅ Frontend: Fully functional with 6 sections
- ✅ Backend: API endpoints operational
- ✅ Integration: Ready for data connection
- ✅ Design: Matches original template
- ✅ Navigation: Smooth section switching
- ✅ Interactivity: Sliders, dropdowns, maps working

## 📄 License

Made with Bob - Carbon Intelligence Dashboard for Flaer