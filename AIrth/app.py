import dash
from dash import dcc, html, Input, Output, State
import dash_bootstrap_components as dbc
import plotly.graph_objs as go
import pandas as pd
import numpy as np
from airth_platform import AIrthPlatform


platform = AIrthPlatform()


data_centers = [
    # North America
    ("Google Council Bluffs Iowa", (41.2619, -95.8608), 180, 850000, 0.52, 75),
    ("AWS US-East Virginia", (38.9072, -77.0369), 200, 900000, 0.45, 45),
    ("Microsoft Azure Virginia", (38.8816, -77.1045), 175, 820000, 0.45, 50),
    ("Facebook Prineville Oregon", (44.2999, -120.8342), 160, 780000, 0.28, 80),
    ("Apple Mesa Arizona", (33.4152, -111.8315), 140, 700000, 0.42, 85),
    
    # Europe
    ("Google Hamina Finland", (60.5695, 27.1978), 120, 750000, 0.15, 95),
    ("Azure Netherlands", (52.3676, 4.9041), 95, 600000, 0.35, 65),
    ("AWS Frankfurt Germany", (50.1109, 8.6821), 110, 650000, 0.38, 55),
    ("OVH Roubaix France", (50.6942, 3.1746), 85, 520000, 0.32, 60),
    ("Equinix London", (51.5074, -0.1278), 100, 580000, 0.28, 70),
    
    # Asia Pacific
    ("China Telecom Inner Mongolia", (40.8414, 111.7519), 150, 1000000, 0.65, 15),
    ("Meta Singapore", (1.3521, 103.8198), 110, 700000, 0.42, 30),
    ("AWS Tokyo Japan", (35.6762, 139.6503), 130, 720000, 0.48, 35),
    ("Alibaba Hangzhou China", (30.2741, 120.1551), 145, 850000, 0.62, 20),
    ("NTT Mumbai India", (19.0760, 72.8777), 105, 640000, 0.72, 25),
    
    # Other Regions
    ("AWS Sydney Australia", (-33.8688, 151.2093), 95, 580000, 0.82, 22),
    ("Azure São Paulo Brazil", (-23.5505, -46.6333), 88, 550000, 0.48, 40),
    ("Equinix Dubai UAE", (25.2048, 55.2708), 92, 560000, 0.55, 28),
    ("AWS Seoul South Korea", (37.5665, 126.9780), 115, 680000, 0.52, 32),
    ("Microsoft Johannesburg", (-26.2041, 28.0473), 78, 480000, 0.88, 18),
]

for name, location, power, area, carbon, renewable in data_centers:
    platform.add_data_center(name, location, power, area, carbon, renewable)

platform.train_prediction_model()


app = dash.Dash(
    __name__,
    external_stylesheets=[
        dbc.themes.BOOTSTRAP,
        'https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800;900&display=swap',
        'https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css'
    ],
    suppress_callback_exceptions=True,
    meta_tags=[{"name": "viewport", "content": "width=device-width, initial-scale=1"}]
)

app.title = "AIrth - Sustainable Energy Platform"

COLORS = {
    'primary': '#00FFA3',
    'secondary': '#7C3AED',
    'accent': '#F59E0B',
    'danger': '#FF3B5C',
    'success': '#00E676',
    'dark': '#0A0E27',
    'darker': '#050816',
    'card': '#0F1629',
    'border': 'rgba(255, 255, 255, 0.08)',
}

app.index_string = '''
<!DOCTYPE html>
<html>
<head>
    {%metas%}
    <title>{%title%}</title>
    {%favicon%}
    {%css%}
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        
        body {
            font-family: 'Inter', sans-serif;
            background: #0A0E27;
            color: #FFFFFF;
            overflow-x: hidden;
        }
        
        .app-wrapper {
            background: radial-gradient(ellipse at top, #1a1f3a 0%, #0A0E27 50%);
            min-height: 100vh;
            position: relative;
        }
        
        .app-wrapper::before {
            content: '';
            position: fixed;
            top: 0;
            left: 0;
            right: 0;
            height: 100vh;
            background: 
                radial-gradient(circle at 20% 50%, rgba(124, 58, 237, 0.15) 0%, transparent 50%),
                radial-gradient(circle at 80% 80%, rgba(0, 255, 163, 0.1) 0%, transparent 50%);
            pointer-events: none;
            z-index: 0;
        }
        
        .content-wrapper {
            position: relative;
            z-index: 1;
        }
        
        /* Premium Navbar */
        .ultra-navbar {
            background: rgba(10, 14, 39, 0.8);
            backdrop-filter: blur(40px) saturate(180%);
            border-bottom: 1px solid rgba(255, 255, 255, 0.06);
            padding: 1.5rem 0;
            position: sticky;
            top: 0;
            z-index: 1000;
            box-shadow: 0 10px 40px rgba(0, 0, 0, 0.3);
        }
        
        .logo-container {
            display: flex;
            align-items: center;
            gap: 1rem;
        }
        
        .logo-icon {
            width: 48px;
            height: 48px;
            background: linear-gradient(135deg, #00FFA3 0%, #7C3AED 100%);
            border-radius: 12px;
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 1.5rem;
            box-shadow: 0 8px 24px rgba(0, 255, 163, 0.3);
        }
        
        .logo-text {
            font-size: 1.75rem;
            font-weight: 800;
            background: linear-gradient(135deg, #00FFA3 0%, #7C3AED 100%);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            letter-spacing: -0.03em;
        }
        
        .logo-subtitle {
            font-size: 0.75rem;
            color: rgba(255, 255, 255, 0.5);
            text-transform: uppercase;
            letter-spacing: 0.15em;
            font-weight: 600;
        }
        
        /* Ultra Premium Cards */
        .ultra-card {
            background: linear-gradient(135deg, rgba(15, 22, 41, 0.9) 0%, rgba(10, 14, 39, 0.9) 100%);
            backdrop-filter: blur(40px) saturate(180%);
            border: 1px solid rgba(255, 255, 255, 0.08);
            border-radius: 24px;
            padding: 2rem;
            box-shadow: 
                0 20px 60px rgba(0, 0, 0, 0.4),
                inset 0 1px 0 rgba(255, 255, 255, 0.05);
            transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1);
            position: relative;
            overflow: hidden;
        }
        
        .ultra-card::before {
            content: '';
            position: absolute;
            top: 0;
            left: 0;
            right: 0;
            height: 2px;
            background: linear-gradient(90deg, transparent, #00FFA3, #7C3AED, transparent);
            opacity: 0;
            transition: opacity 0.4s;
        }
        
        .ultra-card:hover {
            transform: translateY(-8px);
            border-color: rgba(0, 255, 163, 0.3);
            box-shadow: 
                0 30px 80px rgba(0, 0, 0, 0.5),
                0 0 60px rgba(0, 255, 163, 0.15),
                inset 0 1px 0 rgba(255, 255, 255, 0.1);
        }
        
        .ultra-card:hover::before {
            opacity: 1;
        }
        
        /* Stat Cards */
        .stat-card-ultra {
            background: linear-gradient(135deg, rgba(15, 22, 41, 0.95) 0%, rgba(10, 14, 39, 0.95) 100%);
            border: 1px solid rgba(255, 255, 255, 0.08);
            border-radius: 20px;
            padding: 2rem;
            position: relative;
            overflow: hidden;
            transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1);
        }
        
        .stat-card-ultra::after {
            content: '';
            position: absolute;
            top: 0;
            left: 0;
            right: 0;
            bottom: 0;
            background: radial-gradient(circle at top right, var(--glow-color) 0%, transparent 70%);
            opacity: 0.1;
            transition: opacity 0.4s;
        }
        
        .stat-card-ultra:hover {
            transform: translateY(-12px) scale(1.02);
            border-color: var(--glow-color);
            box-shadow: 0 20px 60px rgba(0, 0, 0, 0.4), 0 0 40px var(--glow-shadow);
        }
        
        .stat-card-ultra:hover::after {
            opacity: 0.2;
        }
        
        .stat-icon-ultra {
            width: 64px;
            height: 64px;
            border-radius: 16px;
            background: linear-gradient(135deg, rgba(255, 255, 255, 0.1) 0%, rgba(255, 255, 255, 0.05) 100%);
            border: 1px solid rgba(255, 255, 255, 0.1);
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 1.75rem;
            margin-bottom: 1.5rem;
            color: var(--icon-color);
            box-shadow: 0 8px 24px var(--glow-shadow);
        }
        
        .stat-value-ultra {
            font-size: 2.75rem;
            font-weight: 800;
            background: linear-gradient(135deg, #FFFFFF 0%, rgba(255, 255, 255, 0.6) 100%);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            margin: 1rem 0 0.5rem 0;
            letter-spacing: -0.02em;
        }
        
        .stat-label-ultra {
            font-size: 0.875rem;
            color: rgba(255, 255, 255, 0.5);
            text-transform: uppercase;
            letter-spacing: 0.1em;
            font-weight: 600;
        }
        
        .stat-change {
            display: inline-flex;
            align-items: center;
            gap: 0.25rem;
            font-size: 0.875rem;
            font-weight: 600;
            margin-top: 0.5rem;
            padding: 0.25rem 0.75rem;
            border-radius: 100px;
            background: rgba(0, 230, 118, 0.1);
            color: #00E676;
        }
        
        /* Section Headers */
        .section-title-ultra {
            font-size: 1.5rem;
            font-weight: 700;
            color: #FFFFFF;
            margin-bottom: 1.5rem;
            display: flex;
            align-items: center;
            gap: 1rem;
        }
        
        .section-title-ultra::before {
            content: '';
            width: 4px;
            height: 28px;
            background: linear-gradient(180deg, #00FFA3 0%, #7C3AED 100%);
            border-radius: 2px;
            box-shadow: 0 0 20px rgba(0, 255, 163, 0.5);
        }
        
        /* Premium Badges */
        .ultra-badge {
            padding: 0.5rem 1rem;
            border-radius: 100px;
            font-weight: 600;
            font-size: 0.75rem;
            letter-spacing: 0.05em;
            text-transform: uppercase;
            display: inline-flex;
            align-items: center;
            gap: 0.5rem;
            border: 1px solid;
            backdrop-filter: blur(10px);
        }
        
        .badge-success-ultra {
            background: rgba(0, 230, 118, 0.15);
            border-color: rgba(0, 230, 118, 0.3);
            color: #00E676;
            box-shadow: 0 4px 12px rgba(0, 230, 118, 0.2);
        }
        
        .badge-info-ultra {
            background: rgba(124, 58, 237, 0.15);
            border-color: rgba(124, 58, 237, 0.3);
            color: #A78BFA;
            box-shadow: 0 4px 12px rgba(124, 58, 237, 0.2);
        }
        
        /* Dropdown */
        /* Dropdown Styling - Compatible with Dash */
        /* Main dropdown container */
        .Select, .dropdown {
            width: 100% !important;
        }
        
        /* Control box */
        .Select-control,
        div[class*="control"] {
            background: rgba(28, 28, 30, 0.95) !important;
            border: 1px solid rgba(255, 255, 255, 0.15) !important;
            border-radius: 12px !important;
            min-height: 52px !important;
            cursor: pointer !important;
        }
        
        .Select-control:hover,
        div[class*="control"]:hover {
            border-color: rgba(52, 199, 89, 0.4) !important;
        }
        
        /* Placeholder and value */
        .Select-placeholder,
        div[class*="placeholder"] {
            color: rgba(255, 255, 255, 0.5) !important;
            font-size: 14px !important;
        }
        
        .Select-value-label,
        div[class*="singleValue"] {
            color: #FFFFFF !important;
            font-size: 14px !important;
            font-weight: 500 !important;
        }
        
        /* Dropdown arrow */
        .Select-arrow,
        div[class*="indicatorContainer"] {
            color: rgba(255, 255, 255, 0.6) !important;
        }
        
        /* Menu container */
        .Select-menu-outer,
        div[class*="menu"] {
            background: rgba(28, 28, 30, 0.98) !important;
            border: 1px solid rgba(255, 255, 255, 0.15) !important;
            border-radius: 12px !important;
            margin-top: 0.5rem !important;
            box-shadow: 0 10px 40px rgba(0, 0, 0, 0.5) !important;
            z-index: 9999 !important;
        }
        
        .Select-menu,
        div[class*="MenuList"] {
            max-height: 350px !important;
            padding: 0.5rem !important;
        }
        
        /* Options */
        .Select-option,
        div[class*="option"] {
            background: transparent !important;
            color: #FFFFFF !important;
            padding: 0.875rem 1rem !important;
            cursor: pointer !important;
            border-radius: 8px !important;
            margin-bottom: 0.25rem !important;
            font-size: 14px !important;
        }
        
        .Select-option:hover,
        div[class*="option"]:hover {
            background: rgba(52, 199, 89, 0.15) !important;
            color: #34C759 !important;
        }
        
        .Select-option.is-focused,
        div[class*="option--is-focused"] {
            background: rgba(52, 199, 89, 0.12) !important;
            color: #34C759 !important;
        }
        
        .Select-option.is-selected,
        div[class*="option--is-selected"] {
            background: rgba(52, 199, 89, 0.2) !important;
            color: #34C759 !important;
            font-weight: 600 !important;
        }
        
        /* Input */
        .Select-input,
        div[class*="Input"] input {
            color: #FFFFFF !important;
        }
        
        /* Hide clear button */
        .Select-clear-zone,
        div[class*="indicatorContainer"]:has(svg[class*="clear"]) {
            display: none !important;
        }
        
        /* Score Circle */
        .score-circle-ultra {
            width: 140px;
            height: 140px;
            border-radius: 50%;
            display: flex;
            flex-direction: column;
            align-items: center;
            justify-content: center;
            background: radial-gradient(circle, rgba(15, 22, 41, 0.9) 0%, rgba(10, 14, 39, 0.9) 100%);
            border: 3px solid;
            position: relative;
            box-shadow: 0 8px 32px rgba(0, 0, 0, 0.4);
        }
        
        .score-circle-ultra::before {
            content: '';
            position: absolute;
            inset: -3px;
            border-radius: 50%;
            padding: 3px;
            background: linear-gradient(135deg, var(--score-color), var(--score-color-2));
            -webkit-mask: linear-gradient(#fff 0 0) content-box, linear-gradient(#fff 0 0);
            -webkit-mask-composite: xor;
            mask-composite: exclude;
            animation: rotate 3s linear infinite;
        }
        
        @keyframes rotate {
            from { transform: rotate(0deg); }
            to { transform: rotate(360deg); }
        }
        
        /* Performance optimizations */
        * {
            -webkit-font-smoothing: antialiased;
            -moz-osx-font-smoothing: grayscale;
        }
        
        .ultra-card,
        .stat-card-ultra,
        .rec-card-ultra {
            will-change: transform;
        }
        
        .score-value-ultra {
            font-size: 3rem;
            font-weight: 800;
            color: var(--score-color);
            line-height: 1;
        }
        
        /* Recommendation Cards */
        .rec-card-ultra {
            background: rgba(15, 22, 41, 0.6);
            border: 1px solid rgba(255, 255, 255, 0.08);
            border-left: 3px solid var(--priority-color);
            border-radius: 16px;
            padding: 1.5rem;
            margin-bottom: 1rem;
            transition: all 0.3s;
            backdrop-filter: blur(20px);
        }
        
        .rec-card-ultra:hover {
            transform: translateX(8px);
            background: rgba(15, 22, 41, 0.8);
            border-color: var(--priority-color);
            box-shadow: 0 8px 32px rgba(0, 0, 0, 0.3), 0 0 20px var(--priority-glow);
        }
        
        /* Animations - Optimized */
        @keyframes fadeInUp {
            from {
                opacity: 0;
                transform: translateY(20px);
            }
            to {
                opacity: 1;
                transform: translateY(0);
            }
        }
        
        .animate-in {
            animation: fadeInUp 0.4s ease-out forwards;
        }
        
        .animate-delay-1 { animation-delay: 0.05s; opacity: 0; }
        .animate-delay-2 { animation-delay: 0.1s; opacity: 0; }
        .animate-delay-3 { animation-delay: 0.15s; opacity: 0; }
        .animate-delay-4 { animation-delay: 0.2s; opacity: 0; }
        
        /* Scrollbar */
        ::-webkit-scrollbar {
            width: 12px;
        }
        
        ::-webkit-scrollbar-track {
            background: #0A0E27;
        }
        
        ::-webkit-scrollbar-thumb {
            background: linear-gradient(180deg, #00FFA3 0%, #7C3AED 100%);
            border-radius: 6px;
            border: 2px solid #0A0E27;
        }
        
        ::-webkit-scrollbar-thumb:hover {
            background: linear-gradient(180deg, #00FFB8 0%, #8B5CF6 100%);
        }
        
        /* Chart containers */
        .chart-container {
            border-radius: 16px;
            overflow: hidden;
        }
    </style>
</head>
<body>
    {%app_entry%}
    <footer>
        {%config%}
        {%scripts%}
        {%renderer%}
    </footer>
</body>
</html>
'''

# Calculate stats
total_power = sum(dc.power_mw for dc in platform.data_centers)
total_emissions = sum(dc.carbon_emissions_tons_year for dc in platform.data_centers)
total_water = sum(dc.water_usage_liters_day for dc in platform.data_centers)
avg_renewable = np.mean([dc.renewable_percentage for dc in platform.data_centers])

# Navbar
navbar = html.Div([
    dbc.Container([
        dbc.Row([
            dbc.Col([
                html.Div([
                    html.Div([
                        html.I(className="fas fa-globe")
                    ], className="logo-icon"),
                    html.Div([
                        html.Div("AIrth", className="logo-text"),
                        html.Div("Sustainable Energy Platform", className="logo-subtitle")
                    ])
                ], className="logo-container")
            ], md=6),
            dbc.Col([
                html.Div([
                    html.Span([
                        html.I(className="fas fa-leaf", style={'marginRight': '0.5rem'}),
                        "SDG 7 & 13"
                    ], className="ultra-badge badge-success-ultra", style={'marginRight': '1rem'}),
                    html.Span([
                        html.I(className="fas fa-database", style={'marginRight': '0.5rem'}),
                        f"{len(platform.data_centers)} Data Centers"
                    ], className="ultra-badge badge-info-ultra"),
                ], style={'display': 'flex', 'justifyContent': 'flex-end', 'alignItems': 'center', 'height': '100%'})
            ], md=6)
        ], align="center")
    ], fluid=True)
], className="ultra-navbar")

# Stat cards
def create_stat_card_ultra(title, value, icon, colors, change=None):
    return html.Div([
        html.Div([
            html.Div([
                html.I(className=f"fas {icon}")
            ], className="stat-icon-ultra", style={'--icon-color': colors[0]}),
            html.Div(value, className="stat-value-ultra"),
            html.Div(title, className="stat-label-ultra"),
            html.Div([
                html.I(className="fas fa-arrow-up", style={'fontSize': '0.75rem'}),
                change if change else "Live"
            ], className="stat-change") if change else html.Div()
        ], className="stat-card-ultra", style={
            '--glow-color': colors[0],
            '--glow-shadow': f'rgba({int(colors[0][1:3], 16)}, {int(colors[0][3:5], 16)}, {int(colors[0][5:7], 16)}, 0.3)'
        })
    ], className="animate-in animate-delay-1")

stats = dbc.Row([
    dbc.Col(create_stat_card_ultra("Total Power", f"{total_power:.0f} MW", "fa-bolt", [COLORS['accent']], "12.5%"), md=3, className="mb-4"),
    dbc.Col(create_stat_card_ultra("CO₂ Emissions", f"{total_emissions/1000:.1f}k tons", "fa-smog", [COLORS['danger']], "8.3%"), md=3, className="mb-4"),
    dbc.Col(create_stat_card_ultra("Water Usage", f"{total_water/1000000:.1f}M L", "fa-tint", [COLORS['secondary']], "5.7%"), md=3, className="mb-4"),
    dbc.Col(create_stat_card_ultra("Renewable", f"{avg_renewable:.1f}%", "fa-leaf", [COLORS['success']], "15.2%"), md=3, className="mb-4"),
], style={'marginTop': '2rem'})

# Apple-quality map with premium aesthetics
def create_map():
    fig = go.Figure()
    
    # Prepare data for all markers
    lats = []
    lons = []
    texts = []
    sizes = []
    colors = []
    border_colors = []
    
    for dc in platform.data_centers:
        metrics = dc.get_metrics()
        
        # Apple-style color coding with softer tones
        if metrics['effective_emissions'] < 50000:
            color = '#34C759'  # Apple green
            border = '#30D158'
        elif metrics['effective_emissions'] < 150000:
            color = '#FF9F0A'  # Apple orange
            border = '#FFB340'
        else:
            color = '#FF453A'  # Apple red
            border = '#FF6961'
        
        # Premium hover text with Apple-style formatting
        hover_text = (
            f"<b style='font-size:15px; font-weight:600; letter-spacing:-0.02em'>{dc.name}</b>"
            f"<br><br>"
            f"<span style='color:#8E8E93'>Power</span><br>"
            f"<b style='font-size:14px'>{dc.power_mw:.0f} MW</b><br><br>"
            f"<span style='color:#8E8E93'>Annual Emissions</span><br>"
            f"<b style='font-size:14px'>{metrics['carbon_emissions_tons_year']:,.0f} tons CO₂</b><br><br>"
            f"<span style='color:#8E8E93'>Renewable Energy</span><br>"
            f"<b style='font-size:14px; color:#34C759'>{dc.renewable_percentage:.1f}%</b><br><br>"
            f"<span style='color:#8E8E93'>Water Usage</span><br>"
            f"<b style='font-size:14px'>{metrics['water_usage_liters_day']/1000000:.2f}M L/day</b>"
        )
        
        lats.append(dc.location[0])
        lons.append(dc.location[1])
        texts.append(hover_text)
        sizes.append(max(18, dc.power_mw / 7))
        colors.append(color)
        border_colors.append(border)
    
    # Add markers with Apple-quality styling
    fig.add_trace(go.Scattergeo(
        lon=lons,
        lat=lats,
        text=texts,
        mode='markers',
        marker=dict(
            size=sizes,
            color=colors,
            line=dict(width=3, color='rgba(255,255,255,0.8)'),
            opacity=0.95,
            sizemode='diameter',
            symbol='circle'
        ),
        hovertemplate='%{text}<extra></extra>',
        showlegend=False
    ))
    
    # Apple-inspired map styling
    fig.update_layout(
        geo=dict(
            projection_type='natural earth',
            showland=True,
            landcolor='#1C1C1E',  # Apple dark gray
            coastlinecolor='#3A3A3C',  # Apple medium gray
            showocean=True,
            oceancolor='#000000',  # Pure black like Apple Maps dark mode
            showcountries=True,
            countrycolor='#2C2C2E',  # Apple border gray
            bgcolor='#000000',
            showlakes=False,
            showframe=False,
            resolution=110,
            projection=dict(
                type='natural earth',
                scale=1
            )
        ),
        height=600,
        showlegend=False,
        margin=dict(l=0, r=0, t=0, b=0),
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        font=dict(
            family='-apple-system, BlinkMacSystemFont, "SF Pro Display", Inter, sans-serif',
            color='#FFFFFF',
            size=13
        ),
        hoverlabel=dict(
            bgcolor='rgba(28, 28, 30, 0.98)',  # Apple dark card
            font_size=13,
            font_family='-apple-system, BlinkMacSystemFont, "SF Pro Display", Inter, sans-serif',
            bordercolor='rgba(255,255,255,0.1)',
            align='left'
        ),
        dragmode=False,
        uirevision='constant'
    )
    
    return fig

def create_emissions_chart():
    data = []
    for dc in platform.data_centers:
        metrics = dc.get_metrics()
        data.append({
            'DC': dc.name.split()[0],
            'Total': metrics['carbon_emissions_tons_year'],
            'Effective': metrics['effective_emissions']
        })
    
    df = pd.DataFrame(data).sort_values('Total', ascending=False).head(10)
    
    fig = go.Figure()
    fig.add_trace(go.Bar(
        name='Total',
        x=df['DC'],
        y=df['Total'],
        marker=dict(color=COLORS['danger'], opacity=0.7),
        hovertemplate='%{y:,.0f} tons<extra></extra>'
    ))
    fig.add_trace(go.Bar(
        name='Effective',
        x=df['DC'],
        y=df['Effective'],
        marker=dict(color=COLORS['accent']),
        hovertemplate='%{y:,.0f} tons<extra></extra>'
    ))
    
    fig.update_layout(
        barmode='group',
        height=400,
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        font=dict(family='Inter', color='#FFFFFF'),
        xaxis=dict(showgrid=False, color='rgba(255,255,255,0.5)'),
        yaxis=dict(gridcolor='rgba(255,255,255,0.05)', color='rgba(255,255,255,0.5)'),
        legend=dict(orientation="h", y=1.1, x=0.5, xanchor="center", bgcolor='rgba(0,0,0,0)', font=dict(color='#FFFFFF'))
    )
    
    return fig

def create_renewable_chart():
    data = []
    for dc in platform.data_centers:
        data.append({'DC': dc.name.split()[0], 'Renewable': dc.renewable_percentage, 'Fossil': 100 - dc.renewable_percentage})
    
    df = pd.DataFrame(data).sort_values('Renewable', ascending=False).head(10)
    
    fig = go.Figure()
    fig.add_trace(go.Bar(name='Renewable', x=df['DC'], y=df['Renewable'], marker=dict(color=COLORS['success']), hovertemplate='%{y:.1f}%<extra></extra>'))
    fig.add_trace(go.Bar(name='Fossil', x=df['DC'], y=df['Fossil'], marker=dict(color='#475569', opacity=0.6), hovertemplate='%{y:.1f}%<extra></extra>'))
    
    fig.update_layout(
        barmode='stack',
        height=400,
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        font=dict(family='Inter', color='#FFFFFF'),
        xaxis=dict(showgrid=False, color='rgba(255,255,255,0.5)'),
        yaxis=dict(gridcolor='rgba(255,255,255,0.05)', color='rgba(255,255,255,0.5)'),
        legend=dict(orientation="h", y=1.1, x=0.5, xanchor="center", bgcolor='rgba(0,0,0,0)', font=dict(color='#FFFFFF'))
    )
    
    return fig

def create_forecast_chart(dc_name):
    dc = next((d for d in platform.data_centers if d.name == dc_name), None)
    if not dc:
        return go.Figure()
    
    predictions = platform.predictor.predict_future_emissions(dc, years_ahead=10)
    years = list(range(11))
    
    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=years, y=predictions,
        mode='lines+markers',
        line=dict(color=COLORS['danger'], width=4),
        marker=dict(size=12, color=COLORS['danger'], line=dict(width=2, color='rgba(255,255,255,0.3)')),
        fill='tozeroy',
        fillcolor='rgba(255, 59, 92, 0.1)',
        hovertemplate='Year %{x}: %{y:,.0f} tons<extra></extra>'
    ))
    
    fig.update_layout(
        height=400,
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        font=dict(family='Inter', color='#FFFFFF'),
        xaxis=dict(title="Years", gridcolor='rgba(255,255,255,0.05)', color='rgba(255,255,255,0.5)'),
        yaxis=dict(title="CO₂ Emissions", gridcolor='rgba(255,255,255,0.05)', color='rgba(255,255,255,0.5)')
    )
    
    return fig

dc_selector = html.Div([
    html.Div([
        html.Div([
            html.I(className="fas fa-database", style={'color': '#34C759', 'fontSize': '1.25rem'}),
        ], style={
            'width': '44px',
            'height': '44px',
            'borderRadius': '10px',
            'background': 'rgba(52, 199, 89, 0.12)',
            'display': 'flex',
            'alignItems': 'center',
            'justifyContent': 'center',
            'marginRight': '0.875rem',
            'border': '1px solid rgba(52, 199, 89, 0.2)'
        }),
        html.Div([
            html.Div("Data Center Selection", style={
                'fontWeight': '600',
                'fontSize': '1rem',
                'color': '#FFFFFF',
                'marginBottom': '0.125rem',
                'letterSpacing': '-0.01em'
            }),
            html.Div(f"{len(platform.data_centers)} global facilities", style={
                'fontSize': '0.8125rem',
                'color': '#8E8E93',
                'fontWeight': '500'
            })
        ])
    ], style={'display': 'flex', 'alignItems': 'center', 'marginBottom': '1.25rem'}),
    dcc.Dropdown(
        id='dc-selector',
        options=[{'label': dc.name, 'value': dc.name} for dc in platform.data_centers],
        value=platform.data_centers[0].name,
        clearable=False,
        searchable=False,
        placeholder="Select a facility...",
        style={
            'width': '100%',
            'color': '#FFFFFF'
        }
    )
], className="ultra-card", style={'padding': '1.75rem'})

def create_recommendations(dc_name):
    dc = next((d for d in platform.data_centers if d.name == dc_name), None)
    if not dc:
        return html.Div()
    
    analysis = platform.recommender.analyze_and_recommend(dc, 0.5)
    score = analysis['sustainability_score']
    
    if score >= 70:
        score_colors = [COLORS['success'], COLORS['primary']]
    elif score >= 40:
        score_colors = [COLORS['accent'], COLORS['secondary']]
    else:
        score_colors = [COLORS['danger'], COLORS['accent']]
    
    score_section = html.Div([
        html.Div([
            html.Div(f"{score:.0f}", className="score-value-ultra"),
            html.Div("/ 100", style={'fontSize': '0.875rem', 'color': 'rgba(255,255,255,0.5)'})
        ], className="score-circle-ultra", style={'--score-color': score_colors[0], '--score-color-2': score_colors[1], 'borderColor': score_colors[0]})
    ], style={'display': 'flex', 'justifyContent': 'center', 'marginBottom': '2rem'})
    
    recs = []
    for rec in analysis['recommendations']:
        priority_config = {
            'HIGH': {'color': COLORS['danger'], 'icon': 'fa-exclamation-triangle'},
            'MEDIUM': {'color': COLORS['accent'], 'icon': 'fa-info-circle'},
            'LOW': {'color': COLORS['secondary'], 'icon': 'fa-lightbulb'}
        }
        config = priority_config.get(rec['priority'], priority_config['LOW'])
        
        recs.append(html.Div([
            html.Div([
                html.I(className=f"fas {config['icon']}", style={'color': config['color'], 'fontSize': '1.5rem', 'marginRight': '1rem'}),
                html.Div([
                    html.Div([
                        html.Span(rec['priority'], style={'background': f"{config['color']}20", 'color': config['color'], 'padding': '0.25rem 0.75rem', 'borderRadius': '100px', 'fontSize': '0.75rem', 'fontWeight': '600', 'marginRight': '0.75rem'}),
                        html.Span(rec['category'], style={'fontWeight': '600', 'fontSize': '1rem'})
                    ], style={'marginBottom': '0.5rem'}),
                    html.P(rec['action'], style={'color': 'rgba(255,255,255,0.7)', 'marginBottom': '0.5rem', 'fontSize': '0.875rem'}),
                    html.Div([
                        html.I(className="fas fa-check-circle", style={'color': COLORS['success'], 'marginRight': '0.5rem'}),
                        html.Span(rec['impact'], style={'color': COLORS['success'], 'fontWeight': '500', 'fontSize': '0.875rem'})
                    ])
                ], style={'flex': '1'})
            ], style={'display': 'flex'})
        ], className="rec-card-ultra", style={'--priority-color': config['color'], '--priority-glow': f"{config['color']}40"}))
    
    return html.Div([score_section, html.Div(recs)])

# Layout
app.layout = html.Div([
    html.Div([
        navbar,
        html.Div([
            dbc.Container([
                stats,
                dbc.Row([
                    dbc.Col([
                        html.Div([
                            html.Div("Global Data Center Network", className="section-title-ultra"),
                            html.Div([
                                dcc.Graph(id='global-map', figure=create_map(), config={'displayModeBar': False})
                            ], className="chart-container")
                        ], className="ultra-card")
                    ], md=12, className="mb-4 animate-in animate-delay-2"),
                ]),
                dbc.Row([
                    dbc.Col([
                        html.Div([
                            html.Div("Emissions Analysis", className="section-title-ultra"),
                            html.Div([
                                dcc.Graph(id='emissions-chart', figure=create_emissions_chart(), config={'displayModeBar': False})
                            ], className="chart-container")
                        ], className="ultra-card")
                    ], md=6, className="mb-4 animate-in animate-delay-3"),
                    dbc.Col([
                        html.Div([
                            html.Div("Energy Mix Distribution", className="section-title-ultra"),
                            html.Div([
                                dcc.Graph(id='renewable-chart', figure=create_renewable_chart(), config={'displayModeBar': False})
                            ], className="chart-container")
                        ], className="ultra-card")
                    ], md=6, className="mb-4 animate-in animate-delay-3"),
                ]),
                dbc.Row([
                    dbc.Col([
                        dc_selector,
                        html.Div([
                            html.Div("10-Year Emissions Forecast", className="section-title-ultra"),
                            html.Div([
                                dcc.Graph(id='forecast-chart', config={'displayModeBar': False})
                            ], className="chart-container")
                        ], className="ultra-card", style={'marginTop': '1.5rem'})
                    ], md=6, className="mb-4 animate-in animate-delay-4"),
                    dbc.Col([
                        html.Div([
                            html.Div("Sustainability Report", className="section-title-ultra"),
                            html.Div(id='recommendations-card')
                        ], className="ultra-card")
                    ], md=6, className="mb-4 animate-in animate-delay-4"),
                ]),
                html.Div([
                    html.P([
                        html.I(className="fas fa-leaf", style={'color': COLORS['primary'], 'marginRight': '0.5rem'}),
                        "AIrth - Sustainable Energy Platform | Powered by AI & Machine Learning"
                    ], style={'textAlign': 'center', 'color': 'rgba(255,255,255,0.4)', 'margin': '3rem 0 1rem 0'}),
                    html.P([
                        "Supporting ",
                        html.Span("SDG 7 (Clean Energy)", style={'color': COLORS['primary'], 'fontWeight': '600'}),
                        " & ",
                        html.Span("SDG 13 (Climate Action)", style={'color': COLORS['success'], 'fontWeight': '600'})
                    ], style={'textAlign': 'center', 'color': 'rgba(255,255,255,0.4)', 'fontSize': '0.875rem'})
                ])
            ], fluid=True, style={'paddingTop': '2rem', 'paddingBottom': '3rem'})
        ], className="content-wrapper")
    ], className="app-wrapper")
])

@app.callback(
    [Output('forecast-chart', 'figure'),
     Output('recommendations-card', 'children')],
    [Input('dc-selector', 'value')]
)
def update_analysis(dc_name):
    return create_forecast_chart(dc_name), create_recommendations(dc_name)

if __name__ == '__main__':
    print("\n" + "="*70)
    print("🌍 AIrth - Ultra Premium Edition")
    print("="*70)
    print(f"\n✓ {len(platform.data_centers)} global data centers loaded")
    print("✓ AI prediction model trained")
    print("✓ Ultra-premium UI initialized")
    print("\n🚀 Starting server...")
    print("\n📱 Open: http://127.0.0.1:8050")
    print("\n⌨️  Press Ctrl+C to stop")
    print("="*70 + "\n")
    
    app.run(debug=True, host='127.0.0.1', port=8050)

# Made with Bob
