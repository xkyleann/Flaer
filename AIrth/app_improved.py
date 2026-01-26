import dash
from dash import dcc, html, Input, Output
import dash_bootstrap_components as dbc
import plotly.graph_objs as go
import plotly.express as px
import pandas as pd
import numpy as np
from airth_platform import AIrthPlatform

# Initialize platform
platform = AIrthPlatform()

# Add comprehensive global data centers
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
    external_stylesheets=[dbc.themes.CYBORG, dbc.icons.FONT_AWESOME],
    suppress_callback_exceptions=True
)

app.title = "AIrth - Sustainable Energy Platform"

# Calculate global stats
total_power = sum(dc.power_mw for dc in platform.data_centers)
total_emissions = sum(dc.carbon_emissions_tons_year for dc in platform.data_centers)
total_water = sum(dc.water_usage_liters_day for dc in platform.data_centers)
avg_renewable = np.mean([dc.renewable_percentage for dc in platform.data_centers])

# Create stat cards
def create_stat_card(title, value, icon, color):
    return dbc.Card([
        dbc.CardBody([
            html.Div([
                html.I(className=f"fas {icon} fa-2x", style={'color': color}),
                html.H3(value, className="mt-3 mb-0", style={'color': color}),
                html.P(title, className="text-muted mb-0")
            ], className="text-center")
        ])
    ], className="mb-3", style={'backgroundColor': '#1a1a1a', 'border': f'1px solid {color}'})

# Create global map
def create_map():
    fig = go.Figure()
    
    for dc in platform.data_centers:
        metrics = dc.get_metrics()
        
        if metrics['effective_emissions'] < 50000:
            color = '#00ff00'
        elif metrics['effective_emissions'] < 150000:
            color = '#ffaa00'
        else:
            color = '#ff0000'
        
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
                size=max(8, dc.power_mw / 15),
                color=color,
                line=dict(width=2, color='white'),
                opacity=0.8
            ),
            name=dc.name,
            showlegend=False
        ))
    
    fig.update_layout(
        geo=dict(
            projection_type='natural earth',
            showland=True,
            landcolor='#2a2a2a',
            coastlinecolor='#444',
            showocean=True,
            oceancolor='#1a1a1a',
            showcountries=True,
            countrycolor='#444',
            bgcolor='#0a0a0a'
        ),
        paper_bgcolor='#0a0a0a',
        plot_bgcolor='#0a0a0a',
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
            'effective': metrics['effective_emissions'],
            'renewable': dc.renewable_percentage
        })
    
    df = pd.DataFrame(data).sort_values('emissions', ascending=True).tail(10)
    
    fig = go.Figure()
    fig.add_trace(go.Bar(
        y=df['name'],
        x=df['emissions'],
        name='Total Emissions',
        orientation='h',
        marker=dict(color='#ff6b6b')
    ))
    fig.add_trace(go.Bar(
        y=df['name'],
        x=df['effective'],
        name='Effective Emissions',
        orientation='h',
        marker=dict(color='#4ecdc4')
    ))
    
    fig.update_layout(
        title='Top 10 Data Centers by Emissions',
        xaxis_title='CO₂ Emissions (tons/year)',
        barmode='group',
        paper_bgcolor='#0a0a0a',
        plot_bgcolor='#1a1a1a',
        font=dict(color='white'),
        height=400,
        showlegend=True,
        legend=dict(orientation='h', yanchor='bottom', y=1.02, xanchor='right', x=1)
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
        marker=dict(color='#51cf66')
    ))
    fig.add_trace(go.Bar(
        y=df['name'],
        x=df['non_renewable'],
        name='Non-Renewable',
        orientation='h',
        marker=dict(color='#868e96')
    ))
    
    fig.update_layout(
        title='Top 10 Data Centers by Renewable Energy',
        xaxis_title='Energy Mix (%)',
        barmode='stack',
        paper_bgcolor='#0a0a0a',
        plot_bgcolor='#1a1a1a',
        font=dict(color='white'),
        height=400,
        showlegend=True,
        legend=dict(orientation='h', yanchor='bottom', y=1.02, xanchor='right', x=1)
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
        line=dict(color='#ff6b6b', width=3),
        marker=dict(size=8)
    ))
    
    baseline = [dc.carbon_emissions_tons_year] * 11
    fig.add_trace(go.Scatter(
        x=years,
        y=baseline,
        mode='lines',
        name='Current Emissions',
        line=dict(color='#868e96', width=2, dash='dash')
    ))
    
    fig.update_layout(
        title=f'10-Year Emissions Forecast: {dc.name}',
        xaxis_title='Years from Now',
        yaxis_title='CO₂ Emissions (tons/year)',
        paper_bgcolor='#0a0a0a',
        plot_bgcolor='#1a1a1a',
        font=dict(color='white'),
        height=400,
        showlegend=True,
        legend=dict(orientation='h', yanchor='bottom', y=1.02, xanchor='right', x=1)
    )
    
    return fig

# Create recommendations
def create_recommendations(dc_name):
    dc = next((d for d in platform.data_centers if d.name == dc_name), None)
    if not dc:
        return html.Div("No data center selected")
    
    analysis = platform.recommender.analyze_and_recommend(dc, 0.5)
    
    cards = []
    for rec in analysis['recommendations']:
        priority_colors = {
            'HIGH': '#ff6b6b',
            'MEDIUM': '#ffa94d',
            'LOW': '#51cf66'
        }
        color = priority_colors.get(rec['priority'], '#868e96')
        
        card = dbc.Card([
            dbc.CardHeader([
                html.I(className="fas fa-lightbulb me-2", style={'color': color}),
                html.Strong(rec['category']),
                dbc.Badge(rec['priority'], color="danger" if rec['priority'] == 'HIGH' else "warning", className="ms-2")
            ], style={'backgroundColor': '#1a1a1a', 'borderBottom': f'2px solid {color}'}),
            dbc.CardBody([
                html.P([html.Strong("Action: "), rec['action']], className="mb-2"),
                html.P([html.Strong("Impact: "), rec['impact']], className="mb-2", style={'color': '#51cf66'}),
                html.P([html.Strong("Implementation: "), rec['implementation']], className="mb-0", style={'fontSize': '0.9em'})
            ])
        ], className="mb-3", style={'backgroundColor': '#1a1a1a', 'border': f'1px solid {color}'})
        
        cards.append(card)
    
    score_card = dbc.Card([
        dbc.CardBody([
            html.H4("Sustainability Score", className="text-center mb-3"),
            html.H1(f"{analysis['sustainability_score']:.0f}/100", 
                   className="text-center mb-3",
                   style={'color': '#51cf66' if analysis['sustainability_score'] > 70 else '#ffa94d'}),
            html.P(f"Potential Reduction: {analysis['total_emission_reduction_tons']:.0f} tons CO₂/year",
                  className="text-center text-muted mb-0")
        ])
    ], className="mb-3", style={'backgroundColor': '#1a1a1a', 'border': '1px solid #51cf66'})
    
    return html.Div([score_card] + cards)

# App layout
app.layout = dbc.Container([
    # Header
    dbc.Row([
        dbc.Col([
            html.H1([
                html.I(className="fas fa-globe me-3", style={'color': '#51cf66'}),
                "AIrth"
            ], className="text-center my-4"),
            html.P("Sustainable Energy Platform - AI-Powered Data Center Analysis",
                  className="text-center text-muted mb-4")
        ])
    ]),
    
    # Stats
    dbc.Row([
        dbc.Col(create_stat_card("Total Power", f"{total_power:.0f} MW", "fa-bolt", "#ffa94d"), md=3),
        dbc.Col(create_stat_card("CO₂ Emissions", f"{total_emissions/1000:.1f}k tons", "fa-smog", "#ff6b6b"), md=3),
        dbc.Col(create_stat_card("Water Usage", f"{total_water/1000000:.1f}M L/day", "fa-tint", "#4ecdc4"), md=3),
        dbc.Col(create_stat_card("Renewable", f"{avg_renewable:.1f}%", "fa-leaf", "#51cf66"), md=3),
    ], className="mb-4"),
    
    # Global Map
    dbc.Row([
        dbc.Col([
            dbc.Card([
                dbc.CardHeader(html.H5("Global Data Center Network", className="mb-0")),
                dbc.CardBody([
                    dcc.Graph(figure=create_map(), config={'displayModeBar': False})
                ])
            ], style={'backgroundColor': '#1a1a1a'})
        ])
    ], className="mb-4"),
    
    # Charts
    dbc.Row([
        dbc.Col([
            dbc.Card([
                dbc.CardBody([
                    dcc.Graph(figure=create_emissions_chart(), config={'displayModeBar': False})
                ])
            ], style={'backgroundColor': '#1a1a1a'})
        ], md=6),
        dbc.Col([
            dbc.Card([
                dbc.CardBody([
                    dcc.Graph(figure=create_renewable_chart(), config={'displayModeBar': False})
                ])
            ], style={'backgroundColor': '#1a1a1a'})
        ], md=6),
    ], className="mb-4"),
    
    # Data Center Selector
    dbc.Row([
        dbc.Col([
            dbc.Card([
                dbc.CardHeader(html.H5("Select Data Center for Detailed Analysis", className="mb-0")),
                dbc.CardBody([
                    dcc.Dropdown(
                        id='dc-selector',
                        options=[{'label': dc.name, 'value': dc.name} for dc in platform.data_centers],
                        value=platform.data_centers[0].name,
                        clearable=False,
                        style={'color': '#000'}
                    )
                ])
            ], style={'backgroundColor': '#1a1a1a'})
        ])
    ], className="mb-4"),
    
    # Forecast and Recommendations
    dbc.Row([
        dbc.Col([
            dbc.Card([
                dbc.CardBody([
                    dcc.Graph(id='forecast-chart', config={'displayModeBar': False})
                ])
            ], style={'backgroundColor': '#1a1a1a'})
        ], md=6),
        dbc.Col([
            html.Div(id='recommendations-card')
        ], md=6),
    ], className="mb-4"),
    
    # Footer
    dbc.Row([
        dbc.Col([
            html.Hr(),
            html.P([
                html.I(className="fas fa-leaf me-2", style={'color': '#51cf66'}),
                "AIrth - Supporting SDG 7 (Clean Energy) & SDG 13 (Climate Action)"
            ], className="text-center text-muted")
        ])
    ])
], fluid=True, style={'backgroundColor': '#0a0a0a', 'minHeight': '100vh', 'padding': '20px'})

# Callbacks
@app.callback(
    [Output('forecast-chart', 'figure'),
     Output('recommendations-card', 'children')],
    [Input('dc-selector', 'value')]
)
def update_analysis(dc_name):
    return create_forecast_chart(dc_name), create_recommendations(dc_name)

if __name__ == '__main__':
    print("\n" + "="*70)
    print("🌍 AIrth - Sustainable Energy Platform")
    print("="*70)
    print(f"\n✓ {len(platform.data_centers)} global data centers loaded")
    print("✓ AI prediction model trained")
    print("✓ Web interface initialized")
    print("\n🚀 Starting server...")
    print("\n📱 Open: http://127.0.0.1:8050")
    print("\n⌨️  Press Ctrl+C to stop")
    print("="*70 + "\n")
    
    app.run(debug=True, host='127.0.0.1', port=8050)
