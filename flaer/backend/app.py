from flask import Flask, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

PORTFOLIO_SUMMARY = {
    "brand": "Flaer",
    "workspace_title": "Carbon intelligence workspace",
    "portfolio": {
        "facilities": 25,
        "total_power_gw": 2.8,
        "avg_renewable_pct": 54,
        "high_risk_regions": 6,
        "projected_reduction_pct": 38,
        "energy_savings_eur_m": 2.1,
        "water_reduction_pct": 25,
        "csrd_sensitive_sites": 9
    }
}

REGIONAL_PRESSURE = [
    {"region": "Northern Virginia", "risk": "High", "grid_carbon_gco2_kwh": 412, "forecast_2035": "+18%"},
    {"region": "Singapore", "risk": "High", "grid_carbon_gco2_kwh": 408, "forecast_2035": "+12%"},
    {"region": "Frankfurt", "risk": "Medium", "grid_carbon_gco2_kwh": 284, "forecast_2035": "-15%"},
    {"region": "Warsaw", "risk": "Low", "grid_carbon_gco2_kwh": 234, "forecast_2035": "-31%"},
    {"region": "Stockholm", "risk": "Low", "grid_carbon_gco2_kwh": 22, "forecast_2035": "-5%"}
]

SCENARIOS = [
    {
        "name": "SSP5-8.5",
        "active": True,
        "description": "Higher warming path with steeper demand growth and greater cooling stress."
    },
    {
        "name": "Balanced transition",
        "active": False,
        "description": "Moderate grid decarbonization and incremental operational improvement."
    },
    {
        "name": "Custom scenario",
        "active": False,
        "description": "Apply renewable procurement, cooling upgrades, and workload relocation assumptions."
    },
    {
        "name": "Decision markers",
        "active": False,
        "description": "Overlay interventions directly on the chart so the forecast feels strategic, not abstract."
    }
]

RECOMMENDED_ACTIONS = [
    {
        "title": "Workload shift — Frankfurt → Stockholm",
        "rank": "High ROI",
        "impact": "−18% CO₂",
        "savings": "€420K / year",
        "effort": "Medium",
        "time_to_value": "3 months",
        "confidence": "92%"
    },
    {
        "title": "Cooling optimization — Northern Virginia",
        "rank": "Medium ROI",
        "impact": "−12% CO₂",
        "savings": "€610K / year",
        "effort": "Medium",
        "time_to_value": "2 months",
        "confidence": "95%"
    },
    {
        "title": "Renewable procurement — APAC portfolio",
        "rank": "Strategic",
        "impact": "↓ long-term emissions",
        "savings": "Strategic hedge",
        "effort": "High",
        "time_to_value": "6–12 months",
        "confidence": "88%"
    }
]

@app.get("/api/health")
def health():
    return jsonify({"status": "ok", "service": "flaer-api"})

@app.get("/api/portfolio")
def portfolio():
    return jsonify(PORTFOLIO_SUMMARY)

@app.get("/api/regions")
def regions():
    return jsonify({"items": REGIONAL_PRESSURE})

@app.get("/api/scenarios")
def scenarios():
    return jsonify({"items": SCENARIOS})

@app.get("/api/actions")
def actions():
    return jsonify({"items": RECOMMENDED_ACTIONS})

if __name__ == "__main__":
    app.run(debug=True, host="127.0.0.1", port=5001)

# Made with Bob
