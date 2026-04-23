from flask import Flask, jsonify, request
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# Dashboard Overview Data
DASHBOARD_OVERVIEW = {
    "health_score": 72,
    "total_emissions": 2.4,  # Million tCO2e
    "carbon_intensity": 284,  # gCO2/kWh
    "renewable_energy": 64,  # percentage
    "trajectory_2030": "on_track",
    "facilities_count": 47,
    "optimized_count": 12,
    "watch_count": 18,
    "critical_count": 2
}

DATA_CENTERS = [
    {
        "id": "virginia",
        "name": "N. Virginia",
        "location": "US East",
        "risk": "high",
        "co2": "412 g",
        "trend": "up",
        "carbon_intensity": 412,
        "capacity_mw": 150,
        "pue": 1.42,
        "renewable_pct": 48,
        "wue": 1.8,
        "cue": 0.58,
        "annual_water": "2.4M m³",
        "annual_co2": "124K tCO₂e",
        "forecast_2035": "+18%",
        "csrd_exposure": "High"
    },
    {
        "id": "singapore",
        "name": "Singapore",
        "location": "APAC",
        "risk": "high",
        "co2": "408 g",
        "trend": "up",
        "carbon_intensity": 408,
        "capacity_mw": 120,
        "pue": 1.38,
        "renewable_pct": 35,
        "wue": 2.1,
        "cue": 0.62,
        "annual_water": "1.8M m³",
        "annual_co2": "98K tCO₂e",
        "forecast_2035": "+12%",
        "csrd_exposure": "Medium"
    },
    {
        "id": "frankfurt",
        "name": "Frankfurt",
        "location": "EU West",
        "risk": "medium",
        "co2": "284 g",
        "trend": "down",
        "carbon_intensity": 284,
        "capacity_mw": 180,
        "pue": 1.24,
        "renewable_pct": 72,
        "wue": 1.2,
        "cue": 0.35,
        "annual_water": "1.2M m³",
        "annual_co2": "76K tCO₂e",
        "forecast_2035": "-15%",
        "csrd_exposure": "High"
    },
    {
        "id": "warsaw",
        "name": "Warsaw",
        "location": "EU Central",
        "risk": "low",
        "co2": "234 g",
        "trend": "down",
        "carbon_intensity": 234,
        "capacity_mw": 95,
        "pue": 1.19,
        "renewable_pct": 68,
        "wue": 1.1,
        "cue": 0.28,
        "annual_water": "0.8M m³",
        "annual_co2": "42K tCO₂e",
        "forecast_2035": "-31%",
        "csrd_exposure": "High"
    },
    {
        "id": "stockholm",
        "name": "Stockholm",
        "location": "Nordic",
        "risk": "low",
        "co2": "22 g",
        "trend": "down",
        "carbon_intensity": 22,
        "capacity_mw": 200,
        "pue": 1.08,
        "renewable_pct": 98,
        "wue": 0.4,
        "cue": 0.02,
        "annual_water": "0.3M m³",
        "annual_co2": "8K tCO₂e",
        "forecast_2035": "-5%",
        "csrd_exposure": "Low"
    }
]

FORECAST_DATA = {
    "facility": "N. Virginia cluster",
    "scenario": "SSP5-8.5",
    "years": [2025, 2027, 2030, 2033, 2035],
    "bau_emissions": [95000, 110000, 135000, 165000, 195000],
    "optimized_emissions": [95000, 98000, 105000, 110000, 115000],
    "threshold": 120000,
    "potential_reduction": 38,
    "cost_avoidance": 24,  # Million USD
    "sbti_status": "on_track"
}

PRIORITY_ACTIONS = [
    {
        "priority": "high",
        "title": "Migrate workloads from N. Virginia to Stockholm",
        "description": "Shift non-latency-sensitive compute to Nordic region with 22 gCO₂/kWh grid intensity.",
        "reduction": "18,400 tCO₂e/year",
        "cost": "$2.1M migration",
        "confidence": 92
    },
    {
        "priority": "high",
        "title": "Deploy liquid cooling in Singapore cluster",
        "description": "Replace air cooling with immersion systems to reduce PUE from 1.42 to 1.18.",
        "reduction": "8,200 tCO₂e/year",
        "cost": "$4.8M capex",
        "confidence": 88
    },
    {
        "priority": "medium",
        "title": "Negotiate 24/7 renewable PPAs in Frankfurt",
        "description": "Lock in wind + solar contracts with battery storage to achieve 95% clean energy.",
        "reduction": "12,600 tCO₂e/year",
        "cost": "$1.2M/year premium",
        "confidence": 85
    },
    {
        "priority": "medium",
        "title": "Optimize cooling schedules with AI",
        "description": "Deploy predictive algorithms to reduce cooling energy by 15% across all sites.",
        "reduction": "6,800 tCO₂e/year",
        "cost": "$380K software",
        "confidence": 78
    },
    {
        "priority": "strategic",
        "title": "Phase out coal-heavy regions by 2028",
        "description": "Exit or transform facilities in grids with >40% coal dependency.",
        "reduction": "32,000 tCO₂e/year",
        "cost": "$18M restructuring",
        "confidence": 72
    },
    {
        "priority": "strategic",
        "title": "Invest in on-site solar + storage",
        "description": "Deploy 50MW solar across 12 facilities with 4-hour battery backup.",
        "reduction": "14,200 tCO₂e/year",
        "cost": "$42M capex",
        "confidence": 81
    }
]

SITE_INTELLIGENCE = {
    "stockholm": {
        "name": "Stockholm, Sweden",
        "score": 88,
        "rating": "/ 100 — Excellent candidate",
        "summary": "Outstanding renewable energy, cool climate, strong governance",
        "recommendation": "strongly_recommended",
        "factors": [
            {"name": "Renewable energy availability", "score": 96, "note": "Grid is 98% renewable (hydro + wind); among cleanest in the world"},
            {"name": "Climate & cooling efficiency", "score": 94, "note": "Cold climate enables free cooling 10+ months/year; minimal AC needed"},
            {"name": "Water availability", "score": 82, "note": "Abundant freshwater; low stress even under climate scenarios"},
            {"name": "Regulatory environment", "score": 92, "note": "Stable, transparent, strong ESG culture; CSRD-ready infrastructure"},
            {"name": "Grid reliability & resilience", "score": 88, "note": "Highly reliable Nordic grid; excellent interconnection"},
            {"name": "Land & infrastructure cost", "score": 76, "note": "Moderate costs offset by operational savings and incentives"}
        ]
    },
    "australia": {
        "name": "New South Wales, Australia",
        "score": 74,
        "rating": "/ 100 — Good candidate",
        "summary": "Strong renewable growth, good governance, but water stress risk",
        "recommendation": "good",
        "factors": [
            {"name": "Renewable energy availability", "score": 82, "note": "Grid rapidly decarbonising — 68% renewable target by 2030; solar surplus"},
            {"name": "Climate & cooling efficiency", "score": 62, "note": "Hot summers require significant cooling infrastructure; free cooling limited"},
            {"name": "Water availability", "score": 58, "note": "Water stress risk under climate scenarios; WUE targets harder to achieve"},
            {"name": "Regulatory environment", "score": 88, "note": "Strong governance, transparent regulations, active ESG reporting culture"},
            {"name": "Grid reliability & resilience", "score": 86, "note": "High reliability; good interconnection across eastern grid"},
            {"name": "Land & infrastructure cost", "score": 74, "note": "Moderate costs; good proximity to Asia-Pacific demand centres"}
        ]
    },
    "texas": {
        "name": "Texas, USA",
        "score": 61,
        "rating": "/ 100 — Proceed with caution",
        "summary": "Low cost but grid instability, water scarcity, and high carbon intensity",
        "recommendation": "caution",
        "factors": [
            {"name": "Renewable energy availability", "score": 62, "note": "Large wind/solar capacity but grid mix still includes significant gas (~45%)"},
            {"name": "Climate & cooling efficiency", "score": 40, "note": "Extreme heat; cooling costs are among the highest in North America"},
            {"name": "Water availability", "score": 38, "note": "High water stress; aquifer depletion accelerating. WUE targets very hard to meet"},
            {"name": "Regulatory environment", "score": 72, "note": "Favourable business environment but ERCOT grid isolated; limited interconnection"},
            {"name": "Grid reliability & resilience", "score": 52, "note": "ERCOT outage risk demonstrated in 2021; winter storm vulnerability"},
            {"name": "Land & infrastructure cost", "score": 90, "note": "Very low land cost and strong incentives — primary attraction"}
        ]
    }
}

# API Endpoints
@app.get("/")
def index():
    return jsonify({
        "service": "Flaer Carbon Intelligence API",
        "version": "1.0.0",
        "status": "running",
        "endpoints": {
            "health": "/api/health",
            "dashboard_overview": "/api/dashboard/overview",
            "datacenters": "/api/dashboard/datacenters",
            "datacenter_detail": "/api/dashboard/datacenters/<id>",
            "forecast": "/api/dashboard/forecast",
            "actions": "/api/dashboard/actions",
            "site_intelligence": "/api/dashboard/site-intelligence",
            "site_detail": "/api/dashboard/site-intelligence/<id>",
            "calculator": "/api/dashboard/calculator (POST)"
        },
        "frontend_url": "http://localhost:5173"
    })

@app.get("/api/health")
def health():
    return jsonify({"status": "ok", "service": "flaer-api"})

@app.get("/api/dashboard/overview")
def dashboard_overview():
    return jsonify(DASHBOARD_OVERVIEW)

@app.get("/api/dashboard/datacenters")
def datacenters():
    return jsonify({"items": DATA_CENTERS})

@app.get("/api/dashboard/datacenters/<dc_id>")
def datacenter_detail(dc_id):
    dc = next((d for d in DATA_CENTERS if d["id"] == dc_id), None)
    if dc:
        return jsonify(dc)
    return jsonify({"error": "Data center not found"}), 404

@app.get("/api/dashboard/forecast")
def forecast():
    return jsonify(FORECAST_DATA)

@app.get("/api/dashboard/actions")
def actions():
    return jsonify({"items": PRIORITY_ACTIONS})

@app.get("/api/dashboard/site-intelligence")
def site_intelligence():
    return jsonify(SITE_INTELLIGENCE)

@app.get("/api/dashboard/site-intelligence/<site_id>")
def site_detail(site_id):
    site = SITE_INTELLIGENCE.get(site_id)
    if site:
        return jsonify(site)
    return jsonify({"error": "Site not found"}), 404

@app.post("/api/dashboard/calculator")
def calculator():
    data = request.get_json()
    servers = data.get("servers", 1000)
    pue = data.get("pue", 1.3)
    carbon_intensity = data.get("carbon_intensity", 350)
    utilization = data.get("utilization", 60)
    
    # Calculate emissions
    annual_emissions = (servers * 0.5 * 8760 * pue * carbon_intensity * (utilization / 100)) / 1000000
    monthly_cost = servers * 0.5 * 730 * 0.12 * pue
    trees_equivalent = annual_emissions * 16
    cars_equivalent = annual_emissions / 4.6
    
    return jsonify({
        "annual_emissions": round(annual_emissions, 2),
        "monthly_cost": round(monthly_cost / 1000, 0),
        "scope2_intensity": round(carbon_intensity * pue, 0),
        "trees_equivalent": round(trees_equivalent, 0),
        "cars_equivalent": round(cars_equivalent, 0)
    })

if __name__ == "__main__":
    app.run(debug=True, host="127.0.0.1", port=5001)
