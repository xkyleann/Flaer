# 🚀 AIrth Quick Start Guide

Get the AIrth Sustainable Energy Platform running in 3 simple steps!

## Prerequisites

- Python 3.8 or higher
- pip (Python package manager)
- Web browser (Chrome, Firefox, Safari, or Edge)

## Installation & Setup

### Step 1: Install Dependencies

Open your terminal/command prompt and navigate to the AIrth directory, then run:

```bash
pip install -r requirements.txt
```

This will install all necessary packages including:
- pandas, numpy (data processing)
- scikit-learn (AI models)
- matplotlib, seaborn, plotly (visualizations)
- dash, dash-bootstrap-components (web interface)
- folium (interactive maps)

**Note:** Installation may take 2-3 minutes depending on your internet connection.

### Step 2: Run the Web Application

Start the web server with:

```bash
python src/app.py
```

You should see output like:

```
======================================================================
🌍 AIrth - Sustainable Energy Platform
======================================================================

✓ Platform initialized with 5 global data centers
✓ AI prediction model trained

🚀 Starting web server...

📱 Open your browser and navigate to:
   http://127.0.0.1:8050

⌨️  Press Ctrl+C to stop the server
======================================================================
```

### Step 3: Open in Browser

Open your web browser and go to:

```
http://127.0.0.1:8050
```

or

```
http://localhost:8050
```

## What You'll See

The web interface includes:

### 📊 Dashboard Overview
- **Global Statistics**: Total power, emissions, water usage, and renewable percentage
- **Interactive Map**: Global view of all data centers with color-coded emission levels
- **Comparison Charts**: Emissions and renewable energy mix visualizations

### 🔍 Data Center Analysis
- **Dropdown Selector**: Choose any data center for detailed analysis
- **10-Year Forecast**: AI-powered emissions predictions
- **Sustainability Recommendations**: Actionable insights with priority levels

### 💡 Features
- Real-time data visualization
- Interactive charts and maps
- AI-powered predictions
- Sustainability scoring
- Actionable recommendations

## Sample Data Centers Included

The platform comes pre-loaded with 5 real-world data centers:

1. **China Telecom Inner Mongolia** (World's largest)
   - 150 MW power, 15% renewable

2. **Google Hamina Finland**
   - 120 MW power, 85% renewable

3. **AWS US-East Virginia**
   - 200 MW power, 45% renewable

4. **Azure Netherlands**
   - 95 MW power, 60% renewable

5. **Meta Singapore**
   - 110 MW power, 30% renewable

## Troubleshooting

### Port Already in Use

If you see an error about port 8050 being in use:

```bash
python app.py
```

Then modify the last line in `app.py`:
```python
app.run(debug=True, host='127.0.0.1', port=8051)
```

### Module Not Found Error

If you get "ModuleNotFoundError", ensure all dependencies are installed:

```bash
pip install -r requirements.txt --upgrade
```

### Browser Doesn't Open Automatically

Manually open your browser and type:
```
http://127.0.0.1:8050
```

## Alternative: Command-Line Demo

If you prefer a command-line interface, run:

```bash
python airth_platform.py
```

This generates:
- `airth_global_map.html` - Interactive map
- `airth_dashboard.png` - Summary dashboard
- `emissions_forecast_*.png` - Prediction charts

## Using the Platform Programmatically

For custom analysis, see `example_usage.py`:

```bash
python example_usage.py
```

This demonstrates 6 different usage patterns.

## Next Steps

1. **Explore the Interface**: Click on different data centers to see their metrics
2. **Review Recommendations**: Check sustainability suggestions for each facility
3. **Analyze Forecasts**: Examine 10-year emission predictions
4. **Customize**: Modify `app.py` to add your own data centers

## Adding Your Own Data Center

Edit `app.py` and add to the `sample_data_centers` list:

```python
sample_data_centers = [
    # ... existing centers ...
    ("Your DC Name", (latitude, longitude), power_mw, area_sqm, carbon_intensity, renewable_pct),
]
```

Example:
```python
("My Data Center", (40.7128, -74.0060), 100, 500000, 0.4, 35),
```

Then restart the server.

## Stopping the Server

Press `Ctrl+C` in the terminal where the server is running.

## Support

For issues or questions:
- Check the main README.md for detailed documentation
- Review example_usage.py for code examples
- Examine airth_platform.py for API details

---

**Happy Analyzing! 🌱**

Make data centers sustainable, one insight at a time.
