import dash
from dash import dcc, html, Input, Output, State
import dash_bootstrap_components as dbc
import plotly.graph_objs as go
import pandas as pd
import numpy as np
from airth_platform import AIrthPlatform
from climate_impact_analyzer import ClimateImpactAnalyzer

platform = AIrthPlatform()
climate_analyzer = ClimateImpactAnalyzer()

data_centers = [
    # North America (10)
    ("Google Council Bluffs Iowa", (41.2619, -95.8608), 180, 850000, 0.52, 75),
    ("AWS US-East Virginia", (38.9072, -77.0369), 200, 900000, 0.45, 45),
    ("Microsoft Azure Virginia", (38.8816, -77.1045), 175, 820000, 0.45, 50),
    ("Facebook Prineville Oregon", (44.2999, -120.8342), 160, 780000, 0.28, 80),
    ("Apple Mesa Arizona", (33.4152, -111.8315), 140, 700000, 0.42, 85),
    ("Google Berkeley County SC", (33.1960, -80.0131), 165, 800000, 0.48, 55),
    ("AWS US-West Oregon", (45.5152, -122.6784), 155, 750000, 0.25, 82),
    ("Microsoft Azure Texas", (29.7604, -95.3698), 170, 820000, 0.55, 42),
    ("Digital Realty Dallas", (32.7767, -96.7970), 125, 650000, 0.58, 38),
    ("Equinix Toronto Canada", (43.6532, -79.3832), 98, 580000, 0.32, 68),
    
    # Europe (10)
    ("Google Hamina Finland", (60.5695, 27.1978), 120, 750000, 0.15, 95),
    ("Azure Netherlands", (52.3676, 4.9041), 95, 600000, 0.35, 65),
    ("AWS Frankfurt Germany", (50.1109, 8.6821), 110, 650000, 0.38, 55),
    ("OVH Roubaix France", (50.6942, 3.1746), 85, 520000, 0.32, 60),
    ("Equinix London", (51.5074, -0.1278), 100, 580000, 0.28, 70),
    ("Microsoft Azure Ireland", (53.3498, -6.2603), 135, 720000, 0.42, 62),
    ("Google St. Ghislain Belgium", (50.4674, 3.8208), 115, 680000, 0.28, 75),
    ("AWS Stockholm Sweden", (59.3293, 18.0686), 92, 560000, 0.18, 88),
    ("Yandex Moscow Russia", (55.7558, 37.6173), 105, 620000, 0.68, 12),
    ("Telefonica Madrid Spain", (40.4168, -3.7038), 88, 540000, 0.38, 58),
    
    # Asia Pacific (10)
    ("China Telecom Inner Mongolia", (40.8414, 111.7519), 150, 1000000, 0.65, 15),
    ("Meta Singapore", (1.3521, 103.8198), 110, 700000, 0.42, 30),
    ("AWS Tokyo Japan", (35.6762, 139.6503), 130, 720000, 0.48, 35),
    ("Alibaba Hangzhou China", (30.2741, 120.1551), 145, 850000, 0.62, 20),
    ("NTT Mumbai India", (19.0760, 72.8777), 105, 640000, 0.72, 25),
    ("AWS Sydney Australia", (-33.8688, 151.2093), 95, 580000, 0.82, 22),
    ("Tencent Shenzhen China", (22.5431, 114.0579), 138, 780000, 0.60, 18),
    ("SK Telecom Seoul", (37.5665, 126.9780), 115, 680000, 0.52, 32),
    ("NTT Osaka Japan", (34.6937, 135.5023), 102, 610000, 0.50, 38),
    ("Telstra Melbourne Australia", (-37.8136, 144.9631), 87, 520000, 0.85, 20),
    
    # Other Regions (5)
    ("Azure São Paulo Brazil", (-23.5505, -46.6333), 88, 550000, 0.48, 40),
    ("Equinix Dubai UAE", (25.2048, 55.2708), 92, 560000, 0.55, 28),
    ("Microsoft Johannesburg", (-26.2041, 28.0473), 78, 480000, 0.88, 18),
    ("AWS Bahrain", (26.0667, 50.5577), 85, 510000, 0.72, 15),
    ("Teraco Cape Town", (-33.9249, 18.4241), 72, 450000, 0.82, 22),
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
    suppress_callback_exceptions=True
)

app.title = "AIrth - Sustainable Energy Platform"


COLORS = {
    'primary': '#00D4FF',      # Professional cyan
    'secondary': '#6366F1',    # Indigo
    'accent': '#F59E0B',       # Amber
    'danger': '#EF4444',       # Red
    'success': '#10B981',      # Emerald
    'info': '#3B82F6',         # Blue
}

# CSS
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
            background: linear-gradient(135deg, #0A0E27 0%, #1A1F3A 50%, #0A0E27 100%);
            background-attachment: fixed;
            color: #F8FAFC;
            min-height: 100vh;
        }
        body::before {
            content: '';
            position: fixed;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            background: radial-gradient(circle at 20% 50%, rgba(124, 58, 237, 0.15) 0%, transparent 50%),
                        radial-gradient(circle at 80% 80%, rgba(0, 255, 163, 0.1) 0%, transparent 50%);
            animation: backgroundShift 20s ease infinite;
            pointer-events: none;
            z-index: 0;
        }
        @keyframes backgroundShift {
            0%, 100% { opacity: 1; transform: scale(1); }
            50% { opacity: 0.8; transform: scale(1.1); }
        }
        .container-fluid { position: relative; z-index: 1; }
        .glass-card {
            background: rgba(15, 23, 42, 0.7);
            backdrop-filter: blur(20px) saturate(180%);
            border: 1px solid rgba(255, 255, 255, 0.1);
            border-radius: 24px;
            padding: 2rem;
            box-shadow: 0 20px 60px rgba(0, 0, 0, 0.3), inset 0 1px 0 rgba(255, 255, 255, 0.1);
            transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1);
        }
        .glass-card:hover {
            transform: translateY(-8px);
            border-color: rgba(0, 255, 163, 0.3);
            box-shadow: 0 30px 80px rgba(0, 0, 0, 0.4), 0 0 40px rgba(0, 255, 163, 0.2);
        }
        .stat-card {
            background: linear-gradient(135deg, rgba(15, 23, 42, 0.9) 0%, rgba(30, 41, 59, 0.9) 100%);
            backdrop-filter: blur(20px);
            border: 1px solid rgba(255, 255, 255, 0.1);
            border-radius: 20px;
            padding: 2rem;
            text-align: center;
            transition: all 0.3s ease;
        }
        .stat-card:hover {
            transform: translateY(-5px) scale(1.02);
            box-shadow: 0 20px 40px rgba(0, 0, 0, 0.3);
        }
        .stat-icon {
            font-size: 2.5rem;
            margin-bottom: 1rem;
            animation: float 3s ease-in-out infinite;
        }
        @keyframes float {
            0%, 100% { transform: translateY(0px); }
            50% { transform: translateY(-10px); }
        }
        .stat-value {
            font-size: 2.5rem;
            font-weight: 800;
            margin-bottom: 0.5rem;
            background: linear-gradient(135deg, #00FFA3 0%, #7C3AED 100%);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
        }
        .stat-label {
            font-size: 0.875rem;
            color: rgba(248, 250, 252, 0.6);
            text-transform: uppercase;
            letter-spacing: 0.1em;
            font-weight: 600;
        }
        .premium-header {
            text-align: center;
            padding: 3rem 0 2rem 0;
        }
        .premium-title {
            font-size: 4rem;
            font-weight: 900;
            background: linear-gradient(135deg, #00FFA3 0%, #7C3AED 50%, #F59E0B 100%);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            letter-spacing: -0.03em;
            margin-bottom: 1rem;
            animation: titleGlow 3s ease-in-out infinite;
        }
        @keyframes titleGlow {
            0%, 100% { filter: drop-shadow(0 0 20px rgba(0, 255, 163, 0.3)); }
            50% { filter: drop-shadow(0 0 40px rgba(124, 58, 237, 0.5)); }
        }
        .premium-subtitle {
            font-size: 1.25rem;
            color: rgba(248, 250, 252, 0.7);
            font-weight: 500;
        }
        .premium-badge {
            display: inline-block;
            padding: 0.5rem 1.5rem;
            background: rgba(0, 255, 163, 0.1);
            border: 1px solid rgba(0, 255, 163, 0.3);
            border-radius: 50px;
            color: #00FFA3;
            font-size: 0.875rem;
            font-weight: 600;
            margin: 0 0.5rem;
        }
        .section-title {
            font-size: 1.75rem;
            font-weight: 700;
            margin-bottom: 1.5rem;
            color: #F8FAFC;
            display: flex;
            align-items: center;
            gap: 1rem;
        }
        .section-title i { color: #00FFA3; }
        .rec-card {
            background: rgba(15, 23, 42, 0.6);
            border-left: 3px solid;
            border-radius: 12px;
            padding: 1.5rem;
            margin-bottom: 1rem;
            transition: all 0.3s ease;
        }
        .rec-card:hover {
            transform: translateX(5px);
            box-shadow: 0 10px 30px rgba(0, 0, 0, 0.2);
        }
        .rec-high { border-color: #EF4444; }
        .rec-medium { border-color: #F59E0B; }
        .rec-low { border-color: #10B981; }
        @keyframes fadeInUp {
            from { opacity: 0; transform: translateY(30px); }
            to { opacity: 1; transform: translateY(0); }
        }
        .animate-in {
            animation: fadeInUp 0.6s ease-out forwards;
            opacity: 0;
        }
        .animate-delay-1 { animation-delay: 0.1s; }
        .animate-delay-2 { animation-delay: 0.2s; }
        .animate-delay-3 { animation-delay: 0.3s; }
        .animate-delay-4 { animation-delay: 0.4s; }
        .dc-card {
            background: rgba(15, 23, 42, 0.8);
            border: 1px solid rgba(255, 255, 255, 0.1);
            border-radius: 16px;
            padding: 1.5rem;
            margin-bottom: 1rem;
            transition: all 0.3s ease;
            cursor: pointer;
        }
        .dc-card:hover {
            border-color: #00FFA3;
            transform: translateX(5px);
            box-shadow: 0 10px 30px rgba(0, 255, 163, 0.2);
        }
        .dc-card.selected {
            border-color: #00FFA3;
            background: rgba(0, 255, 163, 0.1);
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

# stats
total_power = sum(dc.power_mw for dc in platform.data_centers)
total_emissions = sum(dc.carbon_emissions_tons_year for dc in platform.data_centers)
total_water = sum(dc.water_usage_liters_day for dc in platform.data_centers)
avg_renewable = np.mean([dc.renewable_percentage for dc in platform.data_centers])

# Create stat cards
def create_stat_card(title, value, icon, color):
    return html.Div([
        html.I(className=f"fas {icon} stat-icon", style={'color': color}),
        html.Div(value, className="stat-value"),
        html.Div(title, className="stat-label")
    ], className="stat-card")

# Create enhanced map with better visualization
def create_map():
    fig = go.Figure()
    
    green_dcs = []
    yellow_dcs = []
    red_dcs = []
    
    for dc in platform.data_centers:
        metrics = dc.get_metrics()
        
        hover_text = f"""<b style='font-size:14px'>{dc.name}</b><br>
        <br>
        <b>Power:</b> {dc.power_mw:.0f} MW<br>
        <b>Area:</b> {dc.area_sqm/1000000:.2f} million m²<br>
        <b>Emissions:</b> {metrics['effective_emissions']:,.0f} tons CO₂/year<br>
        <b>Renewable:</b> {dc.renewable_percentage:.0f}%<br>
        <b>PUE:</b> {metrics['pue']:.2f}<br>
        <b>Water Usage:</b> {dc.water_usage_liters_day/1000000:.1f}M L/day
        """
        
        if metrics['effective_emissions'] < 50000:
            green_dcs.append((dc, metrics, hover_text))
        elif metrics['effective_emissions'] < 150000:
            yellow_dcs.append((dc, metrics, hover_text))
        else:
            red_dcs.append((dc, metrics, hover_text))
    
    categories = [
        (green_dcs, '#10B981', '🟢 Low Emissions (<50k tons)'),
        (yellow_dcs, '#F59E0B', '🟡 Medium Emissions (50-150k tons)'),
        (red_dcs, '#EF4444', '🔴 High Emissions (>150k tons)')
    ]
    
    for dcs, color, legend_name in categories:
        if dcs:
            lons = [dc.location[1] for dc, _, _ in dcs]
            lats = [dc.location[0] for dc, _, _ in dcs]
            texts = [text for _, _, text in dcs]
            sizes = [max(12, dc.power_mw / 10) for dc, _, _ in dcs]
            
            fig.add_trace(go.Scattergeo(
                lon=lons,
                lat=lats,
                text=texts,
                hoverinfo='text',
                mode='markers',
                marker=dict(
                    size=sizes,
                    color=color,
                    line=dict(width=2, color='white'),
                    opacity=0.85,
                    sizemode='diameter'
                ),
                name=legend_name,
                showlegend=True
            ))
    
    fig.update_layout(
        geo=dict(
            projection_type='natural earth',
            showland=True,
            landcolor='#1E293B',
            coastlinecolor='#475569',
            showocean=True,
            oceancolor='#0F172A',
            showcountries=True,
            countrycolor='#334155',
            countrywidth=0.5,
            bgcolor='rgba(0,0,0,0)',
            showlakes=True,
            lakecolor='#0F172A'
        ),
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        margin=dict(l=0, r=0, t=40, b=0),
        height=550,
        font=dict(color='#F8FAFC', family='Inter', size=12),
        legend=dict(
            orientation='h',
            yanchor='top',
            y=0.99,
            xanchor='center',
            x=0.5,
            bgcolor='rgba(15, 23, 42, 0.8)',
            bordercolor='rgba(255, 255, 255, 0.2)',
            borderwidth=1,
            font=dict(size=11)
        ),
        hoverlabel=dict(
            bgcolor='rgba(15, 23, 42, 0.95)',
            font_size=12,
            font_family='Inter',
            bordercolor='rgba(0, 255, 163, 0.5)'
        )
    )
    
    return fig

def create_emission_heatmap():
    fig = go.Figure()
    
    # Prepare data for heatmap
    lons = []
    lats = []
    emissions = []
    names = []
    
    for dc in platform.data_centers:
        metrics = dc.get_metrics()
        lons.append(dc.location[1])
        lats.append(dc.location[0])
        emissions.append(metrics['effective_emissions'])
        names.append(dc.name)
    
    fig.add_trace(go.Densitymapbox(
        lon=lons,
        lat=lats,
        z=emissions,
        radius=50,  
        colorscale=[
            [0, 'rgba(59, 130, 246, 0.3)'],      # Blue (low)
            [0.33, 'rgba(139, 92, 246, 0.5)'],   # Purple (medium-low)
            [0.66, 'rgba(236, 72, 153, 0.7)'],   # Pink (medium-high)
            [1, 'rgba(239, 68, 68, 0.85)']       # Red (high)
        ],
        showscale=True,
        colorbar=dict(
            title=dict(
                text='<b>Annual Emissions</b><br>(tons CO₂)',
                font=dict(size=12, color='white', family='Inter', weight=600)
            ),
            tickfont=dict(size=10, color='white', family='Inter'),
            bgcolor='rgba(15, 23, 42, 0.95)',
            bordercolor='rgba(99, 102, 241, 0.5)',
            borderwidth=2,
            thickness=18,
            x=1.01,
            len=0.7,
            tickformat=',.0f',
            outlinewidth=0
        ),
        hovertemplate='<b>Emission Density</b><br>%{z:,.0f} tons/year<extra></extra>',
        name='Emission Density',
        opacity=0.8
    ))
    
    low_dcs = []
    medium_dcs = []
    high_dcs = []
    
    for dc in platform.data_centers:
        metrics = dc.get_metrics()
        if metrics['effective_emissions'] < 50000:
            low_dcs.append(dc)
        elif metrics['effective_emissions'] < 150000:
            medium_dcs.append(dc)
        else:
            high_dcs.append(dc)
    
    categories = [
        (low_dcs, '#3B82F6', '● Low Emissions (<50k)', 'circle'),
        (medium_dcs, '#8B5CF6', '● Medium (50-150k)', 'circle'),
        (high_dcs, '#EF4444', '● High (>150k)', 'circle')
    ]
    
    for dcs, color, legend_name, symbol in categories:
        if dcs:
            dc_lons = [dc.location[1] for dc in dcs]
            dc_lats = [dc.location[0] for dc in dcs]
            dc_sizes = [max(14, min(30, dc.power_mw / 8)) for dc in dcs]
            
            hover_texts = []
            for dc in dcs:
                metrics = dc.get_metrics()
                hover_text = (
                    f"<b style='font-size:15px; color:white'>{dc.name}</b><br><br>"
                    f"<b>📊 Emissions:</b> {metrics['effective_emissions']:,.0f} tons/year<br>"
                    f"<b>⚡ Power:</b> {dc.power_mw:.0f} MW<br>"
                    f"<b>🏢 Area:</b> {dc.area_sqm/1000:.0f}k m²<br>"
                    f"<b>🌱 Renewable:</b> {dc.renewable_percentage:.0f}%<br>"
                    f"<b>💧 Water:</b> {dc.water_usage_liters_day/1000000:.1f}M L/day<br>"
                    f"<b>📈 PUE:</b> {metrics['pue']:.2f}"
                )
                hover_texts.append(hover_text)
            
            fig.add_trace(go.Scattermapbox(
                lon=dc_lons,
                lat=dc_lats,
                mode='markers',
                marker=dict(
                    size=dc_sizes,
                    color=color,
                    opacity=0.95,
                    symbol=symbol
                ),
                text=hover_texts,
                hoverinfo='text',
                name=legend_name,
                showlegend=True
            ))
    
    fig.update_layout(
        mapbox=dict(
            style='carto-darkmatter',
            center=dict(lat=25, lon=10),
            zoom=1.4,
            bearing=0,
            pitch=0
        ),
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        margin=dict(l=0, r=0, t=50, b=0),
        height=600,  # Increased height
        font=dict(color='#F8FAFC', family='Inter'),
        title=dict(
            text='<b style="font-size:18px">🌍 Interactive Global Emission Heatmap</b><br>'
                 '<span style="font-size:12px">Hover over markers for details | Heat density shows emission concentration</span>',
            font=dict(size=14, color='white', family='Inter'),
            x=0.5,
            xanchor='center',
            y=0.98,
            yanchor='top'
        ),
        legend=dict(
            orientation='h',
            yanchor='bottom',
            y=0.02,
            xanchor='center',
            x=0.5,
            bgcolor='rgba(15, 23, 42, 0.9)',
            bordercolor='rgba(255, 255, 255, 0.3)',
            borderwidth=2,
            font=dict(size=11, family='Inter')
        ),
        hoverlabel=dict(
            bgcolor='rgba(15, 23, 42, 0.98)',
            font_size=13,
            font_family='Inter',
            bordercolor='rgba(0, 255, 163, 0.6)',
            align='left'
        ),
        clickmode='event+select'
    )
    
    return fig

def create_emissions_chart():
    data = [{'name': dc.name, 'emissions': dc.get_metrics()['carbon_emissions_tons_year'],
             'effective': dc.get_metrics()['effective_emissions']} for dc in platform.data_centers]
    df = pd.DataFrame(data).sort_values('emissions', ascending=True).tail(10)
    fig = go.Figure()
    
    fig.add_trace(go.Bar(
        y=df['name'],
        x=df['emissions'],
        name='Total Emissions',
        orientation='h',
        marker=dict(
            color='#EF4444',
            line=dict(color='rgba(239, 68, 68, 0.3)', width=1)
        ),
        hovertemplate='<b>%{y}</b><br>Total: %{x:,.0f} tons/year<extra></extra>'
    ))
    
    fig.add_trace(go.Bar(
        y=df['name'],
        x=df['effective'],
        name='Effective (After Renewables)',
        orientation='h',
        marker=dict(
            color='#10B981',
            line=dict(color='rgba(16, 185, 129, 0.3)', width=1)
        ),
        hovertemplate='<b>%{y}</b><br>Effective: %{x:,.0f} tons/year<extra></extra>'
    ))
    
    fig.update_layout(
        xaxis_title='<b>CO₂ Emissions (tons/year)</b>',
        barmode='group',
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        font=dict(color='#F8FAFC', family='Inter', size=12),
        height=450,
        showlegend=True,
        legend=dict(
            orientation='h',
            yanchor='bottom',
            y=1.02,
            xanchor='right',
            x=1,
            bgcolor='rgba(15, 23, 42, 0.8)',
            bordercolor='rgba(255, 255, 255, 0.1)',
            borderwidth=1
        ),
        xaxis=dict(
            gridcolor='rgba(255, 255, 255, 0.08)',
            showgrid=True,
            zeroline=False,
            tickformat=',',
            title_font=dict(size=13)
        ),
        yaxis=dict(
            gridcolor='rgba(255, 255, 255, 0.05)',
            showgrid=False
        ),
        bargap=0.3,
        margin=dict(l=20, r=20, t=60, b=60)
    )
    return fig

def create_renewable_chart():
    data = [{'name': dc.name, 'renewable': dc.renewable_percentage, 'non_renewable': 100 - dc.renewable_percentage}
            for dc in platform.data_centers]
    df = pd.DataFrame(data).sort_values('renewable', ascending=False).head(10)
    fig = go.Figure()
    
    fig.add_trace(go.Bar(
        y=df['name'],
        x=df['renewable'],
        name='Renewable Energy',
        orientation='h',
        marker=dict(
            color='#10B981',
            line=dict(color='rgba(16, 185, 129, 0.3)', width=1)
        ),
        hovertemplate='<b>%{y}</b><br>Renewable: %{x:.1f}%<extra></extra>'
    ))
    
    fig.add_trace(go.Bar(
        y=df['name'],
        x=df['non_renewable'],
        name='Non-Renewable',
        orientation='h',
        marker=dict(
            color='#64748B',
            line=dict(color='rgba(100, 116, 139, 0.3)', width=1)
        ),
        hovertemplate='<b>%{y}</b><br>Non-Renewable: %{x:.1f}%<extra></extra>'
    ))
    
    fig.update_layout(
        xaxis_title='<b>Energy Mix (%)</b>',
        barmode='stack',
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        font=dict(color='#F8FAFC', family='Inter', size=12),
        height=450,
        showlegend=True,
        legend=dict(
            orientation='h',
            yanchor='bottom',
            y=1.02,
            xanchor='right',
            x=1,
            bgcolor='rgba(15, 23, 42, 0.8)',
            bordercolor='rgba(255, 255, 255, 0.1)',
            borderwidth=1
        ),
        xaxis=dict(
            gridcolor='rgba(255, 255, 255, 0.08)',
            showgrid=True,
            zeroline=False,
            range=[0, 100],
            ticksuffix='%',
            title_font=dict(size=13)
        ),
        yaxis=dict(
            gridcolor='rgba(255, 255, 255, 0.05)',
            showgrid=False
        ),
        bargap=0.3,
        margin=dict(l=20, r=20, t=60, b=60)
    )
    return fig

def create_forecast_chart(dc_name):
    dc = next((d for d in platform.data_centers if d.name == dc_name), None)
    if not dc:
        return html.Div([
            html.H4("10-Year Emissions Forecast", className="mb-4"),
            html.P("Select a data center to view forecast", style={'color': 'rgba(248, 250, 252, 0.6)'})
        ])
    
    # predictions
    predictions = platform.predictor.predict_future_emissions(dc, years_ahead=10)
    years = list(range(11))
    current_emissions = dc.carbon_emissions_tons_year
    
    # Calculate scenarios
    bau_predictions = predictions
    
    # Optimistic scenario - with 50% renewable by year 5
    optimistic_predictions = []
    for i, pred in enumerate(predictions):
        if i <= 5:
            reduction_factor = 1 - (i / 5 * 0.25)  # Gradual 25% reduction
        else:
            reduction_factor = 0.75  # Maintain 25% reduction
        optimistic_predictions.append(pred * reduction_factor)
    
    # Aggressive scenario - with 80% renewable by year 5
    aggressive_predictions = []
    for i, pred in enumerate(predictions):
        if i <= 5:
            reduction_factor = 1 - (i / 5 * 0.45)  # Gradual 45% reduction
        else:
            reduction_factor = 0.55  # Maintain 45% reduction
        aggressive_predictions.append(pred * reduction_factor)
    
    fig = go.Figure()
    
    # BAU 
    fig.add_trace(go.Scatter(
        x=years, y=bau_predictions,
        mode='lines+markers',
        name='Business as Usual',
        line=dict(color='#EF4444', width=3),
        marker=dict(size=8),
        fill='tozeroy',
        fillcolor='rgba(239, 68, 68, 0.1)',
        hovertemplate='Year %{x}<br>Emissions: %{y:,.0f} tons CO₂<extra></extra>'
    ))
    
    # Optimistic scenario
    fig.add_trace(go.Scatter(
        x=years, y=optimistic_predictions,
        mode='lines+markers',
        name='Optimistic (50% Renewable)',
        line=dict(color='#F59E0B', width=2, dash='dot'),
        marker=dict(size=6),
        hovertemplate='Year %{x}<br>Emissions: %{y:,.0f} tons CO₂<extra></extra>'
    ))
    
    # Aggressive scenario
    fig.add_trace(go.Scatter(
        x=years, y=aggressive_predictions,
        mode='lines+markers',
        name='Aggressive (80% Renewable)',
        line=dict(color='#10B981', width=2, dash='dot'),
        marker=dict(size=6),
        hovertemplate='Year %{x}<br>Emissions: %{y:,.0f} tons CO₂<extra></extra>'
    ))
    
    # Current baseline
    fig.add_trace(go.Scatter(
        x=years, y=[current_emissions] * 11,
        mode='lines',
        name='Current Baseline',
        line=dict(color='#64748B', width=2, dash='dash'),
        hovertemplate='Current: %{y:,.0f} tons CO₂<extra></extra>'
    ))
    
    fig.update_layout(
        xaxis_title='Years from Now',
        yaxis_title='CO₂ Emissions (tons/year)',
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        font=dict(color='#F8FAFC'),
        height=450,
        xaxis=dict(gridcolor='rgba(255, 255, 255, 0.1)'),
        yaxis=dict(gridcolor='rgba(255, 255, 255, 0.1)'),
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="right",
            x=1
        ),
        hovermode='x unified'
    )
    
    # key metrics
    total_bau = sum(bau_predictions)
    total_optimistic = sum(optimistic_predictions)
    total_aggressive = sum(aggressive_predictions)
    
    savings_optimistic = total_bau - total_optimistic
    savings_aggressive = total_bau - total_aggressive
    
    # comprehensive forecast section
    return html.Div([
        html.Div([
            html.H4("10-Year Emissions Forecast", className="mb-2", style={'color': '#F8FAFC'}),
            html.P("AI-powered predictions using Random Forest ML with IPCC SSP5-8.5 climate scenario",
                  style={'color': 'rgba(248, 250, 252, 0.6)', 'fontSize': '0.875rem', 'marginBottom': '1.5rem'})
        ]),
        
        dcc.Graph(figure=fig, config={'displayModeBar': False}),
        
        html.Details([
            html.Summary([
                html.I(className="fas fa-microscope me-2"),
                "Forecast Methodology"
            ], style={
                'cursor': 'pointer',
                'fontWeight': '600',
                'color': '#00FFA3',
                'marginTop': '1rem',
                'marginBottom': '0.5rem'
            }),
            html.Div([
                html.P([
                    html.Strong("Model: "),
                    "Random Forest Regressor (100 estimators) trained on 35 global data centers"
                ], style={'color': 'rgba(248, 250, 252, 0.8)', 'fontSize': '0.875rem', 'marginBottom': '0.5rem'}),
                html.P([
                    html.Strong("Climate Scenario: "),
                    "IPCC SSP5-8.5 (high emissions pathway, +0.2°C per year)"
                ], style={'color': 'rgba(248, 250, 252, 0.8)', 'fontSize': '0.875rem', 'marginBottom': '0.5rem'}),
                html.P([
                    html.Strong("Growth Factors: "),
                    "15% annual energy demand growth (IEA projection), 5% cooling penalty per 0.2°C temperature increase"
                ], style={'color': 'rgba(248, 250, 252, 0.8)', 'fontSize': '0.875rem', 'marginBottom': '0.5rem'}),
                html.P([
                    html.Strong("Validation: "),
                    "Model predictions align with IEA data center energy consumption forecasts"
                ], style={'color': 'rgba(248, 250, 252, 0.8)', 'fontSize': '0.875rem'})
            ], style={'marginTop': '0.5rem', 'paddingLeft': '1rem', 'borderLeft': '3px solid #00FFA3'})
        ], style={'marginBottom': '1rem'}),
        
        # Scenario Analysis
        html.Details([
            html.Summary([
                html.I(className="fas fa-chart-bar me-2"),
                "Scenario Analysis"
            ], style={
                'cursor': 'pointer',
                'fontWeight': '600',
                'color': '#00FFA3',
                'marginBottom': '0.5rem'
            }),
            html.Div([
                # BAU
                html.Div([
                    html.H6("Business as Usual (BAU)", style={'color': '#EF4444', 'marginBottom': '0.5rem'}),
                    html.P(f"Total 10-year emissions: {total_bau:,.0f} tons CO₂",
                          style={'color': 'rgba(248, 250, 252, 0.8)', 'fontSize': '0.875rem', 'marginBottom': '0.25rem'}),
                    html.P(f"Year 10 emissions: {bau_predictions[-1]:,.0f} tons CO₂ ({((bau_predictions[-1]/current_emissions - 1) * 100):.1f}% increase)",
                          style={'color': 'rgba(248, 250, 252, 0.6)', 'fontSize': '0.875rem', 'marginBottom': '1rem'})
                ]),
                
                # Optimistic
                html.Div([
                    html.H6("Optimistic Scenario", style={'color': '#F59E0B', 'marginBottom': '0.5rem'}),
                    html.P(f"Total 10-year emissions: {total_optimistic:,.0f} tons CO₂",
                          style={'color': 'rgba(248, 250, 252, 0.8)', 'fontSize': '0.875rem', 'marginBottom': '0.25rem'}),
                    html.P(f"Savings vs BAU: {savings_optimistic:,.0f} tons CO₂ ({(savings_optimistic/total_bau * 100):.1f}% reduction)",
                          style={'color': '#10B981', 'fontSize': '0.875rem', 'marginBottom': '0.25rem'}),
                    html.P("Assumes: 50% renewable energy by year 5, maintained thereafter",
                          style={'color': 'rgba(248, 250, 252, 0.6)', 'fontSize': '0.75rem', 'fontStyle': 'italic', 'marginBottom': '1rem'})
                ]),
                
                # Aggressive
                html.Div([
                    html.H6("Aggressive Scenario", style={'color': '#10B981', 'marginBottom': '0.5rem'}),
                    html.P(f"Total 10-year emissions: {total_aggressive:,.0f} tons CO₂",
                          style={'color': 'rgba(248, 250, 252, 0.8)', 'fontSize': '0.875rem', 'marginBottom': '0.25rem'}),
                    html.P(f"Savings vs BAU: {savings_aggressive:,.0f} tons CO₂ ({(savings_aggressive/total_bau * 100):.1f}% reduction)",
                          style={'color': '#10B981', 'fontSize': '0.875rem', 'marginBottom': '0.25rem'}),
                    html.P("Assumes: 80% renewable energy by year 5, maintained thereafter",
                          style={'color': 'rgba(248, 250, 252, 0.6)', 'fontSize': '0.75rem', 'fontStyle': 'italic'})
                ])
            ], style={'marginTop': '0.5rem', 'paddingLeft': '1rem', 'borderLeft': '3px solid #00FFA3'})
        ], style={'marginBottom': '1rem'}),
        
        # Key Insights
        html.Details([
            html.Summary([
                html.I(className="fas fa-lightbulb me-2"),
                "Key Insights & Recommendations"
            ], style={
                'cursor': 'pointer',
                'fontWeight': '600',
                'color': '#00FFA3',
                'marginBottom': '0.5rem'
            }),
            html.Div([
                html.Ul([
                    html.Li([
                        html.Strong("Urgent Action Required: "),
                        f"Without intervention, emissions will increase {((bau_predictions[-1]/current_emissions - 1) * 100):.1f}% by year 10 due to energy demand growth and climate warming"
                    ], style={'color': 'rgba(248, 250, 252, 0.8)', 'fontSize': '0.875rem', 'marginBottom': '0.5rem'}),
                    html.Li([
                        html.Strong("Renewable Energy Impact: "),
                        f"Achieving 50% renewable could save {savings_optimistic:,.0f} tons CO₂ over 10 years (equivalent to removing {int(savings_optimistic/4.6):,} cars from roads)"
                    ], style={'color': 'rgba(248, 250, 252, 0.8)', 'fontSize': '0.875rem', 'marginBottom': '0.5rem'}),
                    html.Li([
                        html.Strong("Aggressive Targets Pay Off: "),
                        f"80% renewable target saves an additional {(savings_aggressive - savings_optimistic):,.0f} tons CO₂ compared to 50% target"
                    ], style={'color': 'rgba(248, 250, 252, 0.8)', 'fontSize': '0.875rem', 'marginBottom': '0.5rem'}),
                    html.Li([
                        html.Strong("Climate Risk: "),
                        "Temperature increases will require 5% more cooling energy per 0.2°C, compounding emissions growth"
                    ], style={'color': 'rgba(248, 250, 252, 0.8)', 'fontSize': '0.875rem', 'marginBottom': '0.5rem'}),
                    html.Li([
                        html.Strong("Action Timeline: "),
                        "Early action is critical - delaying renewable integration by 2-3 years significantly reduces total savings potential"
                    ], style={'color': 'rgba(248, 250, 252, 0.8)', 'fontSize': '0.875rem'})
                ], style={'paddingLeft': '1.5rem', 'marginTop': '0.5rem'})
            ])
        ])
    ], className="glass-card", style={'padding': '1.5rem', 'marginBottom': '2rem'})

# recommendations with enhanced details
def create_recommendations(dc_name):
    dc = next((d for d in platform.data_centers if d.name == dc_name), None)
    if not dc:
        return html.Div("No data center selected")
    
    from enhanced_reporting import EnhancedReportGenerator, ReportConfig
    reporter = EnhancedReportGenerator(platform)
    
    analysis = platform.recommender.analyze_and_recommend(dc, 0.5)
    score = analysis['sustainability_score']
    score_color = '#10B981' if score > 70 else '#F59E0B' if score > 40 else '#EF4444'
    
    # Score card
    score_card = html.Div([
        html.I(className="fas fa-award", style={'fontSize': '3rem', 'color': score_color, 'marginBottom': '1rem'}),
        html.H2(f"{score:.0f}/100", style={'fontSize': '3rem', 'fontWeight': '800', 'color': score_color}),
        html.P("Sustainability Score", style={'color': 'rgba(248, 250, 252, 0.6)', 'fontSize': '0.875rem', 'textTransform': 'uppercase'}),
        html.Hr(style={'borderColor': 'rgba(255, 255, 255, 0.1)', 'margin': '1.5rem 0'}),
        html.P([html.I(className="fas fa-chart-line me-2", style={'color': '#10B981'}),
               f"Potential Reduction: {analysis['total_emission_reduction_tons']:.0f} tons CO₂/year"],
              style={'color': '#10B981', 'fontWeight': '600'})
    ], style={'textAlign': 'center', 'padding': '2rem'}, className="glass-card mb-4")
    
    rec_cards = []
    for rec in analysis['recommendations']:
        priority_colors = {'HIGH': '#EF4444', 'MEDIUM': '#F59E0B', 'LOW': '#10B981'}
        color = priority_colors.get(rec['priority'], '#64748B')
        
        detailed_steps = reporter._get_implementation_steps(rec['category'])
        timeline = reporter._get_implementation_timeline(rec['category'])
        cost_est = reporter._estimate_implementation_cost(rec['category'], dc)
        roi = reporter._calculate_recommendation_roi(rec['category'], dc, dc.get_metrics())
        success_metrics = reporter._get_success_metrics(rec['category'])
        case_studies = reporter._get_case_studies(rec['category'])
        
        card = html.Div([
            html.Div([
                html.Span([html.I(className="fas fa-exclamation-circle me-2"), rec['priority']],
                         style={'backgroundColor': f"{color}20", 'color': color, 'padding': '0.25rem 0.75rem',
                               'borderRadius': '50px', 'fontSize': '0.75rem', 'fontWeight': '700'}),
                html.H5(rec['category'], style={'marginTop': '1rem', 'color': '#F8FAFC', 'marginBottom': '0.5rem'}),
            ]),
            
            html.P([html.Strong("Action: "), rec['action']], style={'color': 'rgba(248, 250, 252, 0.8)', 'marginBottom': '0.5rem'}),
            html.P([html.Strong("Impact: "), rec['impact']], style={'color': '#10B981', 'marginBottom': '0.5rem'}),
            html.P([html.Strong("Implementation: "), rec['implementation']], style={'color': 'rgba(248, 250, 252, 0.6)', 'fontSize': '0.875rem', 'marginBottom': '1rem'}),
            
            html.Details([
                html.Summary([
                    html.I(className="fas fa-tasks me-2"),
                    "Implementation Steps"
                ], style={'cursor': 'pointer', 'fontWeight': '600', 'color': '#00FFA3', 'marginBottom': '0.5rem'}),
                html.Ol([html.Li(step, style={'color': 'rgba(248, 250, 252, 0.8)', 'fontSize': '0.875rem', 'marginBottom': '0.25rem'})
                        for step in detailed_steps], style={'paddingLeft': '1.5rem', 'marginTop': '0.5rem'})
            ], style={'marginBottom': '1rem'}),
            
            html.Details([
                html.Summary([
                    html.I(className="fas fa-clock me-2"),
                    "Timeline & Quick Wins"
                ], style={'cursor': 'pointer', 'fontWeight': '600', 'color': '#00FFA3', 'marginBottom': '0.5rem'}),
                html.Div([
                    html.P([html.Strong("Total Duration: "), timeline['total_duration']],
                          style={'color': 'rgba(248, 250, 252, 0.8)', 'fontSize': '0.875rem', 'marginBottom': '0.25rem'}),
                    html.P([html.Strong("Quick Win: "), timeline['quick_wins']],
                          style={'color': '#10B981', 'fontSize': '0.875rem', 'marginBottom': '0.25rem'}),
                ], style={'marginTop': '0.5rem'})
            ], style={'marginBottom': '1rem'}),
            
            html.Details([
                html.Summary([
                    html.I(className="fas fa-dollar-sign me-2"),
                    "Cost & ROI"
                ], style={'cursor': 'pointer', 'fontWeight': '600', 'color': '#00FFA3', 'marginBottom': '0.5rem'}),
                html.Div([
                    html.P([html.Strong("Estimated Cost: "), f"${cost_est['low_estimate']:,.0f} - ${cost_est['high_estimate']:,.0f}"],
                          style={'color': 'rgba(248, 250, 252, 0.8)', 'fontSize': '0.875rem', 'marginBottom': '0.25rem'}),
                    html.P([html.Strong("Annual Savings: "), f"${roi['annual_savings']:,.0f}"],
                          style={'color': '#10B981', 'fontSize': '0.875rem', 'marginBottom': '0.25rem'}),
                    html.P([html.Strong("Payback Period: "), f"{roi['payback_period_years']:.1f} years"],
                          style={'color': '#F59E0B', 'fontSize': '0.875rem', 'marginBottom': '0.25rem'}),
                    html.P([html.I(className="fas fa-info-circle me-1"), cost_est['notes']],
                          style={'color': 'rgba(248, 250, 252, 0.6)', 'fontSize': '0.75rem', 'fontStyle': 'italic'})
                ], style={'marginTop': '0.5rem'})
            ], style={'marginBottom': '1rem'}),
            
            html.Details([
                html.Summary([
                    html.I(className="fas fa-chart-line me-2"),
                    "Success Metrics"
                ], style={'cursor': 'pointer', 'fontWeight': '600', 'color': '#00FFA3', 'marginBottom': '0.5rem'}),
                html.Ul([html.Li(metric, style={'color': 'rgba(248, 250, 252, 0.8)', 'fontSize': '0.875rem', 'marginBottom': '0.25rem'})
                        for metric in success_metrics], style={'paddingLeft': '1.5rem', 'marginTop': '0.5rem'})
            ], style={'marginBottom': '1rem'}),
            
            html.Details([
                html.Summary([
                    html.I(className="fas fa-trophy me-2"),
                    "Case Studies"
                ], style={'cursor': 'pointer', 'fontWeight': '600', 'color': '#00FFA3', 'marginBottom': '0.5rem'}),
                html.Div([
                    html.Div([
                        html.P([html.Strong(f"{cs['company']}: "), cs['achievement']],
                              style={'color': 'rgba(248, 250, 252, 0.8)', 'fontSize': '0.875rem', 'marginBottom': '0.25rem'}),
                        html.P([html.I(className="fas fa-lightbulb me-1"), cs['key_learning']],
                              style={'color': '#F59E0B', 'fontSize': '0.75rem', 'marginBottom': '0.75rem', 'fontStyle': 'italic'})
                    ]) for cs in case_studies[:2]  # Show top 2 case studies
                ], style={'marginTop': '0.5rem'})
            ])
            
        ], className=f"rec-card rec-{rec['priority'].lower()}", style={'marginBottom': '1.5rem'})
        rec_cards.append(card)
    
    return html.Div([score_card] + rec_cards)

# INNOVATIVE: Carbon Calculator
def create_carbon_calculator(dc_name):
    dc = next((d for d in platform.data_centers if d.name == dc_name), None)
    if not dc:
        return html.Div("Select a data center")
    
    metrics = dc.get_metrics()
    trees_needed = metrics['effective_emissions'] / 0.02  # 1 tree absorbs ~20kg CO2/year
    cars_equivalent = metrics['effective_emissions'] / 4.6  # Average car emits 4.6 tons/year
    homes_powered = (dc.power_mw * 1000) / 1.2  # Average home uses 1.2 kW
    
    return html.Div([
        html.Div([
            html.I(className="fas fa-tree", style={'fontSize': '2rem', 'color': '#10B981', 'marginBottom': '0.5rem'}),
            html.H4(f"{trees_needed:,.0f}", style={'color': '#10B981', 'fontWeight': '800'}),
            html.P("Trees Needed to Offset", style={'fontSize': '0.875rem', 'color': 'rgba(248, 250, 252, 0.6)'})
        ], style={'textAlign': 'center', 'padding': '1.5rem', 'background': 'rgba(16, 185, 129, 0.1)', 'borderRadius': '12px', 'marginBottom': '1rem'}),
        html.Div([
            html.I(className="fas fa-car", style={'fontSize': '2rem', 'color': '#EF4444', 'marginBottom': '0.5rem'}),
            html.H4(f"{cars_equivalent:,.0f}", style={'color': '#EF4444', 'fontWeight': '800'}),
            html.P("Cars Equivalent", style={'fontSize': '0.875rem', 'color': 'rgba(248, 250, 252, 0.6)'})
        ], style={'textAlign': 'center', 'padding': '1.5rem', 'background': 'rgba(239, 68, 68, 0.1)', 'borderRadius': '12px', 'marginBottom': '1rem'}),
        html.Div([
            html.I(className="fas fa-home", style={'fontSize': '2rem', 'color': '#3B82F6', 'marginBottom': '0.5rem'}),
            html.H4(f"{homes_powered:,.0f}", style={'color': '#3B82F6', 'fontWeight': '800'}),
            html.P("Homes Powered", style={'fontSize': '0.875rem', 'color': 'rgba(248, 250, 252, 0.6)'})
        ], style={'textAlign': 'center', 'padding': '1.5rem', 'background': 'rgba(59, 130, 246, 0.1)', 'borderRadius': '12px'})
    ])

# INNOVATIVE: Data Center Comparison
def create_comparison(dc_name):
    dc = next((d for d in platform.data_centers if d.name == dc_name), None)
    if not dc:
        return html.Div("Select a data center", style={'color': 'white', 'padding': '2rem', 'textAlign': 'center'})
    
    # Find best and worst performers
    all_dcs_with_metrics = [(d, d.get_metrics()) for d in platform.data_centers]
    sorted_dcs = sorted(all_dcs_with_metrics, key=lambda x: x[1]['effective_emissions'])
    best, best_metrics = sorted_dcs[0]
    worst, worst_metrics = sorted_dcs[-1]
    
    def create_comparison_card(dc_obj, metrics, label, color):
        return html.Div([
            html.H6(label, style={'color': color, 'marginBottom': '1rem', 'fontWeight': '700'}),
            html.H5(dc_obj.name, style={'marginBottom': '1rem'}),
            html.Div([
                html.Div([
                    html.P("Emissions", style={'fontSize': '0.75rem', 'color': 'rgba(248, 250, 252, 0.6)', 'marginBottom': '0.25rem'}),
                    html.P(f"{metrics['effective_emissions']:,.0f} tons", style={'fontWeight': '600', 'color': color})
                ], style={'flex': '1'}),
                html.Div([
                    html.P("Renewable", style={'fontSize': '0.75rem', 'color': 'rgba(248, 250, 252, 0.6)', 'marginBottom': '0.25rem'}),
                    html.P(f"{dc_obj.renewable_percentage:.0f}%", style={'fontWeight': '600', 'color': color})
                ], style={'flex': '1'}),
                html.Div([
                    html.P("Power", style={'fontSize': '0.75rem', 'color': 'rgba(248, 250, 252, 0.6)', 'marginBottom': '0.25rem'}),
                    html.P(f"{dc_obj.power_mw:.0f} MW", style={'fontWeight': '600', 'color': color})
                ], style={'flex': '1'})
            ], style={'display': 'flex', 'gap': '1rem'})
        ], style={'padding': '1.5rem', 'background': f"{color}10", 'borderRadius': '12px', 'border': f'1px solid {color}40'})
    
    current_metrics = dc.get_metrics()
    return html.Div([
        html.H5("Industry Comparison", style={'marginBottom': '1.5rem', 'color': 'white'}),
        create_comparison_card(best, best_metrics, "🏆 Best Performer", '#10B981'),
        html.Div(style={'height': '1rem'}),
        html.Div([
            html.H6("Your Selection", style={'color': '#F59E0B', 'marginBottom': '1rem', 'fontWeight': '700'}),
            html.H5(dc.name, style={'marginBottom': '1rem'}),
            html.Div([
                html.Div([
                    html.P("Emissions", style={'fontSize': '0.75rem', 'color': 'rgba(248, 250, 252, 0.6)'}),
                    html.P(f"{current_metrics['effective_emissions']:,.0f} tons", style={'fontWeight': '600', 'color': '#F59E0B'})
                ], style={'flex': '1'}),
                html.Div([
                    html.P("Renewable", style={'fontSize': '0.75rem', 'color': 'rgba(248, 250, 252, 0.6)'}),
                    html.P(f"{dc.renewable_percentage:.0f}%", style={'fontWeight': '600', 'color': '#F59E0B'})
                ], style={'flex': '1'}),
                html.Div([
                    html.P("Power", style={'fontSize': '0.75rem', 'color': 'rgba(248, 250, 252, 0.6)'}),
                    html.P(f"{dc.power_mw:.0f} MW", style={'fontWeight': '600', 'color': '#F59E0B'})
                ], style={'flex': '1'})
            ], style={'display': 'flex', 'gap': '1rem'})
        ], style={'padding': '1.5rem', 'background': '#F59E0B10', 'borderRadius': '12px', 'border': '1px solid #F59E0B40'}),
        html.Div(style={'height': '1rem'}),
        create_comparison_card(worst, worst_metrics, "⚠️ Needs Improvement", '#EF4444')
    ])

# ADVANCED: Create efficiency metrics display
def create_efficiency_metrics(dc_name):
    dc = next((d for d in platform.data_centers if d.name == dc_name), None)
    if not dc:
        return html.Div("Select a data center")
    
    metrics = dc.get_metrics()
    
    # PUE Card
    pue = metrics['pue']
    pue_color = '#10B981' if pue < 1.3 else '#F59E0B' if pue < 1.7 else '#EF4444'
    pue_rating = 'Excellent' if pue < 1.3 else 'Good' if pue < 1.7 else 'Needs Improvement'
    
    # WUE Card
    wue = metrics['wue']
    wue_color = '#10B981' if wue < 1.8 else '#F59E0B' if wue < 3.0 else '#EF4444'
    wue_rating = 'Excellent' if wue < 1.8 else 'Good' if wue < 3.0 else 'Needs Improvement'
    
    # CUE Card
    cue = metrics['cue']
    cue_color = '#10B981' if cue < 0.3 else '#F59E0B' if cue < 0.5 else '#EF4444'
    cue_rating = 'Excellent' if cue < 0.3 else 'Good' if cue < 0.5 else 'Needs Improvement'
    
    return html.Div([
        dbc.Row([
            dbc.Col([
                html.Div([
                    html.Div([
                        html.I(className="fas fa-plug", style={'fontSize': '2rem', 'color': pue_color, 'marginBottom': '0.5rem'}),
                        html.H3(f"{pue:.2f}", style={'color': pue_color, 'fontWeight': '800', 'marginBottom': '0.25rem'}),
                        html.P("PUE", style={'fontSize': '0.875rem', 'color': 'rgba(248, 250, 252, 0.6)', 'marginBottom': '0.5rem'}),
                        html.Span(pue_rating, style={
                            'backgroundColor': f"{pue_color}20",
                            'color': pue_color,
                            'padding': '0.25rem 0.75rem',
                            'borderRadius': '50px',
                            'fontSize': '0.75rem',
                            'fontWeight': '600'
                        })
                    ], style={'textAlign': 'center', 'padding': '1.5rem', 'background': f"{pue_color}10", 'borderRadius': '12px', 'border': f'1px solid {pue_color}40'})
                ])
            ], md=4),
            dbc.Col([
                html.Div([
                    html.Div([
                        html.I(className="fas fa-tint", style={'fontSize': '2rem', 'color': wue_color, 'marginBottom': '0.5rem'}),
                        html.H3(f"{wue:.2f}", style={'color': wue_color, 'fontWeight': '800', 'marginBottom': '0.25rem'}),
                        html.P("WUE (L/kWh)", style={'fontSize': '0.875rem', 'color': 'rgba(248, 250, 252, 0.6)', 'marginBottom': '0.5rem'}),
                        html.Span(wue_rating, style={
                            'backgroundColor': f"{wue_color}20",
                            'color': wue_color,
                            'padding': '0.25rem 0.75rem',
                            'borderRadius': '50px',
                            'fontSize': '0.75rem',
                            'fontWeight': '600'
                        })
                    ], style={'textAlign': 'center', 'padding': '1.5rem', 'background': f"{wue_color}10", 'borderRadius': '12px', 'border': f'1px solid {wue_color}40'})
                ])
            ], md=4),
            dbc.Col([
                html.Div([
                    html.Div([
                        html.I(className="fas fa-smog", style={'fontSize': '2rem', 'color': cue_color, 'marginBottom': '0.5rem'}),
                        html.H3(f"{cue:.2f}", style={'color': cue_color, 'fontWeight': '800', 'marginBottom': '0.25rem'}),
                        html.P("CUE (kg/kWh)", style={'fontSize': '0.875rem', 'color': 'rgba(248, 250, 252, 0.6)', 'marginBottom': '0.5rem'}),
                        html.Span(cue_rating, style={
                            'backgroundColor': f"{cue_color}20",
                            'color': cue_color,
                            'padding': '0.25rem 0.75rem',
                            'borderRadius': '50px',
                            'fontSize': '0.75rem',
                            'fontWeight': '600'
                        })
                    ], style={'textAlign': 'center', 'padding': '1.5rem', 'background': f"{cue_color}10", 'borderRadius': '12px', 'border': f'1px solid {cue_color}40'})
                ])
            ], md=4),
        ]),
        html.Div([
            html.P([
                html.Strong("PUE (Power Usage Effectiveness): "),
                "Ratio of total facility energy to IT equipment energy. Lower is better. Target: <1.3"
            ], style={'fontSize': '0.875rem', 'color': 'rgba(248, 250, 252, 0.6)', 'marginTop': '1rem', 'marginBottom': '0.5rem'}),
            html.P([
                html.Strong("WUE (Water Usage Effectiveness): "),
                "Liters of water per kWh of IT equipment energy. Target: <1.8 L/kWh"
            ], style={'fontSize': '0.875rem', 'color': 'rgba(248, 250, 252, 0.6)', 'marginBottom': '0.5rem'}),
            html.P([
                html.Strong("CUE (Carbon Usage Effectiveness): "),
                "Kilograms of CO₂ per kWh of IT equipment energy. Lower is better."
            ], style={'fontSize': '0.875rem', 'color': 'rgba(248, 250, 252, 0.6)', 'marginBottom': '0'})
        ])
    ])

# ADVANCED: Create cost analysis
def create_cost_analysis(dc_name):
    dc = next((d for d in platform.data_centers if d.name == dc_name), None)
    if not dc:
        return html.Div("Select a data center")
    
    metrics = dc.get_metrics()
    roi = dc.calculate_roi_renewable(5000000)  # $5M investment example
    
    return html.Div([
        html.H5("Annual Operational Costs", style={'marginBottom': '1.5rem', 'color': '#F8FAFC'}),
        html.Div([
            html.Div([
                html.I(className="fas fa-bolt", style={'fontSize': '1.5rem', 'color': '#F59E0B', 'marginBottom': '0.5rem'}),
                html.H4(f"${metrics['energy_cost_usd']:,.0f}", style={'color': '#F59E0B', 'fontWeight': '700'}),
                html.P("Energy Cost", style={'fontSize': '0.875rem', 'color': 'rgba(248, 250, 252, 0.6)'})
            ], style={'textAlign': 'center', 'padding': '1rem', 'background': 'rgba(245, 158, 11, 0.1)', 'borderRadius': '12px', 'flex': '1'}),
            html.Div([
                html.I(className="fas fa-tint", style={'fontSize': '1.5rem', 'color': '#3B82F6', 'marginBottom': '0.5rem'}),
                html.H4(f"${metrics['water_cost_usd']:,.0f}", style={'color': '#3B82F6', 'fontWeight': '700'}),
                html.P("Water Cost", style={'fontSize': '0.875rem', 'color': 'rgba(248, 250, 252, 0.6)'})
            ], style={'textAlign': 'center', 'padding': '1rem', 'background': 'rgba(59, 130, 246, 0.1)', 'borderRadius': '12px', 'flex': '1'}),
            html.Div([
                html.I(className="fas fa-smog", style={'fontSize': '1.5rem', 'color': '#EF4444', 'marginBottom': '0.5rem'}),
                html.H4(f"${metrics['carbon_cost_usd']:,.0f}", style={'color': '#EF4444', 'fontWeight': '700'}),
                html.P("Carbon Cost", style={'fontSize': '0.875rem', 'color': 'rgba(248, 250, 252, 0.6)'})
            ], style={'textAlign': 'center', 'padding': '1rem', 'background': 'rgba(239, 68, 68, 0.1)', 'borderRadius': '12px', 'flex': '1'}),
        ], style={'display': 'flex', 'gap': '1rem', 'marginBottom': '1.5rem'}),
        
        html.Div([
            html.H4(f"${metrics['total_cost_usd']:,.0f}", style={'color': '#10B981', 'fontWeight': '800', 'fontSize': '2rem', 'marginBottom': '0.5rem'}),
            html.P("Total Annual Cost", style={'fontSize': '1rem', 'color': 'rgba(248, 250, 252, 0.7)', 'marginBottom': '1rem'}),
            html.P([
                html.I(className="fas fa-chart-line me-2"),
                f"Potential Savings: ${metrics['potential_savings_usd']:,.0f}/year with 50% renewable"
            ], style={'color': '#10B981', 'fontWeight': '600'})
        ], style={'textAlign': 'center', 'padding': '1.5rem', 'background': 'rgba(16, 185, 129, 0.1)', 'borderRadius': '12px', 'border': '1px solid rgba(16, 185, 129, 0.3)', 'marginBottom': '1.5rem'}),
        
        html.Hr(style={'borderColor': 'rgba(255, 255, 255, 0.1)', 'margin': '1.5rem 0'}),
        
        html.H5("ROI Analysis: Renewable Investment", style={'marginBottom': '1rem', 'color': '#F8FAFC'}),
        html.Div([
            html.P([html.Strong("Investment: "), f"${roi['investment_usd']:,.0f}"], style={'marginBottom': '0.5rem'}),
            html.P([html.Strong("Annual Savings: "), f"${roi['annual_savings_usd']:,.0f}"], style={'marginBottom': '0.5rem', 'color': '#10B981'}),
            html.P([html.Strong("Payback Period: "), roi['payback_period']], style={'marginBottom': '0', 'color': '#F59E0B', 'fontSize': '1.1rem', 'fontWeight': '600'})
        ], style={'padding': '1rem', 'background': 'rgba(15, 23, 42, 0.6)', 'borderRadius': '12px'})
    ])

# ADVANCED: Create highly readable scope emissions chart
def create_scope_emissions_chart(dc_name):
    dc = next((d for d in platform.data_centers if d.name == dc_name), None)
    if not dc:
        return go.Figure()
    
    scope = dc.calculate_scope_emissions()
    
    #readable donut chart
    fig = go.Figure()
    
    labels = ['Scope 1 - Direct Emissions', 'Scope 2 - Electricity', 'Scope 3 - Supply Chain']
    values = [scope['scope1_tons'], scope['scope2_tons'], scope['scope3_tons']]
    colors = ['#EF4444', '#F59E0B', '#10B981']
    percentages = [v/scope['total_tons']*100 for v in values]
    
    fig.add_trace(go.Pie(
        labels=labels,
        values=values,
        hole=0.5,
        marker=dict(
            colors=colors,
            line=dict(color='white', width=3)
        ),
        textinfo='label+percent',
        textposition='outside',
        textfont=dict(size=13, color='white', family='Inter', weight='bold'),
        hovertemplate='<b>%{label}</b><br>' +
                     'Emissions: %{value:,.0f} tons CO₂/year<br>' +
                     'Percentage: %{percent}<br>' +
                     '<extra></extra>',
        pull=[0.05, 0.05, 0.05],
        rotation=90
    ))
    
    fig.add_annotation(
        text=f'<b style="font-size:24px">{scope["total_tons"]:,.0f}</b><br>' +
             f'<span style="font-size:14px">tons CO₂</span><br>' +
             f'<span style="font-size:12px; color:rgba(248,250,252,0.6)">Total Annual</span>',
        x=0.5, y=0.5,
        font=dict(size=14, color='white', family='Inter'),
        showarrow=False,
        xref='paper', yref='paper'
    )
    
    fig.update_layout(
        title=dict(
            text='<b style="font-size:16px">GHG Protocol Scope Emissions</b>',
            font=dict(size=16, color='#F8FAFC', family='Inter'),
            x=0.5,
            xanchor='center',
            y=0.98,
            yanchor='top'
        ),
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        font=dict(color='#F8FAFC', family='Inter'),
        height=450,
        showlegend=True,
        legend=dict(
            orientation='v',
            yanchor='bottom',
            y=0.02,
            xanchor='center',
            x=0.5,
            bgcolor='rgba(15, 23, 42, 0.8)',
            bordercolor='rgba(255, 255, 255, 0.2)',
            borderwidth=1,
            font=dict(size=11)
        ),
        margin=dict(t=60, b=80, l=20, r=20),
        hoverlabel=dict(
            bgcolor='rgba(15, 23, 42, 0.98)',
            font_size=13,
            font_family='Inter',
            bordercolor='rgba(0, 255, 163, 0.6)'
        )
    )
    
    return fig

def create_heat_island_map(dc_name):
    """Create map showing radiant heat island effect - similar to main map style"""
    dc = next((d for d in platform.data_centers if d.name == dc_name), None)
    if not dc:
        return go.Figure()
    
    try:
        heat_island = climate_analyzer.calculate_heat_island_effect(dc.power_mw, dc.area_sqm)
        
        fig = go.Figure()
        
        max_radius_km = heat_island['affected_radius_km']
        max_temp_increase = heat_island['estimated_temp_increase_c']
        
        num_zones = 4  # Reduced from 5 for better performance
        angles = np.linspace(0, 2*np.pi, 50)  # Reduced from 100 for better performance
        
        for i in range(num_zones, 0, -1):
            zone_radius = max_radius_km * (i / num_zones)
            zone_temp = max_temp_increase * (i / num_zones)
            opacity = 0.15 + (0.35 * i / num_zones)
            
            lat_offset = zone_radius / 111
            lon_offset = zone_radius / (111 * np.cos(np.radians(dc.location[0])))
            
            circle_lats = dc.location[0] + lat_offset * np.sin(angles)
            circle_lons = dc.location[1] + lon_offset * np.cos(angles)
            
            if i == num_zones:
                color = f'rgba(220, 38, 38, {opacity})'  # Darkest red at center
                line_color = '#DC2626'
                line_width = 2
                show_legend = True
                legend_name = f'🔥 Max Heat (+{max_temp_increase:.1f}°C)'
            elif i == 1:
                color = f'rgba(252, 165, 165, {opacity})'  # Light red at edge
                line_color = '#FCA5A5'
                line_width = 1
                show_legend = True
                legend_name = f'🌡️ Edge (+{zone_temp:.1f}°C)'
            else:
                color = f'rgba(239, 68, 68, {opacity})'  # Medium red
                line_color = '#EF4444'
                line_width = 1
                show_legend = False
                legend_name = f'Zone {i}'
            
            fig.add_trace(go.Scattergeo(
                lon=list(circle_lons) + [circle_lons[0]],
                lat=list(circle_lats) + [circle_lats[0]],
                mode='lines',
                line=dict(color=line_color, width=line_width),
                fill='toself',
                fillcolor=color,
                name=legend_name,
                showlegend=show_legend,
                hovertemplate=f'<b>Heat Zone</b><br>Radius: {zone_radius:.1f} km<br>Temp Impact: +{zone_temp:.1f}°C<extra></extra>'
            ))
        
        fig.add_trace(go.Scattergeo(
            lon=[dc.location[1]],
            lat=[dc.location[0]],
            mode='markers',
            marker=dict(
                size=18,
                color='#DC2626',
                symbol='square',
                line=dict(width=3, color='white'),
                opacity=1.0
            ),
            name=f'📍 {dc.name}',
            showlegend=True,
            hovertemplate=f'<b>{dc.name}</b><br>Power: {dc.power_mw} MW<br>Max Heat: +{max_temp_increase:.1f}°C<br>Affected Area: {max_radius_km:.1f} km<extra></extra>'
        ))
        

        fig.update_layout(
            geo=dict(
                projection_type='natural earth',
                showland=True,
                landcolor='#1E293B',
                coastlinecolor='#475569',
                showocean=True,
                oceancolor='#0F172A',
                showcountries=True,
                countrycolor='#334155',
                countrywidth=0.5,
                bgcolor='rgba(0,0,0,0)',
                showlakes=True,
                lakecolor='#0F172A',
                center=dict(lat=dc.location[0], lon=dc.location[1]),
                projection=dict(
                    scale=8  # Zoom level - adjust to show area nicely
                )
            ),
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            margin=dict(l=0, r=0, t=30, b=0),
            height=400,
            font=dict(color='#F8FAFC', family='Inter', size=11),
            showlegend=True,
            legend=dict(
                orientation='h',
                yanchor='top',
                y=0.99,
                xanchor='center',
                x=0.5,
                bgcolor='rgba(15, 23, 42, 0.8)',
                bordercolor='rgba(255, 255, 255, 0.2)',
                borderwidth=1,
                font=dict(size=10)
            ),
            title=dict(
                text=f'<b style="font-size:14px">Radiant Heat Island Effect Map</b><br><span style="font-size:11px">Affected Area: {max_radius_km:.1f} km radius | Max Temperature: +{max_temp_increase:.1f}°C</span>',
                font=dict(size=12, color='#F8FAFC', family='Inter'),
                x=0.5,
                xanchor='center',
                y=0.98,
                yanchor='top'
            ),
            hoverlabel=dict(
                bgcolor='rgba(15, 23, 42, 0.95)',
                font_size=12,
                font_family='Inter',
                bordercolor='rgba(239, 68, 68, 0.5)'
            )
        )
        
        return fig
    except Exception as e:
        print(f"Error creating heat island map: {e}")
        import traceback
        traceback.print_exc()
        return go.Figure()

#  Climate & Environmental Impact Analysis
def create_climate_impact_section(dc_name):
    """Create climate and environmental impact analysis section"""
    dc = next((d for d in platform.data_centers if d.name == dc_name), None)
    if not dc:
        return html.Div("Select a data center", style={'color': 'white', 'padding': '2rem', 'textAlign': 'center'})
    
    try:
        # Get climate data
        climate_data = climate_analyzer.get_climate_data(dc.location[0], dc.location[1])
        regional_impact = climate_analyzer.get_regional_impact(dc.location[0], dc.location[1])
        heat_island = climate_analyzer.calculate_heat_island_effect(dc.power_mw, dc.area_sqm)
        water_impact = climate_analyzer.calculate_water_impact(dc.water_usage_liters_day, regional_impact.water_stress_score)
        recommendations = climate_analyzer.generate_location_recommendations(climate_data, regional_impact)
        
        # Climate zone colors
        zone_colors = {
            'Arctic': '#A5F3FC', 'Subarctic': '#67E8F9', 'Temperate': '#10B981',
            'Subtropical': '#F59E0B', 'Tropical': '#EF4444', 'Arid': '#F97316', 'Mediterranean': '#8B5CF6'
        }
        zone_color = zone_colors.get(climate_data.zone.value, '#10B981')
        
        # Water stress colors
        stress_colors = {
            'Low': '#10B981', 'Low-Medium': '#84CC16', 'Medium-High': '#F59E0B',
            'High': '#EF4444', 'Extremely High': '#DC2626'
        }
        stress_color = stress_colors.get(regional_impact.water_stress_level.value, '#F59E0B')
        
        # Calculate climate impact on operations
        temp_impact = "High cooling demand" if climate_data.avg_temp_celsius > 25 else "Moderate cooling" if climate_data.avg_temp_celsius > 15 else "Low cooling demand"
        cooling_efficiency = "Excellent" if climate_data.free_cooling_days > 250 else "Good" if climate_data.free_cooling_days > 150 else "Limited"
        
        return html.Div([
            # Climate Impact Summary
            html.Div([
                html.H6([html.I(className="fas fa-temperature-high me-2"), "Climate Impact on Operations"],
                       style={'marginBottom': '1rem', 'color': '#F59E0B', 'fontWeight': '600'}),
                html.Div([
                    html.Div([
                        html.Strong("Temperature Impact: "),
                        html.Span(temp_impact, style={'color': '#EF4444' if 'High' in temp_impact else '#F59E0B' if 'Moderate' in temp_impact else '#10B981'})
                    ], style={'marginBottom': '0.5rem', 'fontSize': '0.875rem'}),
                    html.Div([
                        html.Strong("Free Cooling Potential: "),
                        html.Span(f"{cooling_efficiency} ({climate_data.free_cooling_days} days/year)",
                                 style={'color': '#10B981' if cooling_efficiency == 'Excellent' else '#F59E0B'})
                    ], style={'marginBottom': '0.5rem', 'fontSize': '0.875rem'}),
                    html.Div([
                        html.Strong("Extreme Weather Risk: "),
                        html.Span(climate_data.extreme_weather_risk, style={'color': '#F59E0B'})
                    ], style={'fontSize': '0.875rem'})
                ], style={'color': 'rgba(248, 250, 252, 0.8)'})
            ], style={'padding': '1rem', 'background': 'rgba(245, 158, 11, 0.1)', 'borderRadius': '12px',
                     'border': '1px solid rgba(245, 158, 11, 0.3)', 'marginBottom': '1rem'}),
            
            # Climate Zone Card
            dbc.Row([
                dbc.Col([
                    html.Div([
                        html.I(className="fas fa-cloud-sun", style={'fontSize': '2rem', 'color': zone_color, 'marginBottom': '0.5rem'}),
                        html.H4(climate_data.zone.value, style={'color': zone_color, 'fontWeight': '700', 'marginBottom': '0.25rem'}),
                        html.P("Climate Zone", style={'fontSize': '0.875rem', 'color': 'rgba(248, 250, 252, 0.6)', 'marginBottom': '0.75rem'}),
                        html.P(f"{climate_data.avg_temp_celsius:.1f}°C avg | {climate_data.humidity_avg:.0f}% humidity",
                              style={'fontSize': '0.75rem', 'color': 'rgba(248, 250, 252, 0.7)'})
                    ], style={'textAlign': 'center', 'padding': '1.5rem', 'background': f"{zone_color}15",
                             'borderRadius': '12px', 'border': f'2px solid {zone_color}40', 'height': '100%'})
                ], md=4),
                dbc.Col([
                    html.Div([
                        html.I(className="fas fa-tint", style={'fontSize': '2rem', 'color': stress_color, 'marginBottom': '0.5rem'}),
                        html.H4(regional_impact.water_stress_level.value, style={'color': stress_color, 'fontWeight': '700', 'marginBottom': '0.25rem'}),
                        html.P("Water Stress", style={'fontSize': '0.875rem', 'color': 'rgba(248, 250, 252, 0.6)', 'marginBottom': '0.75rem'}),
                        html.P(water_impact['impact_description'], style={'fontSize': '0.75rem', 'color': 'rgba(248, 250, 252, 0.7)'})
                    ], style={'textAlign': 'center', 'padding': '1.5rem', 'background': f"{stress_color}10",
                             'borderRadius': '12px', 'height': '100%'})
                ], md=4),
                dbc.Col([
                    html.Div([
                        html.I(className="fas fa-thermometer-half", style={'fontSize': '2rem', 'color': '#EF4444', 'marginBottom': '0.5rem'}),
                        html.H4(f"+{heat_island['estimated_temp_increase_c']:.1f}°C", style={'color': '#EF4444', 'fontWeight': '700', 'marginBottom': '0.25rem'}),
                        html.P("Heat Island Effect", style={'fontSize': '0.875rem', 'color': 'rgba(248, 250, 252, 0.6)', 'marginBottom': '0.75rem'}),
                        html.P(f"Radius: {heat_island['affected_radius_km']:.1f} km", style={'fontSize': '0.75rem', 'color': 'rgba(248, 250, 252, 0.7)'})
                    ], style={'textAlign': 'center', 'padding': '1.5rem', 'background': 'rgba(239, 68, 68, 0.1)',
                             'borderRadius': '12px', 'height': '100%'})
                ], md=4)
            ], className="mb-3"),
            
            # Heat Island Effect Map
            html.Div([
                dcc.Graph(figure=create_heat_island_map(dc_name), config={'displayModeBar': False})
            ], style={'marginBottom': '1rem'}),
            
            # Location Recommendations
            html.Div([
                html.H6([html.I(className="fas fa-map-marker-alt me-2"), "Location-Specific Recommendations"],
                       style={'marginBottom': '1rem', 'color': '#00FFA3', 'fontWeight': '600'}),
                html.Div([
                    html.Div([
                        html.Div([
                            html.Span(rec['priority'], style={
                                'backgroundColor': '#EF4444' if rec['priority'] == 'CRITICAL' else '#F59E0B' if rec['priority'] == 'HIGH' else '#10B981',
                                'color': 'white', 'padding': '0.15rem 0.5rem', 'borderRadius': '4px',
                                'fontSize': '0.65rem', 'fontWeight': '700', 'marginRight': '0.5rem'
                            }),
                            html.Strong(rec['category'], style={'color': '#F8FAFC', 'fontSize': '0.875rem'})
                        ], style={'marginBottom': '0.25rem'}),
                        html.P(rec['recommendation'], style={'color': 'rgba(248, 250, 252, 0.7)', 'fontSize': '0.75rem', 'marginBottom': '0.25rem'}),
                        html.P(f"💡 {rec['potential_savings']}", style={'color': '#10B981', 'fontSize': '0.7rem', 'fontStyle': 'italic'})
                    ], style={'padding': '0.75rem', 'background': 'rgba(15, 23, 42, 0.6)', 'borderRadius': '8px',
                             'marginBottom': '0.5rem', 'borderLeft': '2px solid #00FFA3'})
                    for rec in recommendations[:4]  # Show top 4 recommendations
                ])
            ], style={'padding': '1rem', 'background': 'rgba(0, 255, 163, 0.05)', 'borderRadius': '12px',
                     'border': '1px solid rgba(0, 255, 163, 0.2)'})
        ])
    except Exception as e:
        print(f"ERROR in create_climate_impact_section: {e}")
        import traceback
        traceback.print_exc()
        return html.Div([
            html.I(className="fas fa-exclamation-triangle", style={'fontSize': '2rem', 'color': '#F59E0B', 'marginBottom': '0.5rem'}),
            html.P(f"Climate analysis unavailable", style={'color': 'rgba(248, 250, 252, 0.7)'}),
            html.P(f"Error: {str(e)}", style={'color': 'rgba(248, 250, 252, 0.5)', 'fontSize': '0.75rem'})
        ], style={'textAlign': 'center', 'padding': '2rem'})

    # Find best and worst performers
    all_dcs = sorted(platform.data_centers, key=lambda x: x.get_metrics()['effective_emissions'])
    best = all_dcs[0]
    worst = all_dcs[-1]
    
    def create_comparison_card(dc_obj, label, color):
        metrics = dc_obj.get_metrics()
        return html.Div([
            html.H6(label, style={'color': color, 'marginBottom': '1rem', 'fontWeight': '700'}),
            html.H5(dc_obj.name, style={'marginBottom': '1rem'}),
            html.Div([
                html.Div([
                    html.P("Emissions", style={'fontSize': '0.75rem', 'color': 'rgba(248, 250, 252, 0.6)', 'marginBottom': '0.25rem'}),
                    html.P(f"{metrics['effective_emissions']:,.0f} tons", style={'fontWeight': '600', 'color': color})
                ], style={'flex': '1'}),
                html.Div([
                    html.P("Renewable", style={'fontSize': '0.75rem', 'color': 'rgba(248, 250, 252, 0.6)', 'marginBottom': '0.25rem'}),
                    html.P(f"{dc_obj.renewable_percentage:.0f}%", style={'fontWeight': '600', 'color': color})
                ], style={'flex': '1'}),
                html.Div([
                    html.P("Power", style={'fontSize': '0.75rem', 'color': 'rgba(248, 250, 252, 0.6)', 'marginBottom': '0.25rem'}),
                    html.P(f"{dc_obj.power_mw:.0f} MW", style={'fontWeight': '600', 'color': color})
                ], style={'flex': '1'})
            ], style={'display': 'flex', 'gap': '1rem'})
        ], style={'padding': '1.5rem', 'background': f"{color}10", 'borderRadius': '12px', 'border': f'1px solid {color}40'})
    
    current_metrics = dc.get_metrics()
    return html.Div([
        html.H5("Industry Comparison", style={'marginBottom': '1.5rem'}),
        create_comparison_card(best, "🏆 Best Performer", '#10B981'),
        html.Div(style={'height': '1rem'}),
        html.Div([
            html.H6("Your Selection", style={'color': '#F59E0B', 'marginBottom': '1rem', 'fontWeight': '700'}),
            html.H5(dc.name, style={'marginBottom': '1rem'}),
            html.Div([
                html.Div([
                    html.P("Emissions", style={'fontSize': '0.75rem', 'color': 'rgba(248, 250, 252, 0.6)'}),
                    html.P(f"{current_metrics['effective_emissions']:,.0f} tons", style={'fontWeight': '600', 'color': '#F59E0B'})
                ], style={'flex': '1'}),
                html.Div([
                    html.P("Renewable", style={'fontSize': '0.75rem', 'color': 'rgba(248, 250, 252, 0.6)'}),
                    html.P(f"{dc.renewable_percentage:.0f}%", style={'fontWeight': '600', 'color': '#F59E0B'})
                ], style={'flex': '1'}),
                html.Div([
                    html.P("Power", style={'fontSize': '0.75rem', 'color': 'rgba(248, 250, 252, 0.6)'}),
                    html.P(f"{dc.power_mw:.0f} MW", style={'fontWeight': '600', 'color': '#F59E0B'})
                ], style={'flex': '1'})
            ], style={'display': 'flex', 'gap': '1rem'})
        ], style={'padding': '1.5rem', 'background': '#F59E0B10', 'borderRadius': '12px', 'border': '1px solid #F59E0B40'}),
        html.Div(style={'height': '1rem'}),
        create_comparison_card(worst, "⚠️ Needs Improvement", '#EF4444')
    ])

# App layout
app.layout = dbc.Container([
    html.Div([
        html.H1("AIrth", className="premium-title"),
        html.P("AI-Powered Sustainable Energy Platform", className="premium-subtitle"),
        html.Div([
            html.Span([html.I(className="fas fa-leaf me-2"), "SDG 7"], className="premium-badge"),
            html.Span([html.I(className="fas fa-globe me-2"), "SDG 13"], className="premium-badge"),
            html.Span([html.I(className="fas fa-database me-2"), f"{len(platform.data_centers)} Data Centers"], className="premium-badge"),
        ], style={'marginTop': '1.5rem'})
    ], className="premium-header"),
    
    dbc.Row([
        dbc.Col(create_stat_card("Total Power", f"{total_power:.0f} MW", "fa-bolt", COLORS['accent']), md=3, className="mb-4 animate-in animate-delay-1"),
        dbc.Col(create_stat_card("CO₂ Emissions", f"{total_emissions/1000:.1f}k tons", "fa-smog", COLORS['danger']), md=3, className="mb-4 animate-in animate-delay-2"),
        dbc.Col(create_stat_card("Water Usage", f"{total_water/1000000:.1f}M L/day", "fa-tint", COLORS['info']), md=3, className="mb-4 animate-in animate-delay-3"),
        dbc.Col(create_stat_card("Renewable", f"{avg_renewable:.1f}%", "fa-leaf", COLORS['success']), md=3, className="mb-4 animate-in animate-delay-4"),
    ]),
    
    dbc.Row([
        dbc.Col([
            html.Div([
                html.Div([html.I(className="fas fa-globe-americas"), "Global Data Center Network"], className="section-title"),
                dcc.Graph(figure=create_map(), config={'displayModeBar': False})
            ], className="glass-card animate-in")
        ], className="mb-4")
    ]),
    
    dbc.Row([
        dbc.Col([
            html.Div([
                html.Div([html.I(className="fas fa-fire"), "Global Emission Heatmap"], className="section-title"),
                dcc.Graph(figure=create_emission_heatmap(), config={'displayModeBar': False})
            ], className="glass-card animate-in")
        ], className="mb-4")
    ]),
    
    dbc.Row([
        dbc.Col([
            html.Div([
                html.Div([html.I(className="fas fa-chart-bar"), "Emissions Analysis"], className="section-title"),
                dcc.Graph(figure=create_emissions_chart(), config={'displayModeBar': False})
            ], className="glass-card animate-in")
        ], md=6, className="mb-4"),
        dbc.Col([
            html.Div([
                html.Div([html.I(className="fas fa-solar-panel"), "Energy Mix Distribution"], className="section-title"),
                dcc.Graph(figure=create_renewable_chart(), config={'displayModeBar': False})
            ], className="glass-card animate-in")
        ], md=6, className="mb-4"),
    ]),
    
    dbc.Row([
        dbc.Col([
            html.Div([
                html.Div([html.I(className="fas fa-search"), "Select Data Center"], className="section-title"),
                dbc.Select(
                    id='dc-selector',
                    options=[{'label': dc.name, 'value': dc.name} for dc in platform.data_centers],
                    value=platform.data_centers[0].name,
                    className="mb-3"
                )
            ], className="glass-card animate-in")
        ], className="mb-4")
    ]),
    
    dbc.Row([
        dbc.Col([
            html.Div([
                html.Div([html.I(className="fas fa-calculator"), "Carbon Offset Calculator"], className="section-title"),
                html.Div(id='carbon-calculator')
            ], className="glass-card animate-in", style={'height': '100%'})
        ], md=6, className="mb-4"),
        dbc.Col([
            html.Div([
                html.Div([html.I(className="fas fa-globe-americas"), "Climate & Environmental Impact"], className="section-title"),
                html.Div(id='climate-impact-section')
            ], className="glass-card animate-in", style={'height': '100%'})
        ], md=6, className="mb-4"),
    ]),
    
    # NEW: Advanced Efficiency Metrics
    dbc.Row([
        dbc.Col([
            html.Div([
                html.Div([html.I(className="fas fa-tachometer-alt"), "Efficiency Metrics (PUE, WUE, CUE)"], className="section-title"),
                html.Div(id='efficiency-metrics')
            ], className="glass-card animate-in")
        ], className="mb-4")
    ]),
    
    # NEW: Cost Analysis and Scope Emissions
    dbc.Row([
        dbc.Col([
            html.Div([
                html.Div([html.I(className="fas fa-dollar-sign"), "Cost Analysis & ROI"], className="section-title"),
                html.Div(id='cost-analysis')
            ], className="glass-card animate-in", style={'height': '650px', 'overflow': 'auto'})
        ], md=6, className="mb-4"),
        dbc.Col([
            html.Div([
                html.Div([html.I(className="fas fa-chart-pie"), "Scope Emissions Breakdown"], className="section-title"),
                dcc.Graph(id='scope-emissions-chart', config={'displayModeBar': False}, style={'height': '580px'})
            ], className="glass-card animate-in", style={'height': '650px'})
        ], md=6, className="mb-4"),
    ]),
    
    dbc.Row([
        dbc.Col([
            html.Div(id='forecast-chart', className="animate-in")
        ], md=12, className="mb-4"),
    ]),
    
    dbc.Row([
        dbc.Col([
            html.Div([
                html.Div([html.I(className="fas fa-lightbulb"), "Sustainability Recommendations"], className="section-title"),
                html.Div(id='recommendations-card')
            ], className="glass-card animate-in")
        ], md=6, className="mb-4"),
        dbc.Col([
            html.Div([
                html.Div([html.I(className="fas fa-balance-scale"), "Industry Comparison"], className="section-title"),
                html.Div(id='dc-comparison')
            ], className="glass-card animate-in")
        ], md=6, className="mb-4"),
    ]),
    
    html.Div([
        html.P([html.I(className="fas fa-leaf me-2", style={'color': COLORS['primary']}),
               "AIrth - Sustainable Energy Platform | Powered by AI & Machine Learning"],
              style={'color': 'rgba(248, 250, 252, 0.6)', 'marginBottom': '0.5rem', 'textAlign': 'center'}),
        html.P(["Supporting ", html.Span("SDG 7 (Clean Energy)", style={'color': COLORS['primary'], 'fontWeight': '600'}),
               " & ", html.Span("SDG 13 (Climate Action)", style={'color': COLORS['success'], 'fontWeight': '600'})],
              style={'color': 'rgba(248, 250, 252, 0.5)', 'fontSize': '0.875rem', 'textAlign': 'center'})
    ], style={'marginTop': '4rem', 'paddingTop': '3rem', 'borderTop': '1px solid rgba(255, 255, 255, 0.1)'})
], fluid=True, style={'padding': '2rem'})

# Callbacks
@app.callback(
    [Output('forecast-chart', 'children'),
     Output('recommendations-card', 'children'),
     Output('carbon-calculator', 'children'),
     Output('dc-comparison', 'children'),
     Output('efficiency-metrics', 'children'),
     Output('cost-analysis', 'children'),
     Output('scope-emissions-chart', 'figure'),
     Output('climate-impact-section', 'children')],
    [Input('dc-selector', 'value')]
)
def update_all(dc_name):
    return (create_forecast_chart(dc_name),
            create_recommendations(dc_name),
            create_carbon_calculator(dc_name),
            create_comparison(dc_name),
            create_efficiency_metrics(dc_name),
            create_cost_analysis(dc_name),
            create_scope_emissions_chart(dc_name),
            create_climate_impact_section(dc_name))

if __name__ == '__main__':
    print("\n" + "="*70)
    print("🌍 AIrth - Final Innovation Edition")
    print("="*70)
    print(f"\n✓ {len(platform.data_centers)} global data centers loaded")
    print("✓ AI prediction model trained")
    print("✓ Premium UI with innovative features initialized")
    print("\n🚀 INNOVATIVE FEATURES:")
    print("  • Fixed dropdown selector (fully functional)")
    print("  • Carbon Offset Calculator (trees, cars, homes)")
    print("  • Industry Comparison (best vs worst performers)")
    print("  • Real-time sustainability scoring")
    print("  • Interactive data center analysis")
    print("\n📱 Open: http://127.0.0.1:8050")
    print("\n⌨️  Press Ctrl+C to stop")
    print("="*70 + "\n")
    
    app.run(debug=True, host='127.0.0.1', port=8050)

