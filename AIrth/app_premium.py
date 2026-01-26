import dash
from dash import dcc, html, Input, Output
import dash_bootstrap_components as dbc
import plotly.graph_objs as go
import pandas as pd
import numpy as np
from airth_platform import AIrthPlatform


platform = AIrthPlatform()


data_centers = [
    ("Google Council Bluffs Iowa", (41.2619, -95.8608), 180, 850000, 0.52, 75),
    ("AWS US-East Virginia", (38.9072, -77.0369), 200, 900000, 0.45, 45),
    ("Microsoft Azure Virginia", (38.8816, -77.1045), 175, 820000, 0.45, 50),
    ("Facebook Prineville Oregon", (44.2999, -120.8342), 160, 780000, 0.28, 80),
    ("Apple Mesa Arizona", (33.4152, -111.8315), 140, 700000, 0.42, 85),
    ("Google Hamina Finland", (60.5695, 27.1978), 120, 750000, 0.15, 95),
    ("Azure Netherlands", (52.3676, 4.9041), 95, 600000, 0.35, 65),
    ("AWS Frankfurt Germany", (50.1109, 8.6821), 110, 650000, 0.38, 55),
    ("OVH Roubaix France", (50.6942, 3.1746), 85, 520000, 0.32, 60),
    ("Equinix London", (51.5074, -0.1278), 100, 580000, 0.28, 70),
    ("China Telecom Inner Mongolia", (40.8414, 111.7519), 150, 1000000, 0.65, 15),
    ("Meta Singapore", (1.3521, 103.8198), 110, 700000, 0.42, 30),
    ("AWS Tokyo Japan", (35.6762, 139.6503), 130, 720000, 0.48, 35),
    ("Alibaba Hangzhou China", (30.2741, 120.1551), 145, 850000, 0.62, 20),
    ("NTT Mumbai India", (19.0760, 72.8777), 105, 640000, 0.72, 25),
    ("AWS Sydney Australia", (-33.8688, 151.2093), 95, 580000, 0.82, 22),
    ("Azure São Paulo Brazil", (-23.5505, -46.6333), 88, 550000, 0.48, 40),
    ("Equinix Dubai UAE", (25.2048, 55.2708), 92, 560000, 0.55, 28),
    ("AWS Seoul South Korea", (37.5665, 126.9780), 115, 680000, 0.52, 32),
    ("Microsoft Johannesburg", (-26.2041, 28.0473), 78, 480000, 0.88, 18),
]

for name, location, power, area, carbon, renewable in data_centers:
    platform.add_data_center(name, location, power, area, carbon, renewable)

platform.train_prediction_model()

# Initialize Dash app
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
    'primary': '#00FFA3',
    'secondary': '#7C3AED',
    'accent': '#F59E0B',
    'danger': '#EF4444',
    'success': '#10B981',
    'info': '#3B82F6',
    'dark': '#0F172A',
    'darker': '#020617',
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
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }
        
        body {
            font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
            background: linear-gradient(135deg, #0F172A 0%, #1E293B 50%, #0F172A 100%);
            color: #F8FAFC;
            overflow-x: hidden;
            min-height: 100vh;
        }
        
        /* Animated background */
        body::before {
            content: '';
            position: fixed;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            background: 
                radial-gradient(circle at 20% 50%, rgba(124, 58, 237, 0.15) 0%, transparent 50%),
                radial-gradient(circle at 80% 80%, rgba(0, 255, 163, 0.1) 0%, transparent 50%),
                radial-gradient(circle at 40% 20%, rgba(59, 130, 246, 0.1) 0%, transparent 50%);
            animation: backgroundShift 20s ease infinite;
            pointer-events: none;
            z-index: 0;
        }
        
        @keyframes backgroundShift {
            0%, 100% { opacity: 1; transform: scale(1); }
            50% { opacity: 0.8; transform: scale(1.1); }
        }
        
        .container-fluid {
            position: relative;
            z-index: 1;
        }
        
        /* Premium glassmorphism cards */
        .glass-card {
            background: rgba(15, 23, 42, 0.7);
            backdrop-filter: blur(20px) saturate(180%);
            border: 1px solid rgba(255, 255, 255, 0.1);
            border-radius: 24px;
            padding: 2rem;
            box-shadow: 
                0 20px 60px rgba(0, 0, 0, 0.3),
                inset 0 1px 0 rgba(255, 255, 255, 0.1);
            transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1);
            position: relative;
            overflow: hidden;
        }
        
        .glass-card::before {
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
        
        .glass-card:hover {
            transform: translateY(-8px);
            border-color: rgba(0, 255, 163, 0.3);
            box-shadow: 
                0 30px 80px rgba(0, 0, 0, 0.4),
                0 0 40px rgba(0, 255, 163, 0.2),
                inset 0 1px 0 rgba(255, 255, 255, 0.2);
        }
        
        .glass-card:hover::before {
            opacity: 1;
        }
        
        /* Premium stat cards */
        .stat-card {
            background: linear-gradient(135deg, rgba(15, 23, 42, 0.9) 0%, rgba(30, 41, 59, 0.9) 100%);
            backdrop-filter: blur(20px);
            border: 1px solid rgba(255, 255, 255, 0.1);
            border-radius: 20px;
            padding: 2rem;
            text-align: center;
            transition: all 0.3s ease;
            position: relative;
            overflow: hidden;
        }
        
        .stat-card::after {
            content: '';
            position: absolute;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            background: linear-gradient(135deg, transparent 0%, rgba(255, 255, 255, 0.05) 100%);
            opacity: 0;
            transition: opacity 0.3s;
        }
        
        .stat-card:hover {
            transform: translateY(-5px) scale(1.02);
            box-shadow: 0 20px 40px rgba(0, 0, 0, 0.3);
        }
        
        .stat-card:hover::after {
            opacity: 1;
        }
        
        .stat-icon {
            font-size: 2.5rem;
            margin-bottom: 1rem;
            display: inline-block;
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
            background-clip: text;
        }
        
        .stat-label {
            font-size: 0.875rem;
            color: rgba(248, 250, 252, 0.6);
            text-transform: uppercase;
            letter-spacing: 0.1em;
            font-weight: 600;
        }
        
        /* Premium header */
        .premium-header {
            text-align: center;
            padding: 3rem 0 2rem 0;
            position: relative;
        }
        
        .premium-title {
            font-size: 4rem;
            font-weight: 900;
            background: linear-gradient(135deg, #00FFA3 0%, #7C3AED 50%, #F59E0B 100%);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            background-clip: text;
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
            letter-spacing: 0.05em;
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
            backdrop-filter: blur(10px);
        }
        
        /* Section titles */
        .section-title {
            font-size: 1.75rem;
            font-weight: 700;
            margin-bottom: 1.5rem;
            color: #F8FAFC;
            display: flex;
            align-items: center;
            gap: 1rem;
        }
        
        .section-title i {
            color: #00FFA3;
            font-size: 1.5rem;
        }
        
        /* Dropdown styling */
        .Select-control {
            background: rgba(15, 23, 42, 0.8) !important;
            border: 1px solid rgba(255, 255, 255, 0.1) !important;
            border-radius: 12px !important;
            color: #F8FAFC !important;
        }
        
        .Select-menu-outer {
            background: rgba(15, 23, 42, 0.95) !important;
            border: 1px solid rgba(255, 255, 255, 0.1) !important;
            border-radius: 12px !important;
            backdrop-filter: blur(20px);
        }
        
        .Select-option {
            background: transparent !important;
            color: #F8FAFC !important;
        }
        
        .Select-option:hover {
            background: rgba(0, 255, 163, 0.1) !important;
        }
        
        /* Animations */
        @keyframes fadeInUp {
            from {
                opacity: 0;
                transform: translateY(30px);
            }
            to {
                opacity: 1;
                transform: translateY(0);
            }
        }
        
        .animate-in {
            animation: fadeInUp 0.6s ease-out forwards;
            opacity: 0;
        }
        
        .animate-delay-1 { animation-delay: 0.1s; }
        .animate-delay-2 { animation-delay: 0.2s; }
        .animate-delay-3 { animation-delay: 0.3s; }
        .animate-delay-4 { animation-delay: 0.4s; }
        
        /* Recommendation cards */
        .rec-card {
            background: rgba(15, 23, 42, 0.6);
            border-left: 3px solid;
            border-radius: 12px;
            padding: 1.5rem;
            margin-bottom: 1rem;
            backdrop-filter: blur(10px);
            transition: all 0.3s ease;
        }
        
        .rec-card:hover {
            transform: translateX(5px);
            box-shadow: 0 10px 30px rgba(0, 0, 0, 0.2);
        }
        
        .rec-high { border-color: #EF4444; }
        .rec-medium { border-color: #F59E0B; }
        .rec-low { border-color: #10B981; }
        
        /* Footer */
        .premium-footer {
            text-align: center;
            padding: 3rem 0;
            margin-top: 4rem;
            border-top: 1px solid rgba(255, 255, 255, 0.1);
        }
        
        /* Scrollbar */
        ::-webkit-scrollbar {
            width: 10px;
        }
        
        ::-webkit-scrollbar-track {
            background: rgba(15, 23, 42, 0.5);
        }
        
        ::-webkit-scrollbar-thumb {
            background: linear-gradient(135deg, #00FFA3, #7C3AED);
            border-radius: 5px;
        }
        
        ::-webkit-scrollbar-thumb:hover {
            background: linear-gradient(135deg, #7C3AED, #00FFA3);
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

# Calculate global stats
total_power = sum(dc.power_mw for dc in platform.data_centers)
total_emissions = sum(dc.carbon_emissions_tons_year for dc in platform.data_centers)
total_water = sum(dc.water_usage_liters_day for dc in platform.data_centers)
avg_renewable = np.mean([dc.renewable_percentage for dc in platform.data_centers])

# Create premium stat cards
def create_stat_card(title, value, icon, color):
    return html.Div([
        html.I(className=f"fas {icon} stat-icon", style={'color': color}),
        html.Div(value, className="stat-value"),
        html.Div(title, className="stat-label")
    ], className="stat-card")

# Create global map
def create_map():
    fig = go.Figure()
    
    for dc in platform.data_centers:
        metrics = dc.get_metrics()
        
        if metrics['effective_emissions'] < 50000:
            color = '#10B981'
        elif metrics['effective_emissions'] < 150000:
            color = '#F59E0B'
        else:
            color = '#EF4444'
        
        hover_text = f"<b>{dc.name}</b><br>" \
                    f"Power: {dc.power_mw:.0f} MW<br>" \
                    f"Emissions: {metrics['effective_emissions']:.0f} tons CO₂/year<br>" \
                    f"Renewable: {dc.renewable_percentage:.0f}%"
        
        fig.add_trace(go.Scattergeo(
            lon=[dc.location[1]],
            lat=[dc.location[0]],
            text=hover_text,
            hoverinfo='text',
            mode='markers',
            marker=dict(
                size=max(10, dc.power_mw / 12),
                color=color,
                line=dict(width=2, color='white'),
                opacity=0.9
            ),
            name=dc.name,
            showlegend=False
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
            bgcolor='rgba(0,0,0,0)'
        ),
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        margin=dict(l=0, r=0, t=0, b=0),
        height=500
    )
    
    return fig

# Create emissions chart
def create_emissions_chart():
    data = []
    for dc in platform.data_centers:
        metrics = dc.get_metrics()
        data.append({
            'name': dc.name,
            'emissions': metrics['carbon_emissions_tons_year'],
            'effective': metrics['effective_emissions']
        })
    
    df = pd.DataFrame(data).sort_values('emissions', ascending=True).tail(10)
    
    fig = go.Figure()
    fig.add_trace(go.Bar(
        y=df['name'],
        x=df['emissions'],
        name='Total Emissions',
        orientation='h',
        marker=dict(
            color='#EF4444',
            line=dict(color='#DC2626', width=1)
        )
    ))
    fig.add_trace(go.Bar(
        y=df['name'],
        x=df['effective'],
        name='Effective Emissions',
        orientation='h',
        marker=dict(
            color='#10B981',
            line=dict(color='#059669', width=1)
        )
    ))
    
    fig.update_layout(
        xaxis_title='CO₂ Emissions (tons/year)',
        barmode='group',
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        font=dict(color='#F8FAFC', family='Inter'),
        height=400,
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
        xaxis=dict(gridcolor='rgba(255, 255, 255, 0.1)'),
        yaxis=dict(gridcolor='rgba(255, 255, 255, 0.1)')
    )
    
    return fig

# Create renewable energy chart
def create_renewable_chart():
    data = []
    for dc in platform.data_centers:
        data.append({
            'name': dc.name,
            'renewable': dc.renewable_percentage,
            'non_renewable': 100 - dc.renewable_percentage
        })
    
    df = pd.DataFrame(data).sort_values('renewable', ascending=False).head(10)
    
    fig = go.Figure()
    fig.add_trace(go.Bar(
        y=df['name'],
        x=df['renewable'],
        name='Renewable',
        orientation='h',
        marker=dict(
            color='#10B981',
            line=dict(color='#059669', width=1)
        )
    ))
    fig.add_trace(go.Bar(
        y=df['name'],
        x=df['non_renewable'],
        name='Non-Renewable',
        orientation='h',
        marker=dict(
            color='#64748B',
            line=dict(color='#475569', width=1)
        )
    ))
    
    fig.update_layout(
        xaxis_title='Energy Mix (%)',
        barmode='stack',
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        font=dict(color='#F8FAFC', family='Inter'),
        height=400,
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
        xaxis=dict(gridcolor='rgba(255, 255, 255, 0.1)'),
        yaxis=dict(gridcolor='rgba(255, 255, 255, 0.1)')
    )
    
    return fig

# Create forecast chart
def create_forecast_chart(dc_name):
    dc = next((d for d in platform.data_centers if d.name == dc_name), None)
    if not dc:
        return go.Figure()
    
    predictions = platform.predictor.predict_future_emissions(dc, years_ahead=10)
    years = list(range(11))
    
    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=years,
        y=predictions,
        mode='lines+markers',
        name='Predicted Emissions',
        line=dict(color='#EF4444', width=3),
        marker=dict(size=10, color='#EF4444', line=dict(color='white', width=2)),
        fill='tozeroy',
        fillcolor='rgba(239, 68, 68, 0.1)'
    ))
    
    baseline = [dc.carbon_emissions_tons_year] * 11
    fig.add_trace(go.Scatter(
        x=years,
        y=baseline,
        mode='lines',
        name='Current Emissions',
        line=dict(color='#64748B', width=2, dash='dash')
    ))
    
    fig.update_layout(
        xaxis_title='Years from Now',
        yaxis_title='CO₂ Emissions (tons/year)',
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        font=dict(color='#F8FAFC', family='Inter'),
        height=400,
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
        xaxis=dict(gridcolor='rgba(255, 255, 255, 0.1)'),
        yaxis=dict(gridcolor='rgba(255, 255, 255, 0.1)')
    )
    
    return fig

def create_recommendations(dc_name):
    dc = next((d for d in platform.data_centers if d.name == dc_name), None)
    if not dc:
        return html.Div("No data center selected")
    
    analysis = platform.recommender.analyze_and_recommend(dc, 0.5)
    

    score = analysis['sustainability_score']
    score_color = '#10B981' if score > 70 else '#F59E0B' if score > 40 else '#EF4444'
    
    score_card = html.Div([
        html.Div([
            html.I(className="fas fa-award", style={'fontSize': '3rem', 'color': score_color, 'marginBottom': '1rem'}),
            html.H2(f"{score:.0f}/100", style={'fontSize': '3rem', 'fontWeight': '800', 'color': score_color, 'marginBottom': '0.5rem'}),
            html.P("Sustainability Score", style={'color': 'rgba(248, 250, 252, 0.6)', 'fontSize': '0.875rem', 'textTransform': 'uppercase', 'letterSpacing': '0.1em'}),
            html.Hr(style={'borderColor': 'rgba(255, 255, 255, 0.1)', 'margin': '1.5rem 0'}),
            html.P([
                html.I(className="fas fa-chart-line me-2", style={'color': '#10B981'}),
                f"Potential Reduction: {analysis['total_emission_reduction_tons']:.0f} tons CO₂/year"
            ], style={'color': '#10B981', 'fontWeight': '600'})
        ], style={'textAlign': 'center', 'padding': '2rem'})
    ], className="glass-card mb-4")

    rec_cards = []
    for rec in analysis['recommendations']:
        priority_class = f"rec-{rec['priority'].lower()}"
        priority_colors = {
            'HIGH': '#EF4444',
            'MEDIUM': '#F59E0B',
            'LOW': '#10B981'
        }
        color = priority_colors.get(rec['priority'], '#64748B')
        
        card = html.Div([
            html.Div([
                html.Span([
                    html.I(className="fas fa-exclamation-circle me-2"),
                    rec['priority']
                ], style={
                    'backgroundColor': f"{color}20",
                    'color': color,
                    'padding': '0.25rem 0.75rem',
                    'borderRadius': '50px',
                    'fontSize': '0.75rem',
                    'fontWeight': '700',
                    'textTransform': 'uppercase',
                    'letterSpacing': '0.05em'
                }),
                html.H5(rec['category'], style={'marginTop': '1rem', 'marginBottom': '0.75rem', 'color': '#F8FAFC'})
            ]),
            html.P([html.Strong("Action: "), rec['action']], style={'marginBottom': '0.5rem', 'color': 'rgba(248, 250, 252, 0.8)'}),
            html.P([html.Strong("Impact: "), rec['impact']], style={'marginBottom': '0.5rem', 'color': '#10B981'}),
            html.P([html.Strong("Implementation: "), rec['implementation']], style={'marginBottom': '0', 'color': 'rgba(248, 250, 252, 0.6)', 'fontSize': '0.875rem'})
        ], className=f"rec-card {priority_class}")
        
        rec_cards.append(card)
    
    return html.Div([score_card] + rec_cards)


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
                html.Div([
                    html.I(className="fas fa-globe-americas"),
                    "Global Data Center Network"
                ], className="section-title"),
                dcc.Graph(figure=create_map(), config={'displayModeBar': False})
            ], className="glass-card animate-in")
        ], className="mb-4")
    ]),
    

    dbc.Row([
        dbc.Col([
            html.Div([
                html.Div([
                    html.I(className="fas fa-chart-bar"),
                    "Emissions Analysis"
                ], className="section-title"),
                dcc.Graph(figure=create_emissions_chart(), config={'displayModeBar': False})
            ], className="glass-card animate-in")
        ], md=6, className="mb-4"),
        dbc.Col([
            html.Div([
                html.Div([
                    html.I(className="fas fa-solar-panel"),
                    "Energy Mix Distribution"
                ], className="section-title"),
                dcc.Graph(figure=create_renewable_chart(), config={'displayModeBar': False})
            ], className="glass-card animate-in")
        ], md=6, className="mb-4"),
    ]),
    

    dbc.Row([
        dbc.Col([
            html.Div([
                html.Div([
                    html.I(className="fas fa-search"),
                    "Select Data Center for Detailed Analysis"
                ], className="section-title"),
                dcc.Dropdown(
                    id='dc-selector',
                    options=[{'label': dc.name, 'value': dc.name} for dc in platform.data_centers],
                    value=platform.data_centers[0].name,
                    clearable=False,
                    style={'color': '#000'}
                )
            ], className="glass-card animate-in")
        ], className="mb-4")
    ]),
    
    # Forecast and Recommendations
    dbc.Row([
        dbc.Col([
            html.Div([
                html.Div([
                    html.I(className="fas fa-chart-line"),
                    "10-Year Emissions Forecast"
                ], className="section-title"),
                dcc.Graph(id='forecast-chart', config={'displayModeBar': False})
            ], className="glass-card animate-in")
        ], md=6, className="mb-4"),
        dbc.Col([
            html.Div([
                html.Div([
                    html.I(className="fas fa-lightbulb"),
                    "Sustainability Recommendations"
                ], className="section-title"),
                html.Div(id='recommendations-card')
            ], className="glass-card animate-in")
        ], md=6, className="mb-4"),
    ]),
    

    html.Div([
        html.P([
            html.I(className="fas fa-leaf me-2", style={'color': COLORS['primary']}),
            "AIrth - Sustainable Energy Platform | Powered by AI & Machine Learning"
        ], style={'color': 'rgba(248, 250, 252, 0.6)', 'marginBottom': '0.5rem'}),
        html.P([
            "Supporting ",
            html.Span("SDG 7 (Clean Energy)", style={'color': COLORS['primary'], 'fontWeight': '600'}),
            " & ",
            html.Span("SDG 13 (Climate Action)", style={'color': COLORS['success'], 'fontWeight': '600'})
        ], style={'color': 'rgba(248, 250, 252, 0.5)', 'fontSize': '0.875rem'})
    ], className="premium-footer")
], fluid=True, style={'padding': '2rem'})


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
    print("✓ Premium UI initialized with glassmorphism & animations")
    print("\n🚀 Starting server...")
    print("\n📱 Open: http://127.0.0.1:8050")
    print("\n⌨️  Press Ctrl+C to stop")
    print("="*70 + "\n")
    
    app.run(debug=True, host='127.0.0.1', port=8050)

