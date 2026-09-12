# Data Center Onboarding Guide

## How to Connect Your Data Center to flaer

This guide explains how to add your data center facilities to flaer for sustainability tracking and AI-powered insights.

---

## Quick Start

### 1. **Sign Up & Login**
- Create your account at the flaer dashboard
- Your organization is automatically created
- Free tier includes up to 3 data centers

### 2. **Add Your First Data Center**
Click the **"+ Add Data Center"** button in the dashboard to launch the onboarding wizard.

---

## Onboarding Wizard (3 Steps)

### Step 1: Basic Information

**Required Fields:**
- **Data Center Name**: A unique identifier (e.g., "Virginia DC-1", "Frankfurt Main")
- **Location**: Physical location in format: City, State/Region, Country

**Optional Fields:**
- **Latitude/Longitude**: Geographic coordinates for map visualization
  - Example: Ashburn, VA = 38.9072, -77.0369
  - Helps with accurate map placement and climate risk analysis

---

### Step 2: Sustainability Metrics

**Required Metrics:**

#### **Total Capacity (MW)**
- Your facility's total power capacity in megawatts
- Range: 1 - 10,000 MW
- Used for calculating annual emissions and energy consumption

#### **PUE (Power Usage Effectiveness)**
- Ratio of total facility energy to IT equipment energy
- Range: 1.0 - 3.0
- **Benchmarks:**
  - 1.0 = Perfect efficiency (theoretical)
  - 1.2 = Excellent (hyperscale best practice)
  - 1.5 = Good (industry average)
  - 1.75+ = Needs improvement (triggers anomaly alert)

#### **Grid Carbon Intensity (gCO2/kWh)**
- Your local grid's carbon emissions per kilowatt-hour
- Range: 0 - 1000 gCO2/kWh
- **How to find this:**
  - Check your utility provider's sustainability report
  - Use [Electricity Maps](https://app.electricitymaps.com/)
  - Contact your grid operator
- **Examples:**
  - Sweden: ~22 gCO2/kWh (hydro/nuclear)
  - Germany: ~284 gCO2/kWh (mixed)
  - Virginia, USA: ~412 gCO2/kWh (coal/gas)

#### **Renewable Energy Percentage**
- Percentage of your energy from renewable sources
- Range: 0 - 100%
- Includes:
  - On-site solar/wind
  - Power Purchase Agreements (PPAs)
  - Renewable Energy Certificates (RECs)
  - Grid renewable mix

---

### Step 3: Optional Metrics

These can be added now or updated later:

#### **WUE (Water Usage Effectiveness)**
- Liters of water per kWh of IT equipment energy
- Range: 0.1 - 10.0 L/kWh
- **Benchmarks:**
  - <0.5 = Excellent (air cooling, cold climate)
  - 0.5-1.5 = Good (efficient water cooling)
  - 1.5-2.5 = Fair (traditional cooling)
  - >2.5 = High water usage (triggers alert)

#### **CUE (Carbon Usage Effectiveness)**
- Total CO2 emissions divided by IT equipment energy
- Range: 0.0 - 2.0
- Lower is better
- Calculated automatically if not provided

#### **Monitoring Integration** (Coming Soon)
- Connect your DCIM/BMS system for real-time metrics
- Supported systems: Schneider EcoStruxure, Siemens Desigo, custom APIs

---

## What Happens After Adding a Data Center?

### Automatic Calculations

flaer automatically calculates:

1. **Risk Level** (High/Medium/Low)
   - Based on PUE, carbon intensity, and renewable percentage
   - High risk triggers immediate recommendations

2. **Annual Metrics**
   - Annual CO2 emissions (tCO2e)
   - Annual water consumption (m³)
   - Assumes 70% average utilization

3. **2035 Forecast**
   - Projected emissions trajectory
   - Based on current renewable mix and grid trends

4. **CSRD Exposure**
   - EU Corporate Sustainability Reporting Directive compliance risk
   - High for EU locations and high-carbon facilities

### AI Assistant Activation

Once you add a data center, the **flaer AI assistant** can:
- Generate weekly consumption digests
- Flag anomalies (PUE spikes, unusual consumption)
- Recommend optimization actions
- Calculate ROI for efficiency upgrades

---

## API Integration (Advanced)

### REST API Endpoints

#### Create Data Center
```bash
POST /api/data-centers
Authorization: Bearer <your_token>
Content-Type: application/json

{
  "name": "Virginia DC-1",
  "location": "Ashburn, Virginia, USA",
  "latitude": 38.9072,
  "longitude": -77.0369,
  "capacity_mw": 150,
  "pue": 1.42,
  "wue": 1.8,
  "carbon_intensity": 412,
  "renewable_pct": 48
}
```

#### Update Metrics (Real-time)
```bash
PUT /api/data-centers/{dc_id}
Authorization: Bearer <your_token>
Content-Type: application/json

{
  "pue": 1.38,
  "renewable_pct": 52,
  "carbon_intensity": 405
}
```

#### Get Portfolio Summary
```bash
GET /api/data-centers/summary
Authorization: Bearer <your_token>
```

Response:
```json
{
  "total_facilities": 3,
  "total_capacity_mw": 450,
  "avg_pue": 1.35,
  "avg_carbon_intensity": 298,
  "avg_renewable_pct": 62,
  "risk_breakdown": {
    "high": 0,
    "medium": 1,
    "low": 2
  }
}
```

---

## Data Sources & Accuracy

### Where to Get Your Metrics

#### **PUE**
- Your DCIM system (Schneider, Siemens, etc.)
- Building Management System (BMS)
- Utility bills: Total facility kWh / IT equipment kWh
- Industry average: 1.5 if unknown

#### **Carbon Intensity**
- [Electricity Maps](https://app.electricitymaps.com/) - Real-time grid data
- [WattTime](https://www.watttime.org/) - Marginal emissions API
- Your utility provider's sustainability report
- EPA eGRID database (USA)

#### **Renewable Percentage**
- Your PPA contracts
- REC purchases
- Utility renewable mix (if no PPAs)
- On-site generation meters

#### **WUE**
- Water meter readings
- Cooling tower makeup water
- Evaporative cooling systems
- Chiller plant data

---

## Best Practices

### 1. **Start with Accurate Baseline Data**
- Use actual measured values, not estimates
- Document your data sources
- Update metrics quarterly at minimum

### 2. **Set Up Regular Updates**
- Monthly: PUE, renewable %, carbon intensity
- Quarterly: Capacity changes, major upgrades
- Annual: Full audit of all metrics

### 3. **Use the AI Assistant**
- Ask for weekly digests every Friday
- Request anomaly checks after major changes
- Get optimization recommendations quarterly

### 4. **Track Improvements**
- Set PUE reduction targets (e.g., 1.5 → 1.3 by 2026)
- Increase renewable % annually
- Monitor Scope 2 emissions trend

### 5. **Benchmark Against Industry**
- Compare your PUE to similar facilities
- Use the Site IQ tool to evaluate new locations
- Learn from best-in-class examples (Stockholm: PUE 1.08)

---

## Troubleshooting

### "Data center limit reached"
- **Free tier**: 3 facilities
- **Starter**: 10 facilities
- **Professional**: 50 facilities
- **Enterprise**: Unlimited
- Upgrade your plan to add more

### "PUE above 2.5 indicates severe inefficiency"
- Verify your calculation: Total facility energy / IT equipment energy
- Check if you're including non-data center loads
- Contact support if the value is correct

### "Invalid carbon intensity"
- Must be between 0-1000 gCO2/kWh
- Check your grid operator's data
- Use Electricity Maps for verification

### Missing metrics after adding
- Some metrics are calculated automatically
- WUE/CUE are optional - add them later
- Annual metrics appear after first calculation cycle

---

## Support & Resources

### Documentation
- [API Reference](http://localhost:8000/docs)
- [Dashboard Guide](./DASHBOARD_DATA_CALCULATION_GUIDE.md)
- [AI Assistant Guide](./README.md)

### Contact
- Email: support@flaer.ai
- In-app chat: Click the help icon
- Community: [GitHub Discussions](https://github.com/flaer/community)

### Example Data Centers
The dashboard includes 14 example facilities for reference:
- Stockholm: PUE 1.08, 98% renewable (best practice)
- Frankfurt: PUE 1.24, 72% renewable (EU standard)
- Virginia: PUE 1.42, 48% renewable (US average)

---

## Next Steps

1. ✅ Add your first data center
2. ✅ Verify metrics in the portfolio view
3. ✅ Ask the AI assistant for a weekly digest
4. ✅ Set up monthly metric updates
5. ✅ Explore optimization recommendations

**Ready to start tracking?** Click **"+ Add Data Center"** in your dashboard!